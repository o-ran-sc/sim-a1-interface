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

#### Hello world and admin functions ###
echo "=== Simulator hello world ==="
RESULT="OK"
do_curl GET / 200

echo "=== Check used and implemented interfaces ==="
RESULT="Current interface: alpha_x All supported A1 interface yamls in this container: ['1.1.x-alpha.2', 'alpha_x', 'STD_1.1.3', 'OSC_2.1.0']"
do_curl GET /container_interfaces 200

echo "=== Reset simulator instances ==="
RESULT="All policy instances deleted"
do_curl POST /deleteinstances 200

echo "=== Reset simulator, all ==="
RESULT="All policy instances and types deleted"
do_curl POST /deleteall 200

### Policy instances and policy types ###
echo "=== API: Get policy instances, shall be empty=="
RESULT="json:[]"
do_curl GET /A1-P/v1/policies 200

echo "=== API: Get policy types, shall be empty=="
RESULT="json:[]"
do_curl GET /A1-P/v1/policytypes 200

echo "=== Put a policy type: without id, shall fail ==="
RESULT="Parameter <id> missing in request"
do_curl PUT /policytype 400 jsonfiles/pt1.json

echo "=== Put a policy type: STD_TEST_0.0.1 ==="
RESULT="Policy type STD_TEST_0.0.1 is OK"
do_curl PUT /policytype?id=STD_TEST_0.0.1 201 jsonfiles/pt1.json

echo "=== Put a policy type: STD_TEST_0.0.1, again ==="
RESULT="Policy type STD_TEST_0.0.1 is OK"
do_curl PUT /policytype?id=STD_TEST_0.0.1 200 jsonfiles/pt1.json

echo "=== API: Get a policy type: STD_TEST_0.0.1 ==="
RESULT="json:"$(<jsonfiles/pt1.json)
do_curl GET /A1-P/v1/policytypes/STD_TEST_0.0.1 200

echo "=== Put a policy type: a json but not a type, shall fail ==="
RESULT="The policy type does not include a policySchema or is corrupt"
do_curl PUT /policytype?id=STD_TEST_0.0.1 400 jsonfiles/pi1.json

echo "=== Put a corrupt policy type: not a type, shall fail ==="
RESULT="The policy type is corrupt or missing"
do_curl PUT /policytype?id=STD_TEST_0.0.1 400 jsonfiles/notajson.json

echo "=== Delete a policy type: without id, shall fail ==="
RESULT="Parameter <id> missing in request"
do_curl DELETE /policytype 400

echo "=== Delete a policy type: test1 fail ==="
RESULT="Policy type test1 not found"
do_curl DELETE /policytype?id=test1 404

echo "=== Delete a policy type: STD_TEST_0.0.1 ==="
RESULT=""
do_curl DELETE /policytype?id=STD_TEST_0.0.1 204

echo "=== Put a policy type: STD_TEST_0.0.1 ==="
RESULT="Policy type STD_TEST_0.0.1 is OK"
do_curl PUT /policytype?id=STD_TEST_0.0.1 201 jsonfiles/pt1.json

echo "=== Put a policy type: STD_TEST2_0.0.1 ==="
RESULT="Policy type STD_TEST2_0.0.1 is OK"
do_curl PUT /policytype?id=STD_TEST2_0.0.1 201 jsonfiles/pt2.json

echo "=== Put a policy type: STD_TEST3_0.0.1 ==="
RESULT="Policy type STD_TEST3_0.0.1 is OK"
do_curl PUT /policytype?id=STD_TEST3_0.0.1 201 jsonfiles/pt3_nostatus.json

echo "=== API: Get policy type ids=="
RESULT="json:[ \"STD_TEST_0.0.1\", \"STD_TEST2_0.0.1\",\"STD_TEST3_0.0.1\" ]"
do_curl GET /A1-P/v1/policytypes 200

### Delayed and forced error responses
echo "=== Set force response code 409. ==="
RESULT="*"
do_curl POST '/forceresponse?code=409' 200

echo "=== API: Get policy type ids, shall fail with 409=="
RESULT="json:{\"title\": \"Conflict\", \"status\": 409, \"detail\": \"Request could not be processed in the current state of the resource\"}"
do_curl GET /A1-P/v1/policytypes 409

echo "=== Set force delay 10. ==="
RESULT="Force delay: 10 sec set for all A1 responses"
do_curl POST '/forcedelay?delay=10' 200

echo "=== API: Get policy types, shall be delayed 10 sec=="
RESULT="json:[ \"STD_TEST_0.0.1\", \"STD_TEST2_0.0.1\", \"STD_TEST3_0.0.1\" ]"
do_curl GET /A1-P/v1/policytypes 200

echo "=== Reset force delay. ==="
RESULT="Force delay: None sec set for all A1 responses"
do_curl POST /forcedelay 200

### Create and update policies
echo "=== API: Get policy instances, shall be empty=="
RESULT="json:[]"
do_curl GET /A1-P/v1/policies 200

echo "=== API: Get policy instances, shall be empty=="
RESULT="json:[]"
do_curl GET /A1-P/v1/policies?policyTypeId=test1 200

echo "=== API: Get policy instances of type: STD_TEST_0.0.1  , shall be empty=="
RESULT="json:[]"
do_curl GET /A1-P/v1/policies?policyTypeId=STD_TEST_0.0.1 200

echo "=== API: Create policy instance 100, no json payload, shall fail ==="
RESULT="*"
do_curl PUT /A1-P/v1/policies/100 400

echo "=== API: Create policy instance 100, bad json payload, shall fail ==="
RESULT="*"
do_curl PUT /A1-P/v1/policies/100 400 notajson.json

echo "=== API: Create policy instance pi4 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT /A1-P/v1/policies/pi4 201 jsonfiles/pi4.json

echo "=== API: Update policy instance pi4 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT /A1-P/v1/policies/pi4 200 jsonfiles/pi4.json

echo "=== API: Delete policy instance pi4 ==="
RESULT=""
do_curl DELETE /A1-P/v1/policies/pi4 204

echo "=== API: Create policy instance pi4 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT /A1-P/v1/policies/pi4 201 jsonfiles/pi4.json

echo "=== API: Create policy instance pi5, duplicate of pi4 ==="
RESULT="json:{\"title\": \"The policy json already exists.\", \"status\": 400, \"instance\": \"pi5\"}"
do_curl PUT /A1-P/v1/policies/pi5 400 jsonfiles/pi4.json

echo "=== API: Update policy instance pi4, new value ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 6}}"
do_curl PUT /A1-P/v1/policies/pi4 200 jsonfiles/pi4_updated.json

echo "=== API: Update policy instance pi4 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT /A1-P/v1/policies/pi4 200 jsonfiles/pi4.json

echo "=== API: Create policy instance pi1, policy type not found ==="
RESULT="{\"title\": \"The policy type does not exist.\", \"status\": 404, \"instance\": \"STD_TEST\"}"
do_curl PUT /A1-P/v1/policies/pi1?policyTypeId=STD_TEST 404 jsonfiles/pi1.json

echo "=== API: Create policy instance pi1, policy corrupt ==="
RESULT="*"
do_curl PUT /A1-P/v1/policies/pi1?policyTypeId=STD_TEST_0.0.1 400 jsonfiles/notajson.json

echo "=== API: Create policy instance pi1, validation fails ==="
RESULT="{\"title\": \"The policy does not validate towards the policy type schema.\", \"status\": 400, \"instance\": \"pi1\"}"
do_curl PUT /A1-P/v1/policies/pi1?policyTypeId=STD_TEST_0.0.1 400 jsonfiles/pi4.json

echo "=== API: Create policy instance pi1, type STD_TEST_0.0.1 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"qosId\": \"qos1\"}, \"qosObjectives\": {\"priorityLevel\": 5}}"
do_curl PUT /A1-P/v1/policies/pi1?policyTypeId=STD_TEST_0.0.1 201 jsonfiles/pi1.json

echo "=== API: Update policy instance pi1, type STD_TEST_0.0.1 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"qosId\": \"qos1\"}, \"qosObjectives\": {\"priorityLevel\": 5}}"
do_curl PUT /A1-P/v1/policies/pi1?policyTypeId=STD_TEST_0.0.1 200 jsonfiles/pi1.json

echo "=== API: Update policy instance pi1, new type STD_TEST2_0.0.1 ==="
RESULT="{\"title\": \"The policy does not validate towards the policy type schema.\", \"status\": 400, \"instance\": \"pi1\"}"
do_curl PUT /A1-P/v1/policies/pi1?policyTypeId=STD_TEST2_0.0.1 400 jsonfiles/pi1.json

echo "=== API: Create policy instance pi2, type STD_TEST2_0.0.1 ==="
RESULT="json:{\"scope\": {\"sliceId\": \"slice2\", \"qosId\": \"qos2\"}, \"qosObjectives\": {\"bitrate\": 10}}"
do_curl PUT /A1-P/v1/policies/pi2?policyTypeId=STD_TEST2_0.0.1 201 jsonfiles/pi2.json

echo "=== API: Get policy instance pi2 ==="
RESULT="json:{\"scope\": {\"sliceId\": \"slice2\", \"qosId\": \"qos2\"}, \"qosObjectives\": {\"bitrate\": 10}}"
do_curl GET /A1-P/v1/policies/pi2 200

echo "=== API: GET policy instance pi4 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl GET /A1-P/v1/policies/pi4 200

echo "=== API: Update policy instance pi4 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT /A1-P/v1/policies/pi4 200 jsonfiles/pi4.json

echo "=== API: Create policy instance pi5, duplicate of pi4 ==="
RESULT="json:{\"title\": \"The policy json already exists.\", \"status\": 400, \"instance\": \"pi5\"}"
do_curl PUT /A1-P/v1/policies/pi5 400 jsonfiles/pi4.json

echo "=== Delete a policy type: STD_TEST2_0.0.1 having instances, shall fail ==="
RESULT="The policy type exists but instances exists"
do_curl DELETE /policytype?id=STD_TEST2_0.0.1 400

echo "=== Put a policy type: STD_TEST_0.0.1 having instaces, shall fail==="
RESULT="The policy type already exists and instances exists"
do_curl PUT /policytype?id=STD_TEST_0.0.1 400 jsonfiles/pt1.json

### Status handling ###
echo "=== API: Get policy status pi4 (notype)==="
RESULT="json:{\"enforceStatus\": \"UNDEFINED\"}"
do_curl GET /A1-P/v1/policies/pi4/status 200

echo "=== API: Update policy instance pi4 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"groupId\": \"group1\", \"sliceId\": \"slice1\", \"qosId\": \"qos1\", \"cellId\": \"cell1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT '/A1-P/v1/policies/pi4?notificationDestination='$HTTPX'://localhost:'$PORT'/statustest' 200 jsonfiles/pi4.json

echo "=== Send status for pi4 (notype)==="
RESULT="json:{\"enforceStatus\": \"UNDEFINED\"}"
do_curl POST '/sendstatus?policyid=pi4' 200

echo "=== Set status for policy instance pi4 ==="
RESULT="Status set to NOTOK for policy: pi4"
do_curl PUT '/status?policyid=pi4&status=NOTOK' 200

echo "=== API: Get policy status pi4 (notype)==="
RESULT="json:{\"enforceStatus\": \"NOTOK\"}"
do_curl GET /A1-P/v1/policies/pi4/status 200

echo "=== Send status for pi4 (notype)==="
RESULT="json:{\"enforceStatus\": \"NOTOK\"}"
do_curl POST '/sendstatus?policyid=pi4' 200

echo "=== Set status for policy instance pi4 ==="
RESULT="Status set to NOTOK and notok_reason for policy: pi4"
do_curl PUT '/status?policyid=pi4&status=NOTOK&reason=notok_reason' 200

echo "=== API: Get policy status pi4 (notype)==="
RESULT="json:{\"enforceStatus\": \"NOTOK\", \"enforceReason\": \"notok_reason\"}"
do_curl GET /A1-P/v1/policies/pi4/status 200

echo "=== Send status for pi4 (notype)==="
RESULT="json:{\"enforceStatus\": \"NOTOK\", \"enforceReason\": \"notok_reason\"}"
do_curl POST '/sendstatus?policyid=pi4' 200

echo "=== Set status for pi4 (notype) with json, ignoring json==="
RESULT="Status set to NOTOK for policy: pi4"
do_curl PUT '/status?policyid=pi4&status=NOTOK' 200 jsonfiles/pi1_status1.json

echo "=== Send status for pi4 (notype)==="
RESULT="json:{\"enforceStatus\": \"NOTOK\"}"
do_curl POST '/sendstatus?policyid=pi4' 200

echo "=== API: Get policy status pi1 (STD_TEST_0.0.1) no status set, will fail==="
RESULT="json:{\"title\": \"The policy status is not set.\", \"status\": 400, \"detail\": \"The policy exists but has not status set\", \"instance\": \"pi1\"}"
do_curl GET /A1-P/v1/policies/pi1/status 400

echo "=== API: Update policy instance pi1, type STD_TEST_0.0.1 ==="
RESULT="json:{\"scope\": {\"ueId\": \"ue1\", \"qosId\": \"qos1\"}, \"qosObjectives\": {\"priorityLevel\": 5}}"
do_curl PUT '/A1-P/v1/policies/pi1?policyTypeId=STD_TEST_0.0.1&notificationDestination='$HTTPX'://localhost:'$PORT'/statustest' 200 jsonfiles/pi1.json

echo "=== Set status for pi1 (STD_TEST_0.0.1) with json==="
RESULT="Status set to: {\"status\": {\"policystatus\": \"ENFORCED\"}} for policy pi1"
do_curl PUT '/status?policyid=pi1' 200 jsonfiles/pi1_status1.json

echo "=== API: Get policy status pi1 ==="
RESULT="json:{\"status\": {\"policystatus\": \"ENFORCED\"}}"
do_curl GET /A1-P/v1/policies/pi1/status 200

echo "=== Send status for pi1==="
RESULT="json:{\"status\": {\"policystatus\": \"ENFORCED\"}}"
do_curl POST '/sendstatus?policyid=pi1' 200

echo "=== Set status for pi1 (STD_TEST_0.0.1) with json==="
RESULT="Status set to: {\"status\": {\"policystatus\": \"TRAFFIC\", \"reason\": \"active\"}} for policy pi1"
do_curl PUT '/status?policyid=pi1' 200 jsonfiles/pi1_status2.json

echo "=== API: Get policy status pi1 ==="
RESULT="json:{\"status\": {\"policystatus\": \"TRAFFIC\", \"reason\": \"active\"}}"
do_curl GET /A1-P/v1/policies/pi1/status 200

echo "=== Send status for pi1==="
RESULT="json:{\"status\": {\"policystatus\": \"TRAFFIC\", \"reason\": \"active\"}}"
do_curl POST '/sendstatus?policyid=pi1' 200

echo "=== API: Create policy instance pi3 ==="
RESULT="json:{\"scope\": {\"cellId\": \"cell3\", \"qosId\": \"qos3\"}, \"qosObjectives\": {\"bitrate\": 10}}"
do_curl PUT '/A1-P/v1/policies/pi3?policyTypeId=STD_TEST3_0.0.1&notificationDestination='$HTTPX'://localhost:'$PORT'/statustest' 201 jsonfiles/pi3.json

echo "=== Set status for policy instance pi3, shall fail since no status schema ==="
RESULT="Policy has not status schema defined. Not possible to set status"
do_curl PUT '/status?policyid=pi3' 400

echo "=== Delete a policy type: STD_TEST_0.0.1 has instances, shall fail==="
RESULT="The policy type exists but instances exists"
do_curl DELETE /policytype?id=STD_TEST_0.0.1 400

echo "=== Put a policy type: STD_TEST_0.0.1, has instances, shall fail==="
RESULT="The policy type already exists and instances exists"
do_curl PUT /policytype?id=STD_TEST_0.0.1 400 jsonfiles/pt1.json

### Duplicate check - duplicated policies allowed if different types
echo "=== Put a policy type: STD_TEST5_0.0.1 ==="
RESULT="Policy type STD_TEST5_0.0.1 is OK"
do_curl PUT /policytype?id=STD_TEST5_0.0.1 201 jsonfiles/pt5.json

echo "=== API: Create policy instance pi5, type STD_TEST5_0.0.1 ==="
RESULT="json:{\"scope\": {\"sliceId\": \"slice2\", \"qosId\": \"qos2\"}, \"qosObjectives\": {\"bitrate\": 10}}"
do_curl PUT /A1-P/v1/policies/pi5?policyTypeId=STD_TEST5_0.0.1 201 jsonfiles/pi5.json

echo "=== API: Get policy instances =="
RESULT="json:[ \"pi1\", \"pi2\", \"pi3\", \"pi4\", \"pi5\" ]"
do_curl GET /A1-P/v1/policies 200

### Counter/metrics readout
echo "=== Get counter: intstance ==="
RESULT="5"
do_curl GET /counter/num_instances 200

echo "=== API: Delete a policy : pi4 ==="
RESULT=""
do_curl DELETE /A1-P/v1/policies/pi4 204

echo "=== API: Get policy instances =="
RESULT="json:[ \"pi1\", \"pi2\", \"pi3\", \"pi5\" ]"
do_curl GET /A1-P/v1/policies 200

echo "=== Get counter: intstance ==="
RESULT="4"
do_curl GET /counter/num_instances 200

echo "=== Get counter: types ==="
RESULT="4"
do_curl GET /counter/num_types 200

echo "=== API: Delete a policy : pi5 ==="
RESULT=""
do_curl DELETE /A1-P/v1/policies/pi5 204

echo "=== API: Get policy type ids=="
RESULT="json:[ \"STD_TEST_0.0.1\", \"STD_TEST2_0.0.1\",\"STD_TEST3_0.0.1\" ,\"STD_TEST5_0.0.1\"]"
do_curl GET /A1-P/v1/policytypes 200

echo "=== Delete a policy type: STD_TEST5_0.0.1 ==="
RESULT=""
do_curl DELETE /policytype?id=STD_TEST5_0.0.1 204

echo "=== API: Get policy type ids=="
RESULT="json:[ \"STD_TEST_0.0.1\", \"STD_TEST2_0.0.1\",\"STD_TEST3_0.0.1\" ]"
do_curl GET /A1-P/v1/policytypes 200

echo "=== Get counter: types ==="
RESULT="3"
do_curl GET /counter/num_types 200

echo "=== Get counter: interface ==="
RESULT="alpha_x"
do_curl GET /counter/interface 200

echo "=== Get counter: remote hosts ==="
RESULT="*"
do_curl GET '/counter/remote_hosts' 200

echo "********************"
echo "*** All tests ok ***"
echo "********************"
