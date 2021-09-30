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

# This test case test the OSC_2.1.0 version of the simulator

import json

#Version of simulator
INTERFACE_VERSION="OSC_2.1.0"

from unittest_setup import SERVER_URL, setup_env, get_testdata_dir, client

#Setup env and import paths
setup_env(INTERFACE_VERSION)

from compare_json import compare

def test_apis(client):

    testdata=get_testdata_dir()

    # Simulator hello world
    response=client.get(SERVER_URL)
    assert response.status_code == 200

    # Check used and implemented interfaces
    response=client.get(SERVER_URL+'container_interfaces')
    assert response.status_code == 200
    assert response.data ==  b"Current interface: OSC_2.1.0  All supported A1 interface yamls in this container: ['OSC_2.1.0', 'STD_1.1.3', 'STD_2.0.0']"

    # Reset simulator instances
    response=client.post(SERVER_URL+'deleteinstances')
    assert response.status_code == 200

    # Reset simulator, all
    response=client.post(SERVER_URL+'deleteall')
    assert response.status_code == 200

    # API: Healthcheck
    response=client.get(SERVER_URL+'a1-p/healthcheck')
    assert response.status_code == 200

    # API: Get policy types, shall be empty
    data_policytypes_get = [ ]
    response=client.get(SERVER_URL+'a1-p/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policytypes_get, result)
    assert res == True

    # API: Delete a policy type, shall fail
    response=client.delete(SERVER_URL+'a1-p/policytypes/1')
    assert response.status_code == 404

    # API: Get policy instances for type 1, shall fail
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies')
    assert response.status_code == 404

    # Header for json payload
    header = {
        "Content-Type" : "application/json"
    }

    # API: Put a policy type: 1
    with open(testdata+'pt1.json') as json_file:
        policytype_1 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/1', headers=header, data=json.dumps(policytype_1))
        assert response.status_code == 201

    # API: Put a policy type: 1 again
    with open(testdata+'pt1.json') as json_file:
        policytype_1 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/1', headers=header, data=json.dumps(policytype_1))
        assert response.status_code == 201

    # API: Delete a policy type
    response=client.delete(SERVER_URL+'a1-p/policytypes/1')
    assert response.status_code == 204

    # API: Get policy type ids, shall be empty
    data_policytypes_get = [ ]
    response=client.get(SERVER_URL+'a1-p/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policytypes_get, result)
    assert res == True

    # API: Put a policy type: 1
    with open(testdata+'pt1.json') as json_file:
        policytype_1 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/1', headers=header, data=json.dumps(policytype_1))
        assert response.status_code == 201

    # API: Get policy type ids, shall contain '1'
    data_policytypes_get = [ 1 ]
    response=client.get(SERVER_URL+'a1-p/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policytypes_get, result)
    assert res == True

    # API: Get instances for type 1, shall be empty
    data_policies_get = [ ]
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policies_get, result)
    assert res == True

    # API: Create policy instance pi1 of type: 1
    with open(testdata+'pi1.json') as json_file:
        policy_1 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/1/policies/pi1', headers=header, data=json.dumps(policy_1))
        assert response.status_code == 202

    # API: Get policy instance pi1 of type: 1
    with open(testdata+'pi1.json') as json_file:
        policy_1 = json.load(json_file)
        response=client.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1')
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(policy_1, result)
        assert res == True

    # API: Update policy instance pi1 of type: 1
    with open(testdata+'pi1.json') as json_file:
        policy_1 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/1/policies/pi1', headers=header, data=json.dumps(policy_1))
        assert response.status_code == 202

    # API: Update policy type: 1, shall fail
    with open(testdata+'pt1.json') as json_file:
        policytype_1 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/1', headers=header, data=json.dumps(policytype_1))
        assert response.status_code == 400

    # API: Get instances for type 1, shall contain 'pi1'
    data_policies_get = [ "pi1" ]
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policies_get, result)
    assert res == True

    # API: Create policy instance pi2 (copy of pi1) of type: 1.
    with open(testdata+'pi1.json') as json_file:
        policy_2 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/1/policies/pi2', headers=header, data=json.dumps(policy_2))
        assert response.status_code == 202

    # API: DELETE policy instance pi1
    response=client.delete(SERVER_URL+'a1-p/policytypes/1/policies/pi2')
    assert response.status_code == 202

    # Set force response code 401
    response=client.post(SERVER_URL+'forceresponse?code=401')
    assert response.status_code == 200

    # API: Get policy type 1. Shall fail with forced code
    response=client.get(SERVER_URL+'a1-p/policytypes/1')
    assert response.status_code == 401

    # API: Get policy status
    policy_status = {
        "instance_status" : "NOT IN EFFECT",
        "has_been_deleted" : "false",
        "created_at" : "????"
    }
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(policy_status, result)
    assert res == True

    # Load a policy type: 2
    with open(testdata+'pt2.json') as json_file:
        policytype_2 = json.load(json_file)
        response=client.put(SERVER_URL+'policytype?id=2', headers=header, data=json.dumps(policytype_2))
        assert response.status_code == 201
        assert response.data == b"Policy type 2 is OK."

    # Load a policy type: 2, again
    with open(testdata+'pt2.json') as json_file:
        policytype_2 = json.load(json_file)
        response=client.put(SERVER_URL+'policytype?id=2', headers=header, data=json.dumps(policytype_2))
        assert response.status_code == 200
        assert response.data == b"Policy type 2 is OK."

    # API: Get policy type ids, shall contain '1' and '2'
    data_policytypes_get = [ 1,2 ]
    response=client.get(SERVER_URL+'a1-p/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policytypes_get, result)
    assert res == True

    # Get policy type ids, shall contain type 1 and 2 =="
    data_policytypes_get = [ "1","2" ]
    response=client.get(SERVER_URL+'policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policytypes_get, result)
    assert res == True

    # API: Get policy type 2
    with open(testdata+'pt2.json') as json_file:
        policytype_2 = json.load(json_file)
        response=client.get(SERVER_URL+'a1-p/policytypes/2')
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(policytype_2, result)
        assert res == True

    # Delete a policy type
    response=client.delete(SERVER_URL+'policytype?id=2')
    assert response.status_code == 204

    # API: Get policy type ids, shall contain '1'
    data_policytypes_get = [ 1]
    response=client.get(SERVER_URL+'a1-p/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policytypes_get, result)
    assert res == True

    # Load a policy type: 2
    with open(testdata+'pt2.json') as json_file:
        policytype_2 = json.load(json_file)
        response=client.put(SERVER_URL+'policytype?id=2', headers=header, data=json.dumps(policytype_2))
        assert response.status_code == 201
        assert response.data == b"Policy type 2 is OK."

    # API: Get policy type 2
    with open(testdata+'pt2.json') as json_file:
        policytype_2 = json.load(json_file)
        response=client.get(SERVER_URL+'a1-p/policytypes/2')
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(policytype_2, result)
        assert res == True

    # API: Get instances for type 2, shall be empty
    data_policies_get = [ ]
    response=client.get(SERVER_URL+'a1-p/policytypes/2/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policies_get, result)
    assert res == True

    # API: Create policy instance pi1 of type: 2, shall fail
    with open(testdata+'pi1.json') as json_file:
        policy_1 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/2/policies/pi1', headers=header, data=json.dumps(policy_1))
        assert response.status_code == 400

    # API: Create policy instance pi2 of type: 2. Missing param, shall fail
    with open(testdata+'pi2_missing_param.json') as json_file:
        policy_2 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/2/policies/pi2', headers=header, data=json.dumps(policy_2))
        assert response.status_code == 400

    # API: Create policy instance pi2 of type: 2
    with open(testdata+'pi2.json') as json_file:
        policy_2 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/2/policies/pi2', headers=header, data=json.dumps(policy_2))
        assert response.status_code == 202

    with open(testdata+'pi2.json') as json_file:
        policy_2 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/2/policies/pi2', headers=header, data=json.dumps(policy_2))
        assert response.status_code == 202

    # API: Get instances for type 1, shall contain pi1
    data_policies_get = [ "pi1" ]
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policies_get, result)
    assert res == True

    # API: Get instances for type 2, shall contain pi2
    data_policies_get = ["pi2" ]
    response=client.get(SERVER_URL+'a1-p/policytypes/2/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policies_get, result)
    assert res == True

    # Set force response code 409. ==="
    response=client.post(SERVER_URL+'forceresponse?code=401')
    assert response.status_code == 200

    # API: Get policy status for pi1, shall fail
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
    assert response.status_code == 401

    # Set force delay 10
    response=client.post(SERVER_URL+'forcedelay?delay=10')
    assert response.status_code == 200
    assert response.data ==  b"Force delay: 10 sec set for all A1 responses"

    # API: Get policy status for pi1. Shall delay 10 sec
    policy_status = {
        "instance_status" : "NOT IN EFFECT",
        "has_been_deleted" : "false",
        "created_at" : "????"
    }
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(policy_status, result)
    assert res == True

    # Reset force delay
    response=client.post(SERVER_URL+'forcedelay')
    assert response.status_code == 200
    assert response.data ==  b"Force delay: None sec set for all A1 responses"

    #  Set status for pi1
    response=client.put(SERVER_URL+'status?policyid=pi1&status=IN%20EFFECT')
    assert response.status_code == 200

    # API: Get policy status for pi1
    policy_status = {
        "instance_status" : "IN EFFECT",
        "has_been_deleted" : "false",
        "created_at" : "????"
    }
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(policy_status, result)
    assert res == True

    #  Set status for pi1
    response=client.put(SERVER_URL+'status?policyid=pi1&status=IN%20EFFECT&deleted=true&created_at=2020-03-30%2012:00:00')
    assert response.status_code == 200

    # API: Get policy status for pi1
    policy_status = {
        "instance_status" : "IN EFFECT",
        "has_been_deleted" : "true",
        "created_at" : "????"
    }
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(policy_status, result)
    assert res == True

    # Get counter: intstance
    response=client.get(SERVER_URL+'counter/num_instances')
    assert response.status_code == 200
    assert response.data ==  b"2"

    # Get counter: types (shall be 2)
    response=client.get(SERVER_URL+'counter/num_types')
    assert response.status_code == 200
    assert response.data ==  b"2"

    # Get counter: interface
    response=client.get(SERVER_URL+'counter/interface')
    assert response.status_code == 200
    assert response.data == b"OSC_2.1.0"

    # Get counter: remote hosts
    response=client.get(SERVER_URL+'counter/remote_hosts')
    assert response.status_code == 200

    # Get counter: test, shall fail
    response=client.get(SERVER_URL+'counter/test')
    assert response.status_code == 404

    # API: DELETE policy instance pi1
    response=client.delete(SERVER_URL+'a1-p/policytypes/1/policies/pi1')
    assert response.status_code == 202

    # API: Get instances for type 1, shall be empty
    data_policies_get = [ ]
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policies_get, result)
    assert res == True

    # API: Get instances for type 2, shall contain pi2
    data_policies_get = ["pi2" ]
    response=client.get(SERVER_URL+'a1-p/policytypes/2/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policies_get, result)
    assert res == True

    # Get counter: instances
    response=client.get(SERVER_URL+'counter/num_instances')
    assert response.status_code == 200
    assert response.data ==  b"1"


    ### Tests to increase code coverage

    # Set force response code 500
    response=client.post(SERVER_URL+'forceresponse?code=500')
    assert response.status_code == 200

    # API: Healthcheck
    response=client.get(SERVER_URL+'a1-p/healthcheck')
    assert response.status_code == 500

    # Set force response code 501
    response=client.post(SERVER_URL+'forceresponse?code=501')
    assert response.status_code == 200

    # API: Get policy types
    data_policytypes_get = [ ]
    response=client.get(SERVER_URL+'a1-p/policytypes')
    assert response.status_code == 501

    # Set force response code 502
    response=client.post(SERVER_URL+'forceresponse?code=502')
    assert response.status_code == 200

    # API: Delete a policy type, shall fail
    response=client.delete(SERVER_URL+'a1-p/policytypes/55')
    assert response.status_code == 502

    # Set force response code 503. ==="
    response=client.post(SERVER_URL+'forceresponse?code=503')
    assert response.status_code == 200

    with open(testdata+'pi1.json') as json_file:
        policy_1 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/1/policies/pi11', headers=header, data=json.dumps(policy_1))
        assert response.status_code == 503

    # Set force response code 504
    response=client.post(SERVER_URL+'forceresponse?code=504')
    assert response.status_code == 200

    # API: Get instances for type 1, shall fail
    data_policies_get = [ ]
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies')
    assert response.status_code == 504

    # Set force response code 505. ==="
    response=client.post(SERVER_URL+'forceresponse?code=505')
    assert response.status_code == 200

    # API: delete instance pi1, shall fail
    response=client.delete(SERVER_URL+'a1-p/policytypes/1/policies/pi1')
    assert response.status_code == 505

    # API: Delete a policy type having instances, shall fail
    response=client.delete(SERVER_URL+'a1-p/policytypes/2')
    assert response.status_code == 400

    # API: delete instance pi1 in type 5, shall fail
    response=client.delete(SERVER_URL+'a1-p/policytypes/5/policies/pi1')
    assert response.status_code == 404

    # API: delete instance pi99 in type 1, shall fail
    response=client.delete(SERVER_URL+'a1-p/policytypes/1/policies/pi99')
    assert response.status_code == 404

    # API: Create policy instance pi80 of type: 5
    with open(testdata+'pi1.json') as json_file:
        policy_80 = json.load(json_file)
        response=client.put(SERVER_URL+'a1-p/policytypes/5/policies/pi80', headers=header, data=json.dumps(policy_80))
        assert response.status_code == 404

    # API: Get policy type
    data_policytypes_get = [ ]
    response=client.get(SERVER_URL+'a1-p/policytypes/55')
    assert response.status_code == 404

    # API: Get status, bad type - shall fail
    response=client.get(SERVER_URL+'a1-p/policytypes/99/policies/pi1/status')
    assert response.status_code == 404

    # API: Get status, bad instance - shall fail
    response=client.get(SERVER_URL+'a1-p/policytypes/1/policies/pi111/status')
    assert response.status_code == 404

    # Load policy type, no type in url - shall faill
    with open(testdata+'pt2.json') as json_file:
        policytype_2 = json.load(json_file)
        response=client.put(SERVER_URL+'policytype', headers=header, data=json.dumps(policytype_2))
        assert response.status_code == 400

    # Load policy type - duplicatee - shall faill
    with open(testdata+'pt1.json') as json_file:
        policytype_1 = json.load(json_file)
        response=client.put(SERVER_URL+'policytype?id=2', headers=header, data=json.dumps(policytype_1))
        assert response.status_code == 400
