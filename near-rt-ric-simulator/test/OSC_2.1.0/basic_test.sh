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
RESULT="Current interface: OSC_2.1.0 All supported A1 interface yamls in this container: ['OSC_2.1.0', 'STD_1.1.3', 'STD_2.0.0']"
do_curl GET /container_interfaces 200

echo "=== Reset simulator instances ==="
RESULT="All policy instances deleted"
do_curl POST /deleteinstances 200

echo "=== Reset simulator, all ==="
RESULT="All policy instances and types deleted"
do_curl POST /deleteall 200

echo "=== API: Healthcheck ==="
RESULT=""
do_curl GET /a1-p/healthcheck 200

echo "=== API: Get policy types, shall be empty array =="
RESULT="json:[]"
do_curl GET /a1-p/policytypes 200

echo "=== API: Delete a policy type, shall fail =="
RESULT=""
do_curl DELETE /a1-p/policytypes/1 404

echo "=== API: Get policy instances for type 1, shall fail =="
RESULT=""
do_curl GET /a1-p/policytypes/1/policies 404

echo "=== API: Put a policy type: 1 ==="
RESULT=""
do_curl PUT /a1-p/policytypes/1 201 jsonfiles/pt1.json

echo "=== API: Put a policy type: 1, again ==="
RESULT=""
do_curl PUT /a1-p/policytypes/1 201 jsonfiles/pt1.json

echo "=== API: Delete a policy type: 1 ==="
RESULT=""
do_curl DELETE /a1-p/policytypes/1 204

echo "=== API: Get policy type ids, shall be empty =="
RESULT="json:[]"
do_curl GET /a1-p/policytypes 200

echo "=== API: Load a policy type: 1 ==="
RESULT=""
do_curl PUT /a1-p/policytypes/1 201 jsonfiles/pt1.json

echo "=== API: Get policy type ids, shall contain type 1 =="
RESULT="json:[ 1 ]"
do_curl GET /a1-p/policytypes 200

echo "=== API: Get instances for type 1, shall be empty ==="
RESULT="json:[]"
do_curl GET '/a1-p/policytypes/1/policies' 200

echo "=== API: Create policy instance pi1 of type: 1 ==="
RESULT=""
# res=$(cat jsonfiles/pi1.json)
# RESULT="json:$res"
do_curl PUT '/a1-p/policytypes/1/policies/pi1' 202 jsonfiles/pi1.json

echo "=== API: Update policy instance pi1 of type: 1 ==="
RESULT=""
do_curl PUT '/a1-p/policytypes/1/policies/pi1' 202 jsonfiles/pi1.json
# res=$(cat jsonfiles/pi1.json)
# RESULT="json:$res"
# do_curl PUT '/a1-p/policytypes/1/policies/pi1' 200 jsonfiles/pi1.json

echo "=== API: Load a policy type: 1, shall fail ==="
RESULT=""
do_curl PUT /a1-p/policytypes/1 400 jsonfiles/pt1.json

echo "=== API: Get instances for type 1, shall contain pi1 ==="
RESULT="json:[ \"pi1\" ]"
do_curl GET '/a1-p/policytypes/1/policies' 200

if [ $DUP_CHECK == 1 ]; then
    echo "=== API: Create policy instance pi2 (copy of pi1) of type: 1. Shall fail ==="
    RESULT=""
    do_curl PUT '/a1-p/policytypes/1/policies/pi2' 400 jsonfiles/pi1.json
else
    echo "=== API: Create policy instance pi2 (copy of pi1) of type: 1. Shall succeed ==="
    RESULT=""
    do_curl PUT '/a1-p/policytypes/1/policies/pi2' 202 jsonfiles/pi1.json
    # res=$(cat jsonfiles/pi1.json)
    # RESULT="json:$res"
    # do_curl PUT '/a1-p/policytypes/1/policies/pi2' 200 jsonfiles/pi1.json

    echo "=== Delete policy instance: pi2 ==="
    RESULT=""
    do_curl DELETE '/a1-p/policytypes/1/policies/pi2' 202
fi

echo "=== Set force response code 401. ==="
RESULT="*"
do_curl POST '/forceresponse?code=401' 200

echo "=== API: Get policy type 1. Shall fail with forced code ==="
RESULT=""
do_curl GET '/a1-p/policytypes/1' 401

echo "=== API: Get policy status ==="
RESULT="json:{\"enforceStatus\": \"NOT_ENFORCED\", \"enforceReason\": \"OTHER_REASON\"}"
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 200

echo "=== Load a policy type: 2 ==="
RESULT="Policy type 2 is OK."
do_curl PUT '/policytype?id=2' 201 jsonfiles/pt2.json

echo "=== Load a policy type: 2 again. ==="
RESULT="Policy type 2 is OK."
do_curl PUT '/policytype?id=2' 200 jsonfiles/pt2.json

echo "=== API: Get policy type ids, shall contain type 1 and 2 =="
RESULT="json:[ 1, 2 ]"
do_curl GET /a1-p/policytypes 200

echo "=== Get policy type ids, shall contain type 1 and 2 =="
RESULT="json:[\"1\", \"2\"]"
do_curl GET /policytypes 200

echo "=== API: Get policy type 2 =="
RESULT="json:{\"name\": \"pt2\", \"description\": \"pt2 policy type\", \"policy_type_id\": 2, \"create_schema\": {\"\$schema\": \"http://json-schema.org/draft-07/schema#\", \"title\": \"STD_QoSNudging_0.2.0\", \"description\": \"QoS policy type\", \"type\": \"object\", \"properties\": {\"scope\": {\"type\": \"object\", \"properties\": {\"ueId\": {\"type\": \"string\"}, \"qosId\": {\"type\": \"string\"}}, \"additionalProperties\": false, \"required\": [\"ueId\", \"qosId\"]}, \"statement\": {\"type\": \"object\", \"properties\": {\"priorityLevel\": {\"type\": \"number\"}}, \"additionalProperties\": false, \"required\": [\"priorityLevel\"]}}}}"
do_curl GET /a1-p/policytypes/2 200

echo "=== Delete policy type: 2 ==="
RESULT=""
do_curl DELETE '/policytype?id=2' 204 jsonfiles/pt2.json

echo "=== API: Get policy type ids, shall contain type 1 =="
RESULT="json:[ 1 ]"
do_curl GET /a1-p/policytypes 200

echo "=== Load a policy type: 2 ==="
RESULT="Policy type 2 is OK."
do_curl PUT '/policytype?id=2' 201 jsonfiles/pt2.json

echo "=== API: Get policy type 2 =="
RESULT="json:{\"name\": \"pt2\", \"description\": \"pt2 policy type\", \"policy_type_id\": 2, \"create_schema\": {\"\$schema\": \"http://json-schema.org/draft-07/schema#\", \"title\": \"STD_QoSNudging_0.2.0\", \"description\": \"QoS policy type\", \"type\": \"object\", \"properties\": {\"scope\": {\"type\": \"object\", \"properties\": {\"ueId\": {\"type\": \"string\"}, \"qosId\": {\"type\": \"string\"}}, \"additionalProperties\": false, \"required\": [\"ueId\", \"qosId\"]}, \"statement\": {\"type\": \"object\", \"properties\": {\"priorityLevel\": {\"type\": \"number\"}}, \"additionalProperties\": false, \"required\": [\"priorityLevel\"]}}}}"
do_curl GET /a1-p/policytypes/2 200

echo "=== API: Get instances for type 2, shall be empty ==="
RESULT="json:[]"
do_curl GET '/a1-p/policytypes/2/policies' 200

echo "=== API: Create duplicate policy instance id pi1 of type: 2 (pi1 exist for type 1), shall fail==="
RESULT=""
do_curl PUT '/a1-p/policytypes/2/policies/pi1' 400 jsonfiles/pi1.json

echo "=== API: Create policy instance pi2 of type: 2. Missing param, shall fail. ==="
RESULT=""
do_curl PUT '/a1-p/policytypes/2/policies/pi2' 400 jsonfiles/pi2_missing_param.json

echo "=== API: Create policy instance pi2 of type: 2 ==="
RESULT=""
do_curl PUT '/a1-p/policytypes/2/policies/pi2' 202 jsonfiles/pi2.json
# res=$(cat jsonfiles/pi2.json)
# RESULT="json:$res"
# do_curl PUT '/a1-p/policytypes/2/policies/pi2' 200 jsonfiles/pi2.json

echo "=== API: Update policy instance pi2 of type: 2 ==="
RESULT=""
do_curl PUT '/a1-p/policytypes/2/policies/pi2' 202 jsonfiles/pi2.json

echo "=== API: Update policy instance pi2 of type: 2 ==="
RESULT=""
do_curl PUT "/a1-p/policytypes/2/policies/pi2?notificationDestination=http://localhost:${PORT}/statustest" 202 jsonfiles/pi2.json

echo "=== Send status for pi2==="
RESULT="OK"
do_curl POST '/sendstatus?policyid=pi2' 201 jsonfiles/pi2.json

echo "=== API: Get instances for type 1, shall contain pi1 ==="
RESULT="json:[ \"pi1\" ]"
do_curl GET '/a1-p/policytypes/1/policies' jsonfiles/200

echo "=== API: Get instances for type 2, shall contain pi2 ==="
RESULT="json:[ \"pi2\" ]"
do_curl GET '/a1-p/policytypes/2/policies' 200

if [ $DUP_CHECK == 1 ]; then
    echo "=== API: Create policy instance pi11 (copy of pi1) of type: 1. Shall fail ==="
    RESULT=""
    do_curl PUT '/a1-p/policytypes/1/policies/pi11' 400 jsonfiles/pi1.json
else
    echo "=== API: Create policy instance pi11 (copy of pi1) of type: 1. Shall succeed ==="
    RESULT=""
    do_curl PUT '/a1-p/policytypes/1/policies/pi11' 202 jsonfiles/pi1.json
    # res=$(cat jsonfiles/pi1.json)
    # RESULT="json:$res"
    # do_curl PUT '/a1-p/policytypes/1/policies/pi11' 200 jsonfiles/pi1.json

    echo "=== Delete policy instance: pi11 ==="
    RESULT=""
    do_curl DELETE '/a1-p/policytypes/1/policies/pi11' 202
fi

if [ $DUP_CHECK == 1 ]; then
    echo "=== API: Create policy instance pi3 (copy of pi1) of type: 2. Shall fail ==="
    RESULT=""
    do_curl PUT '/a1-p/policytypes/1/policies/pi3' 400 jsonfiles/pi1.json
else
    echo "=== API: Create policy instance pi3 (copy of pi1) of type: 1. Shall succeed ==="
    RESULT=""
    do_curl PUT '/a1-p/policytypes/1/policies/pi3' 202 jsonfiles/pi1.json
    # res=$(cat jsonfiles/pi1.json)
    # RESULT="json:$res"
    # do_curl PUT '/a1-p/policytypes/1/policies/pi3' 200 jsonfiles/pi1.json

    echo "=== Delete policy instance: pi3 ==="
    RESULT=""
    do_curl DELETE '/a1-p/policytypes/1/policies/pi3' 202
fi

echo "=== API: Get instances for type 1, shall contain pi1 ==="
RESULT="json:[ \"pi1\" ]"
do_curl GET '/a1-p/policytypes/1/policies' jsonfiles/200

echo "=== API: Get instances for type 2, shall contain pi2 ==="
RESULT="json:[ \"pi2\" ]"
do_curl GET '/a1-p/policytypes/2/policies' 200

echo "=== Set force response code 401. ==="
RESULT="*"
do_curl POST '/forceresponse?code=401' 200

echo "=== API: Get policy status for pi1, shall fail ==="
RESULT=""
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 401

echo "=== Set force delay 10. ==="
RESULT="Force delay: 10 sec set for all A1 responses"
do_curl POST '/forcedelay?delay=10' 200

echo "=== API: Get policy status for pi1. Shall delay 10 sec ==="
RESULT="json:{\"enforceStatus\": \"NOT_ENFORCED\", \"enforceReason\": \"OTHER_REASON\"}"
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 200

echo "=== Reset force delay. ==="
RESULT="Force delay: None sec set for all A1 responses"
do_curl POST '/forcedelay' 200

echo "=== Set status for pi1 ==="
RESULT="Status set to ENFORCED for policy: pi1"
do_curl PUT '/status?policyid=pi1&status=ENFORCED' 200

echo "=== API: Get policy status for pi1 ==="
RESULT="json:{\"enforceStatus\": \"ENFORCED\", \"enforceReason\": null}"
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 200

echo "=== Set status for pi1 ==="
RESULT="Status set to ENFORCED for policy: pi1"
do_curl PUT '/status?policyid=pi1&status=ENFORCED' 200

echo "=== API: Get policy status for pi1 ==="
RESULT="json:{\"enforceStatus\": \"ENFORCED\", \"enforceReason\": null}"
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 200

echo "=== Get counter: instances ==="
RESULT="2"
do_curl GET '/counter/num_instances' 200

echo "=== Get counter: types ==="
RESULT="2"
do_curl GET '/counter/num_types' 200

echo "=== Get counter: interface ==="
RESULT="OSC_2.1.0"
do_curl GET '/counter/interface' 200

echo "=== Get counter: remote hosts ==="
RESULT="*"
do_curl GET '/counter/remote_hosts' 200

echo "=== DELETE policy pi1 ==="
RESULT=""
do_curl DELETE /a1-p/policytypes/1/policies/pi1 202

echo "=== API: Get instances for type 1, shall be empty ==="
RESULT="[]"
do_curl GET /a1-p/policytypes/1/policies 200

echo "=== API: Get instances for type 2, shall contain pi2 ==="
RESULT="json:[ \"pi2\" ]"
do_curl GET /a1-p/policytypes/2/policies 200

echo "=== Get counter: instances ==="
RESULT="1"
do_curl GET /counter/num_instances 200

echo "=== Get counter: datadelivery ==="
RESULT="0"
do_curl GET /counter/datadelivery 200

echo "********************"
echo "*** All tests ok ***"
echo "********************"
