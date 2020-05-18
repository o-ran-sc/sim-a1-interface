#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2020 Nordix Foundation. All rights reserved.
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
# Run the build_and_start with the same arg as this script
if [ $# -ne 1 ]; then
    echo "Usage: ./basic_test.sh nonsecure|secure"
    exit 1
fi
if [ "$1" != "nonsecure" ] && [ "$1" != "secure" ]; then
    echo "Usage: ./basic_test.sh nonsecure|secure"
    exit 1
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
RESULT="Current interface: STD_1.1.3 All supported A1 interface yamls in this container: ['1.1.x-alpha.2', 'OSC_2.1.0', 'STD_1.1.3']"
do_curl GET /container_interfaces 200

echo "=== Reset simulator instances ==="
RESULT="All policy instances deleted"
do_curl POST /deleteinstances 200

echo "=== Reset simulator, all ==="
RESULT="All policy instances deleted"
do_curl POST /deleteall 200

echo "=== API: Get policy instances, shall be empty=="
RESULT="json:[]"
do_curl GET /A1-P/v1/policies 200

echo "=== API: Create policy instance pi1 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT /A1-P/v1/policies/pi1 201 jsonfiles/pi1.json

echo "=== API: Update policy instance pi1 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 6}}"
do_curl PUT /A1-P/v1/policies/pi1 200 jsonfiles/pi1_updated.json

echo "=== API: Get policy instances, shall contain pi1=="
RESULT="json:[ \"pi1\" ]"
do_curl GET /A1-P/v1/policies 200

echo "=== API: Create policy instance pi2 (copy of pi1). Shall fail ==="
RESULT="json:{\"title\": \"The policy json already exists.\", \"status\": 400, \"instance\": \"pi2\"}"
do_curl PUT /A1-P/v1/policies/pi2 400 jsonfiles/pi1_updated.json

echo "=== Set force response code 409. ==="
RESULT="*"
do_curl POST '/forceresponse?code=409' 200

echo "=== API: Get policy instances, shall fail =="
RESULT="json:{\"title\": \"Conflict\", \"status\": 409, \"detail\": \"Request could not be processed in the current state of the resource\"}"
do_curl GET /A1-P/v1/policies 409

echo "=== API: Get policy status ==="
RESULT="json:{\"enforceStatus\": \"UNDEFINED\"}"
do_curl GET /A1-P/v1/policies/pi1/status 200

echo "=== API: Create policy instance pi2 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue2\", \"groupId\": \"group2\", \"sliceId\": \"slice2\", \"qosId\": \"qos2\", \"cellId\": \"cell2\"}, \"statement\": {\"priorityLevel\": 10}}"
do_curl PUT /A1-P/v1/policies/pi2 201 jsonfiles/pi2.json

echo "=== API: Update policy instance pi2 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue2\", \"groupId\": \"group2\", \"sliceId\": \"slice2\", \"qosId\": \"qos2\", \"cellId\": \"cell2\"}, \"statement\": {\"priorityLevel\": 10}}"
do_curl PUT '/A1-P/v1/policies/pi2?notificationDestination=http://localhost:2223/statustest' 200 jsonfiles/pi2.json

echo "=== API: Get policy instances, shall contain pi1 and pi2=="
RESULT="json:[ \"pi1\", \"pi2\" ]"
do_curl GET /A1-P/v1/policies 200

echo "=== Set force delay 10. ==="
RESULT="Force delay: 10 sec set for all A1 responses"
do_curl POST '/forcedelay?delay=10' 200

echo "=== API: Get policy instances, shall contain pi1 and pi2 and delayed 10 sec=="
RESULT="json:[ \"pi1\", \"pi2\" ]"
do_curl GET /A1-P/v1/policies 200

echo "=== Reset force delay. ==="
RESULT="Force delay: None sec set for all A1 responses"
do_curl POST /forcedelay 200

echo "=== API: GET policy instance pi1 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 6}}"
do_curl GET /A1-P/v1/policies/pi1 200

echo "=== API: GET policy instance pi2 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue2\", \"groupId\": \"group2\", \"sliceId\": \"slice2\", \"qosId\": \"qos2\", \"cellId\": \"cell2\"}, \"statement\": {\"priorityLevel\": 10}}"
do_curl GET /A1-P/v1/policies/pi2 200

echo "=== API: DELETE policy instance pi1 ==="
RESULT=""
do_curl DELETE /A1-P/v1/policies/pi1 204

echo "=== API: Get policy status for pi1, shall fail==="
RESULT="json:{\"title\": \"The policy identity does not exist.\", \"status\": 404, \"detail\": \"There is no existing policy instance with the identity: pi1\", \"instance\": \"pi1\"}"
do_curl GET /A1-P/v1/policies/pi1/status 404

echo "=== Set status for policy instance pi2 ==="
RESULT="Status set to OK for policy: pi2"
do_curl PUT '/status?policyid=pi2&status=OK' 200

echo "=== API: Get policy status for pi2==="
RESULT="json:{\"enforceStatus\": \"OK\"}"
do_curl GET /A1-P/v1/policies/pi2/status 200

echo "=== Set status for policy instance pi2 ==="
RESULT="Status set to NOTOK and notok_reason for policy: pi2"
do_curl PUT '/status?policyid=pi2&status=NOTOK&reason=notok_reason' 200

echo "=== API: Get policy status for pi2 ==="
RESULT="json:{\"enforceStatus\": \"NOTOK\", \"enforceReason\": \"notok_reason\"}"
do_curl GET /A1-P/v1/policies/pi2/status 200

echo "=== Send status for pi2==="
RESULT="json:{\"enforceStatus\": \"NOTOK\", \"enforceReason\": \"notok_reason\"}"
do_curl POST '/sendstatus?policyid=pi2' 200

echo "=== Get counter: intstance ==="
RESULT="1"
do_curl GET /counter/num_instances 200

echo "=== Get counter: types (shall be 0)==="
RESULT="0"
do_curl GET /counter/num_types 200

echo "=== Get counter: interface ==="
RESULT="STD_1.1.3"
do_curl GET /counter/interface 200

echo "=== Get counter: remote hosts ==="
RESULT="*"
do_curl GET '/counter/remote_hosts' 200

echo "********************"
echo "*** All tests ok ***"
echo "********************"
