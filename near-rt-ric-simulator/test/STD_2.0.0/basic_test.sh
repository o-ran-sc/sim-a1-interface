#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2021 Nordix Foundation. All rights reserved.
#  ========================================================================
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ============LICENSE_END=================================================
#

# Script for basic test of the simulator.
# Run the build_and_start with the same arg, except arg 'nonsecure|secure', as this script

print_usage() {
    echo "Usage: ./basic_test.sh nonsecure|secure duplicate-check|ignore-duplicate "
    exit 1
}

if [ $# -ne 2 ]; then
    print_usage
fi
if [ "$1" != "nonsecure" ] && [ "$1" != "secure" ]; then
    print_usage
fi
if [ "$2" == "duplicate-check" ]; then
    DUP_CHECK=1
elif [ "$2" == "ignore-duplicate" ]; then
    DUP_CHECK=0
else
    print_usage
fi

if [ $1 == "nonsecure" ]; then
    #Default http port for the simulator
    PORT=8085
    # Set http protocol
    HTTPX="http"
else
    #Default https port for the simulator
    PORT=8185
    # Set https protocol
    HTTPX="https"
fi

. ../common/test_common.sh


echo "=== Simulator hello world ==="
RESULT="OK"
do_curl GET / 200

echo "=== Check used and implemented interfaces ==="
RESULT="Current interface: STD_2.0.0 All supported A1 interface yamls in this container: ['OSC_2.1.0', 'STD_1.1.3', 'STD_2.0.0']"
do_curl GET /container_interfaces 200

echo "=== Reset simulator instances ==="
RESULT="All policy instances deleted"
do_curl POST /deleteinstances 200

echo "=== Reset simulator, all ==="
RESULT="All policy instances and types deleted"
do_curl POST /deleteall 200

echo "=== Get counter: interface ==="
RESULT="STD_2.0.0"
do_curl GET /counter/interface 200

echo "=== Get counter: remote hosts ==="
RESULT="*"
do_curl GET /counter/remote_hosts 200

echo "=== Get counter: intstance ==="
RESULT="0"
do_curl GET /counter/num_instances 200

echo "=== Get counter: types (shall be 0)==="
RESULT="0"
do_curl GET /counter/num_types 200

echo "=== API: Get policy types, shall be empty array =="
RESULT="json:[]"
do_curl GET /A1-P/v2/policytypes 200

echo "=== API: Get policy instances for type 1, type not found=="
RESULT="json:{\"title\": \"The policy type does not exist.\", \"status\": 404, \"instance\": \"1\"}"
do_curl GET /A1-P/v2/policytypes/1/policies 404

echo "=== API: Get policy instances, type not found=="
RESULT="json:{\"title\": \"The policy type does not exist.\", \"status\": 404, \"instance\": \"test\"}"
do_curl GET /A1-P/v2/policytypes/test/policies 404

echo "=== Put a policy type: STD_1 ==="
RESULT="Policy type STD_1 is OK."
do_curl PUT  '/policytype?id=STD_1' 201 jsonfiles/std_1.json

echo "=== Put a policy type: STD_1, again ==="
RESULT="Policy type STD_1 is OK."
do_curl PUT  '/policytype?id=STD_1' 200 jsonfiles/std_1.json

echo "=== API: Get policy type ids, shall contain type STD_1 =="
RESULT="json:[ \"STD_1\" ]"
do_curl GET /A1-P/v2/policytypes 200

echo "=== Delete a policy type: STD_1 ==="
RESULT=""
do_curl DELETE  '/policytype?id=STD_1' 204

echo "=== API: Get policy type ids, shall be empty =="
RESULT="json:[]"
do_curl GET  /A1-P/v2/policytypes 200

echo "=== Put a policy type: STD_1 ==="
RESULT="Policy type STD_1 is OK."
do_curl PUT  '/policytype?id=STD_1' 201 jsonfiles/std_1.json

echo "=== API: Get policy type ids, shall contain type STD_1 =="
RESULT="json:[ \"STD_1\" ]"
do_curl GET /A1-P/v2/policytypes 200

echo "=== Get counter: types (shall be 1)==="
RESULT="1"
do_curl GET /counter/num_types 200

echo "=== API: Get policy type: STD_1 ==="
res=$(cat jsonfiles/std_1.json)
RESULT="json:$res"
do_curl GET /A1-P/v2/policytypes/STD_1 200

echo "=== API: Get policy instances, shall be empty=="
RESULT="json:[ ]"
do_curl GET /A1-P/v2/policytypes/STD_1/policies 200

echo "=== API: Create policy instance pi1 of type: STD_1 ==="
res=$(cat jsonfiles/pi1.json)
RESULT="json:$res"
do_curl PUT /A1-P/v2/policytypes/STD_1/policies/pi1 201 jsonfiles/pi1.json

echo "=== API: Get policy instance pi1 of type: STD_1 ==="
res=$(cat jsonfiles/pi1.json)
RESULT="json:$res"
do_curl GET /A1-P/v2/policytypes/STD_1/policies/pi1 200

echo "=== API: Update policy instance pi1 of type: STD_1==="
res=$(cat jsonfiles/pi1.json)
RESULT="json:$res"
do_curl PUT /A1-P/v2/policytypes/STD_1/policies/pi1 200 jsonfiles/pi1.json

echo "=== API: Update policy instance pi1 of type: STD_1==="
res=$(cat jsonfiles/pi1_updated.json)
RESULT="json:$res"
do_curl PUT /A1-P/v2/policytypes/STD_1/policies/pi1 200 jsonfiles/pi1_updated.json

echo "=== API: Duplicate policy instance json,  pi2 of type: STD_1==="
res=$(cat jsonfiles/pi1_updated.json)
if [ $DUP_CHECK == 1 ]; then
    #Fail with dupl check
    RESULT="json:{\"title\": \"Duplicate, the policy json already exists.\", \"status\": 400, \"instance\": \"pi2\"}"
    do_curl PUT /A1-P/v2/policytypes/STD_1/policies/pi2 400 jsonfiles/pi1_updated.json
else
    #OK without dupl check
    res=$(cat jsonfiles/pi1_updated.json)
    RESULT="json:$res"
    do_curl PUT /A1-P/v2/policytypes/STD_1/policies/pi2 201 jsonfiles/pi1_updated.json

    echo "=== API: DELETE policy instance pi2 ==="
    RESULT=""
    do_curl DELETE /A1-P/v2/policytypes/STD_1/policies/pi2 204
fi

echo "=== API: Get policy instances, shall contain pi1=="
RESULT="json:[ \"pi1\" ]"
do_curl GET /A1-P/v2/policytypes/STD_1/policies 200

echo "=== Put a policy type: STD_2 ==="
RESULT="Policy type STD_2 is OK."
do_curl PUT  '/policytype?id=STD_2' 201 jsonfiles/std_2.json


echo "=== API: Duplicate policy instance id pi1 of type: STD_2==="
res=$(cat jsonfiles/pi1_updated.json)
RESULT="json:{\"title\": \"The policy id already exist for other policy type.\", \"status\": 400, \"instance\": \"pi1\"}"
do_curl PUT /A1-P/v2/policytypes/STD_2/policies/pi1 400 jsonfiles/pi1_updated.json

echo "=== API: Get policy type ids, shall contain type STD_1  and STD_2 =="
RESULT="json:[ \"STD_1\", \"STD_2\" ]"
do_curl GET /A1-P/v2/policytypes 200

echo "=== Get counter: types (shall be 2)==="
RESULT="2"
do_curl GET /counter/num_types 200

echo "=== Get counter: intstance ==="
RESULT="1"
do_curl GET /counter/num_instances 200


echo "=== Set force response code 409. ==="
RESULT="*"
do_curl POST '/forceresponse?code=409' 200

echo "=== API: Get policy instances, shall fail with 409 =="
RESULT="json:{\"title\": \"Conflict\", \"status\": 409, \"detail\": \"Request could not be processed in the current state of the resource\"}"
do_curl GET /A1-P/v2/policytypes/STD_1/policies 409

echo "=== API: Get policy status ==="
RESULT="json:{\"enforceStatus\": \"\", \"enforceReason\": \"\"}"
do_curl GET /A1-P/v2/policytypes/STD_1/policies/pi1/status 200

echo "=== API: Create policy instance pi2 of type: STD_1 ==="
res=$(cat jsonfiles/pi2.json)
RESULT="json:$res"
do_curl PUT /A1-P/v2/policytypes/STD_1/policies/pi2 201 jsonfiles/pi2.json

echo "=== API: Update policy instance pi2 of type: STD_1 ==="
res=$(cat jsonfiles/pi2.json)
RESULT="json:$res"
do_curl PUT '/A1-P/v2/policytypes/STD_1/policies/pi2?notificationDestination=http://localhost:2223/statustest' 200 jsonfiles/pi2.json

echo "=== API: Get policy instances, shall contain pi1 and pi2=="
RESULT="json:[ \"pi1\", \"pi2\" ]"
do_curl GET /A1-P/v2/policytypes/STD_1/policies 200

echo "=== Get counter: types (shall be 2)==="
RESULT="2"
do_curl GET /counter/num_types 200

echo "=== Get counter: intstance ==="
RESULT="2"
do_curl GET /counter/num_instances 200

echo "=== Set force delay 10. ==="
RESULT="Force delay: 10 sec set for all A1 responses"
do_curl POST '/forcedelay?delay=10' 200

echo "=== API: Get policy instances, shall contain pi1 and pi2=="
RESULT="json:[ \"pi1\", \"pi2\" ]"
do_curl GET /A1-P/v2/policytypes/STD_1/policies 200

echo "=== Reset force delay. ==="
RESULT="Force delay: None sec set for all A1 responses"
do_curl POST /forcedelay 200

echo "=== API: Get policy instance pi1 of type: STD_1 ==="
res=$(cat jsonfiles/pi1_updated.json)
RESULT="json:$res"
do_curl GET /A1-P/v2/policytypes/STD_1/policies/pi1 200

echo "=== API: Get policy instance pi2 of type: STD_1 ==="
res=$(cat jsonfiles/pi2.json)
RESULT="json:$res"
do_curl GET /A1-P/v2/policytypes/STD_1/policies/pi2 200

echo "=== API: DELETE policy instance pi1 ==="
RESULT=""
do_curl DELETE /A1-P/v2/policytypes/STD_1/policies/pi1 204

echo "=== API: Get policy instances, shall contain pi1 and pi2=="
RESULT="json:[ \"pi2\" ]"
do_curl GET /A1-P/v2/policytypes/STD_1/policies 200

echo "=== API: Get policy status ==="
RESULT="json:{\"enforceStatus\": \"\", \"enforceReason\": \"\"}"
do_curl GET /A1-P/v2/policytypes/STD_1/policies/pi2/status 200

echo "=== Set status for policy instance pi2 ==="
RESULT="Status set to OK for policy: pi2"
do_curl PUT '/status?policyid=pi2&status=OK' 200

echo "=== API: Get policy status ==="
RESULT="json:{\"enforceStatus\": \"OK\"}"
do_curl GET /A1-P/v2/policytypes/STD_1/policies/pi2/status 200

echo "=== Set status for policy instance pi2 ==="
RESULT="Status set to NOTOK and notok_reason for policy: pi2"
do_curl PUT '/status?policyid=pi2&status=NOTOK&reason=notok_reason' 200

echo "=== API: Get policy status ==="
RESULT="json:{\"enforceStatus\": \"NOTOK\", \"enforceReason\":\"notok_reason\"}"
do_curl GET /A1-P/v2/policytypes/STD_1/policies/pi2/status 200

echo "=== Send status for pi2==="
RESULT="json:{\"enforceStatus\": \"NOTOK\", \"enforceReason\": \"notok_reason\"}"
do_curl POST '/sendstatus?policyid=pi2' 200

echo "=== Get counter: datadelivery ==="
RESULT="0"
do_curl GET /counter/datadelivery 200

echo "=== Send data ==="
echo "{}" > .p.json
RESULT=""
do_curl POST /datadelivery 200 .p.json

echo "=== Get counter: datadelivery ==="
RESULT="1"
do_curl GET /counter/datadelivery 200

echo "=== Get counter: intstance ==="
RESULT="1"
do_curl GET /counter/num_instances 200

echo "=== Get counter: types (shall be 2)==="
RESULT="2"
do_curl GET /counter/num_types 200

echo "=== Get counter: interface ==="
RESULT="STD_2.0.0"
do_curl GET /counter/interface 200

echo "=== Get counter: remote hosts ==="
RESULT="*"
do_curl GET /counter/remote_hosts 200

echo "********************"
echo "*** All tests ok ***"
echo "********************"
