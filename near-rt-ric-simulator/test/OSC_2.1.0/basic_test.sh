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

#Default port for the simulator
PORT=8085

. ../common/test_common.sh

echo "=== Simulator hello world ==="
RESULT="OK"
do_curl GET / 200

echo "=== Check used and implemented interfaces ==="
RESULT="*"
do_curl GET /container_interfaces 200

echo "=== Reset simulator instances ==="
RESULT="All policy instances deleted"
do_curl POST /deleteinstances 200

echo "=== Reset simulator, all ==="
RESULT="All policy instances and types deleted"
do_curl POST /deleteall 200

echo "=== API: Healthcheck ==="
RESULT=""
do_curl get /a1-p/healthcheck 200

echo "=== API: Get policy types, shall be empty =="
RESULT="[]"
do_curl GET /a1-p/policytypes 200

echo "=== API: Delete a policy type, shall fail =="
RESULT="{\"type\": \"about:blank\", \"title\": \"The policy type does not exist.\", \"status\": 404, \"instance\": \"1\"}"
do_curl DELETE /a1-p/policytypes/1 404

echo "=== API: Get policy instances for type 1, shall fail =="
RESULT="{\"type\": \"about:blank\", \"title\": \"The policy type does not exist.\", \"status\": 404, \"instance\": \"1\"}"
do_curl GET /a1-p/policytypes/1/policies 404

echo "=== API: Load a policy type: 1 ==="
RESULT="{\"name\": \"pt1\", \"description\": \"pt1 policy type\", \"policy_type_id\": 1, \"create_schema\": {\"\$schema\": \"http://json-schema.org/draft-07/schema#\", \"title\": \"STD_QoSNudging_0.2.0\", \"description\": \"QoS policy type\", \"type\": \"object\", \"properties\": {\"scope\": {\"type\": \"object\", \"properties\": {\"ueId\": {\"type\": \"string\"}, \"qosId\": {\"type\": \"string\"}}, \"additionalProperties\": false, \"required\": [\"ueId\", \"qosId\"]}, \"statement\": {\"type\": \"object\", \"properties\": {\"priorityLevel\": {\"type\": \"number\"}}, \"additionalProperties\": false, \"required\": [\"priorityLevel\"]}}}}"
do_curl PUT /a1-p/policytypes/1 201 jsonfiles/pt1.json

echo "=== API: Load a policy type: 1, again ==="
RESULT="{\"name\": \"pt1\", \"description\": \"pt1 policy type\", \"policy_type_id\": 1, \"create_schema\": {\"\$schema\": \"http://json-schema.org/draft-07/schema#\", \"title\": \"STD_QoSNudging_0.2.0\", \"description\": \"QoS policy type\", \"type\": \"object\", \"properties\": {\"scope\": {\"type\": \"object\", \"properties\": {\"ueId\": {\"type\": \"string\"}, \"qosId\": {\"type\": \"string\"}}, \"additionalProperties\": false, \"required\": [\"ueId\", \"qosId\"]}, \"statement\": {\"type\": \"object\", \"properties\": {\"priorityLevel\": {\"type\": \"number\"}}, \"additionalProperties\": false, \"required\": [\"priorityLevel\"]}}}}"
do_curl PUT /a1-p/policytypes/1 200 jsonfiles/pt1.json

echo "=== API: Delete a policy type: 1 ==="
RESULT=""
do_curl DELETE /a1-p/policytypes/1 204

echo "=== API: Get policy type ids, shall be empty =="
RESULT="[]"
do_curl GET /a1-p/policytypes 200

echo "=== API: Load a policy type: 1 ==="
RESULT="{\"name\": \"pt1\", \"description\": \"pt1 policy type\", \"policy_type_id\": 1, \"create_schema\": {\"\$schema\": \"http://json-schema.org/draft-07/schema#\", \"title\": \"STD_QoSNudging_0.2.0\", \"description\": \"QoS policy type\", \"type\": \"object\", \"properties\": {\"scope\": {\"type\": \"object\", \"properties\": {\"ueId\": {\"type\": \"string\"}, \"qosId\": {\"type\": \"string\"}}, \"additionalProperties\": false, \"required\": [\"ueId\", \"qosId\"]}, \"statement\": {\"type\": \"object\", \"properties\": {\"priorityLevel\": {\"type\": \"number\"}}, \"additionalProperties\": false, \"required\": [\"priorityLevel\"]}}}}"
do_curl PUT /a1-p/policytypes/1 201 jsonfiles/pt1.json

echo "=== API: Get policy type ids, shall contain type 1 =="
RESULT="[ \"1\" ]"
do_curl GET /a1-p/policytypes 200

echo "=== API: Get instances for type 1, shall be empty ==="
RESULT="[]"
do_curl GET '/a1-p/policytypes/1/policies' 200

echo "=== API: Create policy instance pi1 of type: 1 ==="
RESULT="{\"scope\": {\"ueId\": \"ue1\", \"qosId\": \"qos1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT '/a1-p/policytypes/1/policies/pi1' 201 jsonfiles/pi1.json

echo "=== API: Update policy instance pi1 of type: 1 ==="
RESULT="{\"scope\": {\"ueId\": \"ue1\", \"qosId\": \"qos1\"}, \"statement\": {\"priorityLevel\": 5}}"
do_curl PUT '/a1-p/policytypes/1/policies/pi1' 200 jsonfiles/pi1.json

echo "=== API: Load a policy type: 1, shall fail ==="
RESULT="{\"type\": \"about:blank\", \"title\": \"The policy type cannot be updated, instances exists.\", \"status\": 400, \"instance\": \"1\"}"
do_curl PUT /a1-p/policytypes/1 400 jsonfiles/pt1.json

echo "=== API: Get instances for type 1, shall contain pi1 ==="
RESULT="[ \"pi1\" ]"
do_curl GET '/a1-p/policytypes/1/policies' 200

echo "=== API: Create policy instance pi2 (copy of pi1) of type: 1. Shall fail ==="
RESULT="{\"type\": \"about:blank\", \"title\": \"The policy json already exists.\", \"status\": 400, \"instance\": \"pi2\"}"
do_curl PUT '/a1-p/policytypes/1/policies/pi2' 400 jsonfiles/pi1.json

echo "=== Set force response code 401. ==="
RESULT="*"
do_curl POST '/forceresponse?code=401' 200

echo "=== API: Get policy type 1. Shall fail with forded code ==="
RESULT="*"  #No check, variable contents in the result
do_curl GET '/a1-p/policytypes/1' 401

echo "=== API: Get policy status ==="
RESULT="*"  #No check, variable contents in the result
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 200

echo "=== Load a policy type: 2 ==="
RESULT="Policy type 2 is OK."
do_curl PUT '/policytype?id=2' 201 jsonfiles/pt1.json

echo "=== Load a policy type: 2 again. ==="
RESULT="Policy type 2 is OK."
do_curl PUT '/policytype?id=2' 200 jsonfiles/pt1.json

echo "=== API: Get policy type ids, shall contain type 1 and 2 =="
RESULT="[ \"1\", \"2\" ]"
do_curl GET /a1-p/policytypes 200

echo "=== Get policy type ids, shall contain type 1 and 2 =="
RESULT="[\"1\", \"2\"]"
do_curl GET /policytypes 200

echo "=== API: Get policy type 2 =="
RESULT="{\"name\": \"pt1\", \"description\": \"pt1 policy type\", \"policy_type_id\": 1, \"create_schema\": {\"\$schema\": \"http://json-schema.org/draft-07/schema#\", \"title\": \"STD_QoSNudging_0.2.0\", \"description\": \"QoS policy type\", \"type\": \"object\", \"properties\": {\"scope\": {\"type\": \"object\", \"properties\": {\"ueId\": {\"type\": \"string\"}, \"qosId\": {\"type\": \"string\"}}, \"additionalProperties\": false, \"required\": [\"ueId\", \"qosId\"]}, \"statement\": {\"type\": \"object\", \"properties\": {\"priorityLevel\": {\"type\": \"number\"}}, \"additionalProperties\": false, \"required\": [\"priorityLevel\"]}}}}"
do_curl GET /a1-p/policytypes/2 200

echo "=== Delete policy type: 2 ==="
RESULT=""
do_curl DELETE '/policytype?id=2' 204 jsonfiles/pt1.json

echo "=== API: Get policy type ids, shall contain type 1 =="
RESULT="[ \"1\" ]"
do_curl GET /a1-p/policytypes 200

echo "=== Load a policy type: 2 ==="
RESULT="Policy type 2 is OK."
do_curl PUT '/policytype?id=2' 201 jsonfiles/pt2.json

echo "=== API: Get policy type 2 =="
RESULT="{\"name\": \"pt1\", \"description\": \"pt1 policy type\", \"policy_type_id\": 1, \"create_schema\": {\"\$schema\": \"http://json-schema.org/draft-07/schema#\", \"title\": \"STD_QoSNudging_0.2.0\", \"description\": \"QoS policy type\", \"type\": \"object\", \"properties\": {\"scope\": {\"type\": \"object\", \"properties\": {\"ueId\": {\"type\": \"string\"}, \"qosId\": {\"type\": \"string\"}}, \"additionalProperties\": false, \"required\": [\"ueId\", \"qosId\"]}, \"statement\": {\"type\": \"object\", \"properties\": {\"priorityLevel\": {\"type\": \"number\"}}, \"additionalProperties\": false, \"required\": [\"priorityLevel\"]}}}}"
do_curl GET /a1-p/policytypes/1 200

echo "=== API: Get instances for type 2, shall be empty ==="
RESULT="[]"
do_curl GET '/a1-p/policytypes/2/policies' 200

echo "=== API: Create policy instance pi1 of type: 2, shall fail==="
RESULT="{\"type\": \"about:blank\", \"title\": \"The policy id already exists for other type.\", \"status\": 400, \"instance\": \"pi1\"}"
do_curl PUT '/a1-p/policytypes/2/policies/pi1' 400 jsonfiles/pi1.json

echo "=== API: Create policy instance pi2 of type: 2. Missing param, shall fail. ==="
RESULT="{\"type\": \"about:blank\", \"title\": \"The policy does not match type.\", \"status\": 400, \"instance\": \"pi2\"}"
do_curl PUT '/a1-p/policytypes/2/policies/pi2' 400 jsonfiles/pi2_missing_param.json

echo "=== API: Create policy instance pi2 of type: 2 ==="
RESULT="{\"scope\": {\"ueId\": \"ue2\", \"qosId\": \"qos2\"}, \"statement\": {\"priorityLevel\": 10}}"
do_curl PUT '/a1-p/policytypes/2/policies/pi2' 201 jsonfiles/pi2.json

echo "=== API: Update policy instance pi2 of type: 2 ==="
RESULT="{\"scope\": {\"ueId\": \"ue2\", \"qosId\": \"qos2\"}, \"statement\": {\"priorityLevel\": 10}}"
do_curl PUT '/a1-p/policytypes/2/policies/pi2' 200 jsonfiles/pi2.json

echo "=== API: Get instances for type 1, shall contain pi1 ==="
RESULT="[ \"pi1\" ]"
do_curl GET '/a1-p/policytypes/1/policies' jsonfiles/200

echo "=== API: Get instances for type 2, shall contain pi2 ==="
RESULT="[ \"pi2\" ]"
do_curl GET '/a1-p/policytypes/2/policies' 200

echo "=== API: Create policy instance pi11 (copy of pi1) of type: 1. Shall fail ==="
RESULT="{\"type\": \"about:blank\", \"title\": \"The policy json already exists.\", \"status\": 400, \"instance\": \"pi11\"}"
do_curl PUT '/a1-p/policytypes/1/policies/pi11' 400 jsonfiles/pi1.json

echo "=== Set force response code 401. ==="
RESULT="*"
do_curl POST '/forceresponse?code=401' 200

echo "=== API: Get policy status for pi1, shall fail ==="
RESULT="{\"type\": \"about:blank\", \"title\": \"Not found\", \"status\": \"401\", \"detail\": \"No resource found at the URI\"}"
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 401

echo "=== Set force delay 10. ==="
RESULT="Force delay: 10 sec set for all A1 responses"
do_curl POST '/forcedelay?delay=10' 200

echo "=== API: Get policy status for pi1. Shall delay 10 sec ==="
RESULT="*"
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 200

echo "=== Reset force delay. ==="
RESULT="Force delay: None sec set for all A1 responses"
do_curl POST '/forcedelay' 200

echo "=== Set status for pi1 ==="
RESULT="Status set to IN EFFECT for policy: pi1"
do_curl PUT '/status?policyid=pi1&status=IN%20EFFECT' 200

echo "=== API: Get policy status for pi1 ==="
RESULT="*"  #No check, variable contents in the result
do_curl GET '/a1-p/policytypes/1/policies/pi1/status' 200

echo "=== Get counter: intstance ==="
RESULT="2"
do_curl GET '/counter/num_instances' 200

echo "=== Get counter: types ==="
RESULT="2"
do_curl GET '/counter/num_types' 200

echo "=== Get counter: interface ==="
RESULT="OSC_2.1.0"
do_curl GET '/counter/interface' 200

echo "=== DELETE policy pi1 ==="
RESULT=""
do_curl DELETE /a1-p/policytypes/1/policies/pi1 204

echo "=== API: Get instances for type 1, shall be empty ==="
RESULT="[]"
do_curl GET /a1-p/policytypes/1/policies 200

echo "=== API: Get instances for type 2, shall contain pi2 ==="
RESULT="[ \"pi2\" ]"
do_curl GET /a1-p/policytypes/2/policies 200

echo "=== Get counter: intstance ==="
RESULT="1"
do_curl GET /counter/num_instances 200

echo "********************"
echo "*** All tests ok ***"
echo "********************"
