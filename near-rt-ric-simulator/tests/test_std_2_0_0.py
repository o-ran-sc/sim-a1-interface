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

# This test case test the STD_2.0.0 version of the simulator

import json
import time

#Version of simulator
INTERFACE_VERSION="STD_2.0.0"

from unittest_setup import SERVER_URL, HOST_IP, PORT_NUMBER, setup_env, get_testdata_dir, client

#Setup env and import paths
setup_env(INTERFACE_VERSION)

from compare_json import compare

def test_apis(client):

    testdata=get_testdata_dir()

    # Header for json payload
    header = {
        "Content-Type" : "application/json"
    }

    # Simulator hello world
    response=client.get(SERVER_URL)
    assert response.status_code == 200

    # Check used and implemented interfaces
    response=client.get(SERVER_URL+'container_interfaces')
    assert response.status_code == 200
    assert response.data ==  b"Current interface: STD_2.0.0  All supported A1 interface yamls in this container: ['OSC_2.1.0', 'STD_1.1.3', 'STD_2.0.0']"

    # Reset simulator instances
    response=client.post(SERVER_URL+'deleteinstances')
    assert response.status_code == 200

    # Reset simulator, all
    response=client.post(SERVER_URL+'deleteall')
    assert response.status_code == 200

    # Get counter: interface
    response=client.get(SERVER_URL+'counter/interface')
    assert response.status_code == 200
    assert response.data ==  b"STD_2.0.0"

    # Get counter: remote hosts
    response=client.get(SERVER_URL+'counter/remote_hosts')
    assert response.status_code == 200

    # Get counter: intstance
    response=client.get(SERVER_URL+'counter/num_instances')
    assert response.status_code == 200
    assert response.data ==  b"0"

    # Get counter: types
    response=client.get(SERVER_URL+'counter/num_types')
    assert response.status_code == 200
    assert response.data ==  b"0"

    # API: Get policy type, shall be empty
    data_response = [ ]
    response=client.get(SERVER_URL+'A1-P/v2/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # API: Get policy instances for type 1, type not found
    data_response = {"title": "The policy type does not exist.", "status": 404, "instance": "1"}
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/1/policies')
    assert response.status_code == 404
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # API: Get policy instances, type not found
    data_response = {"title": "The policy type does not exist.", "status": 404, "instance": "test"}
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/test/policies')
    assert response.status_code == 404
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # Put a policy type: STD_1
    with open(testdata+'std_1.json') as json_file:
        data_response = b"Policy type STD_1 is OK."
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'policytype?id=STD_1', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 201
        assert data_response == response.data

    # Put a policy type: STD_1, again
    with open(testdata+'std_1.json') as json_file:
        data_response = b"Policy type STD_1 is OK."
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'policytype?id=STD_1', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 200
        assert data_response == response.data

    # API: Get policy type ids, shall contain type STD_1
    data_response = [ "STD_1" ]
    response=client.get(SERVER_URL+'A1-P/v2/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # Delete a policy type: STD_1
    data_response = b""
    response=client.delete(SERVER_URL+'policytype?id=STD_1')
    assert response.status_code == 204
    assert data_response == response.data

    # API: Get policy type ids, shall be empty
    data_response = [  ]
    response=client.get(SERVER_URL+'A1-P/v2/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # Put a policy type: STD_1
    with open(testdata+'std_1.json') as json_file:
        data_response = b"Policy type STD_1 is OK."
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'policytype?id=STD_1', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 201
        assert data_response == response.data

    # API: Get policy type ids, shall contain type STD_1
    data_response = [ "STD_1" ]
    response=client.get(SERVER_URL+'A1-P/v2/policytypes')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # Get counter: types (shall be 1)
    response=client.get(SERVER_URL+'counter/num_types')
    assert response.status_code == 200
    assert response.data ==  b"1"

    # API: Get policy type: STD_1
    with open(testdata+'std_1.json') as json_file:
        data_response = json.load(json_file)
        response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1')
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(data_response, result)
        assert res == True

    # API: API: Get policy instances, shall be empty
    data_response = []
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # API: Create policy instance pi1 of type: STD_1
    with open(testdata+'pi1.json') as json_file:
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi1', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 201
        result=json.loads(response.data)
        res=compare(json_payload, result)
        assert res == True

    # API: API: Get policy instance pi1 of type: STD_1
    with open(testdata+'pi1.json') as json_file:
        data_response = json.load(json_file)
        response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi1')
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(data_response, result)
        assert res == True

    # API: Update policy instance pi1 of type: STD_1
    with open(testdata+'pi1.json') as json_file:
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi1', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(json_payload, result)
        assert res == True

    # API: Update policy instance pi1 of type: STD_1
    with open(testdata+'pi1_updated.json') as json_file:
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi1', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(json_payload, result)
        assert res == True

    # # API: Duplicate policy instance pi2 of type: STD_1 - and delete it

    with open(testdata+'pi1_updated.json') as json_file:
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi2', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 201
        result=json.loads(response.data)
        res=compare(json_payload, result)
        assert res == True
    data_response = b""
    response=client.delete(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi2')
    assert response.status_code == 204
    assert data_response == response.data


    # API: Get policy instances, shall contain pi1
    data_response = ["pi1"]
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # Get counter: intstance
    response=client.get(SERVER_URL+'counter/num_instances')
    assert response.status_code == 200
    assert response.data ==  b"1"

    # Get counter: types
    response=client.get(SERVER_URL+'counter/num_types')
    assert response.status_code == 200
    assert response.data ==  b"1"

    # Set force response code 409. ==="
    response=client.post(SERVER_URL+'forceresponse?code=409')
    assert response.status_code == 200

    # API: Get policy instances, shall fail
    data_response = {"title" : "Conflict", "status" : 409, "detail" : "Request could not be processed in the current state of the resource"}
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies')
    assert response.status_code == 409
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # API: API: Get policy status
    data_response = {"enforceStatus" : "", "enforceReason" : ""}
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi1/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # API: Create policy instance pi2 of type: STD_1
    with open(testdata+'pi2.json') as json_file:
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi2', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 201
        result=json.loads(response.data)
        res=compare(json_payload, result)
        assert res == True

    # API: Update policy instance pi2 of type: STD_1
    with open(testdata+'pi2.json') as json_file:
        json_payload=json.load(json_file)
        response=client.put(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi2', headers=header, data=json.dumps(json_payload))
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(json_payload, result)
        assert res == True

    # API: Get policy instances, shall contain pi1 and pi2
    data_response = ["pi1","pi2"]
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # Get counter: intstance
    response=client.get(SERVER_URL+'counter/num_instances')
    assert response.status_code == 200
    assert response.data ==  b"2"

    # Get counter: types
    response=client.get(SERVER_URL+'counter/num_types')
    assert response.status_code == 200
    assert response.data ==  b"1"

    # Set force delay 10
    response=client.post(SERVER_URL+'forcedelay?delay=10')
    assert response.status_code == 200
    assert response.data ==  b"Force delay: 10 sec set for all A1 responses"

    #start time stamp
    start=time.time()

    # API: Get policy instances, shall contain pi1 and pi2 and delayed 10 sec
    data_response = ["pi1","pi2"]
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    end=time.time()

    assert (end-start) > 9

    # Reset force delay
    response=client.post(SERVER_URL+'forcedelay')
    assert response.status_code == 200
    assert response.data ==  b"Force delay: None sec set for all A1 responses"

    # API: API: Get policy instance pi1 of type: STD_1
    with open(testdata+'pi1_updated.json') as json_file:
        data_response = json.load(json_file)
        response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi1')
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(data_response, result)
        assert res == True

    # API: API: Get policy instance pi2 of type: STD_1
    with open(testdata+'pi2.json') as json_file:
        data_response = json.load(json_file)
        response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi2')
        assert response.status_code == 200
        result=json.loads(response.data)
        res=compare(data_response, result)
        assert res == True

    # API: DELETE policy instance pi1
    data_response = b""
    response=client.delete(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi1')
    assert response.status_code == 204
    assert data_response == response.data

    # API: Get policy instances, shall contain pi2
    data_response = ["pi2"]
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # API: API: Get policy status
    data_response = {"enforceStatus" : "", "enforceReason" : ""}
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi2/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True

    # Set status for policy instance pi2
    response=client.put(SERVER_URL+'status?policyid=pi2&status=OK')
    assert response.status_code == 200

    # API: API: Get policy status
    data_response = {"enforceStatus" : "OK"}
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi2/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    print(response.data)
    assert res == True

    # Set status for policy instance pi2
    response=client.put(SERVER_URL+'status?policyid=pi2&status=NOTOK&reason=notok_reason')
    assert response.status_code == 200

    # API: API: Get policy status
    data_response = {"enforceStatus" : "NOTOK", "enforceReason" : "notok_reason"}
    response=client.get(SERVER_URL+'A1-P/v2/policytypes/STD_1/policies/pi2/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_response, result)
    assert res == True


    # #Found no way to test these functions
    # #'sendstatus' will send a http request that will fail
    # #since no server will receive the call
    # #These function is instead tested when running the bash script in the 'test' dir
    # # # Send status for pi2
    # # response=client.post(SERVER_URL+'sendstatus?policyid=pi2')
    # # assert response.status_code == 200
    # # result=json.loads(response.data)
    # # res=compare(data_get_status, result)
    # # assert res == True

    # # # Send status, shall fail
    # # response=client.post(SERVER_URL+'sendstatus')
    # # assert response.status_code == 400

    # Get counter: data_delivery
    response=client.get(SERVER_URL+'counter/datadelivery')
    assert response.status_code == 200
    assert response.data ==  b"0"

    # Send data
    json_payload={}
    response=client.post(SERVER_URL+'datadelivery', headers=header, data=json.dumps(json_payload))
    assert response.status_code == 200

    # Get counter: data_delivery
    response=client.get(SERVER_URL+'counter/datadelivery')
    assert response.status_code == 200
    assert response.data ==  b"1"

    # Get counter: interface
    response=client.get(SERVER_URL+'counter/interface')
    assert response.status_code == 200
    assert response.data ==  b"STD_2.0.0"

    # Get counter: remote hosts
    response=client.get(SERVER_URL+'counter/remote_hosts')
    assert response.status_code == 200

    # Get counter: intstance
    response=client.get(SERVER_URL+'counter/num_instances')
    assert response.status_code == 200
    assert response.data ==  b"1"

    # Get counter: types
    response=client.get(SERVER_URL+'counter/num_types')
    assert response.status_code == 200
    assert response.data ==  b"1"