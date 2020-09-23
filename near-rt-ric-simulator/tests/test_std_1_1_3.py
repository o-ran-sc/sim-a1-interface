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

# This test case test the STD_1.1.3 version of the simulator

import json

#Version of simulator
INTERFACE_VERSION="STD_1.1.3"

from unittest_setup import SERVER_URL, HOST_IP, PORT_NUMBER, setup_env, client

#Setup env and import paths
setup_env(INTERFACE_VERSION)

from compare_json import compare

def test_apis(client):

    # Simulator hello world
    response=client.get(SERVER_URL)
    assert response.status_code == 200

    # Check used and implemented interfaces
    response=client.get(SERVER_URL+'container_interfaces')
    assert response.status_code == 200
    assert response.data ==  b"Current interface: STD_1.1.3  All supported A1 interface yamls in this container: ['OSC_2.1.0', 'STD_1.1.3']"

    # Reset simulator instances
    response=client.post(SERVER_URL+'deleteinstances')
    assert response.status_code == 200

    # Reset simulator, all
    response=client.post(SERVER_URL+'deleteall')
    assert response.status_code == 200

    # API: Get policy instances, shall be empty
    data_policy_get = [ ]
    response=client.get(SERVER_URL+'A1-P/v1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policy_get, result)
    assert res == True

    #API: Create policy instance pi1
    data_pi1 = {
        "scope": {
            "ueId": "ue1",
            "groupId": "group1",
            "sliceId": "slice1",
            "qosId": "qos1",
            "cellId": "cell1"
            },
        "statement": {
            "priorityLevel": 5
        }
    }
    # header for json payload
    header = {
        "Content-Type" : "application/json"
    }
    response=client.put(SERVER_URL+'A1-P/v1/policies/pi1', headers=header, data=json.dumps(data_pi1))
    assert response.status_code == 201
    result=json.loads(response.data)
    res=compare(data_pi1, result)
    assert res == True

    #API: Update policy instance pi1
    data_pi1_updated = {
        "scope": {
            "ueId": "ue1",
            "groupId": "group1",
            "sliceId": "slice1",
            "qosId": "qos1",
            "cellId": "cell1"
            },
        "statement": {
            "priorityLevel": 6
        }
    }
    response=client.put(SERVER_URL+'A1-P/v1/policies/pi1', headers=header, data=json.dumps(data_pi1_updated))
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_pi1_updated, result)
    assert res == True

    #API: Create policy instance pi9, bad json
    response=client.put(SERVER_URL+'A1-P/v1/policies/pi9', headers=header, data="test")
    assert response.status_code == 400

    # API: Get policy instances, shall contain pi1
    data_policy_get = [ "pi1" ]
    response=client.get(SERVER_URL+'A1-P/v1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policy_get, result)
    assert res == True

    # API: Create policy instance pi2 (copy of pi1). Shall fail
    data_create_errror_pi1 = {
        "title" : "The policy json already exists.",
        "status" : 400,
        "instance" : "pi2"
    }
    response=client.put(SERVER_URL+'A1-P/v1/policies/pi2', headers=header, data=json.dumps(data_pi1_updated))
    assert response.status_code == 400
    result=json.loads(response.data)
    res=compare(data_create_errror_pi1, result)
    assert res == True

    # Set force response code 409. ==="
    response=client.post(SERVER_URL+'forceresponse?code=409')
    assert response.status_code == 200

    # API: Get policy instances, shall fail
    data_get_errror = {
        "title" : "Conflict",
        "status" : 409,
        "detail" : "Request could not be processed in the current state of the resource"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies')
    assert response.status_code == 409
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    # Reset force response
    response=client.post(SERVER_URL+'forceresponse')
    assert response.status_code == 200
    assert response.data ==  b"Force response code: None set for one single A1 response"

    ###
    ### Repeating the above two test for code coverage
    ###
    # Set force response code 400
    response=client.post(SERVER_URL+'forceresponse?code=400')
    assert response.status_code == 200

    #API: Create policy instance pi3, shall fail
    data_pi3 = {
        "scope": {
            "ueId": "ue3"
            },
        "statement": {
            "priorityLevel": 5
        }
    }
    data_get_errror = {
        "title" : "Bad request",
        "status" : 400,
        "detail" : "Object in payload not properly formulated or not related to the method"
    }
    response=client.put(SERVER_URL+'A1-P/v1/policies/pi3', headers=header, data=json.dumps(data_pi3))
    assert response.status_code == 400
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    # Set force response code 404
    response=client.post(SERVER_URL+'forceresponse?code=404')
    assert response.status_code == 200

    # API: Get policy instance pi1, shall fail =="
    data_get_errror = {
        "title" : "Not found",
        "status" : 404,
        "detail" : "No resource found at the URI"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi1')
    assert response.status_code == 404
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    # Set force response code 405
    response=client.post(SERVER_URL+'forceresponse?code=405')
    assert response.status_code == 200

    # API: Delete policy instances pi1, shall fail =="
    data_get_errror = {
        "title" : "Method not allowed",
        "status" : 405,
        "detail" : "Method not allowed for the URI"
    }
    response=client.delete(SERVER_URL+'A1-P/v1/policies/pi1')
    assert response.status_code == 405
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    # Set force response code 429
    response=client.post(SERVER_URL+'forceresponse?code=429')
    assert response.status_code == 200

    # API: Get policy status pi3, shall fail =="
    data_get_errror = {
        "title" : "Too many requests",
        "status" : 429,
        "detail" : "Too many requests have been sent in a given amount of time"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi3/status')
    assert response.status_code == 429
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    # Set force response code 507
    response=client.post(SERVER_URL+'forceresponse?code=507')
    assert response.status_code == 200

    # API: Get policy instances, shall fail
    data_get_errror = {
        "title" : "Insufficient storage",
        "status" : 507,
        "detail" : "The method could not be performed on the resource because the provider is unable to store the representation needed to successfully complete the request"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies')
    assert response.status_code == 507
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    # Set force response code 503. ==="
    response=client.post(SERVER_URL+'forceresponse?code=503')
    assert response.status_code == 200

    # API: Get policy instances, shall fail
    data_get_errror = {
        "title" : "Service unavailable",
        "status" : 503,
        "detail" : "The provider is currently unable to handle the request due to a temporary overload"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies')
    assert response.status_code == 503
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    # Set force response code 555. ==="
    response=client.post(SERVER_URL+'forceresponse?code=555')
    assert response.status_code == 200

    # API: Get policy instances, shall fail
    data_get_errror = {
        "title" : "Unknown",
        "status" : "555",
        "detail" : "Not implemented response code"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies')
    assert response.status_code == 555
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    ###
    ### End of repeated test
    ###


    # API: Get policy status
    data_policy_status = {
        "enforceStatus" : "UNDEFINED"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi1/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policy_status, result)
    assert res == True

    # API: Create policy instance pi2
    data_pi2 = {
        "scope": {
            "ueId": "ue2",
            "groupId": "group2",
            "sliceId": "slice2",
            "qosId": "qos2",
            "cellId": "cell2"
            },
        "statement": {
            "priorityLevel": 10
        }
    }
    response=client.put(SERVER_URL+'A1-P/v1/policies/pi2', headers=header, data=json.dumps(data_pi2))
    assert response.status_code == 201
    result=json.loads(response.data)
    res=compare(data_pi2, result)
    assert res == True


    # API: Update policy instance pi2
    # Reuse same policy data
    response=client.put(SERVER_URL+'A1-P/v1/policies/pi2?notificationDestination=http://'+HOST_IP+':'+PORT_NUMBER+'/statustest', headers=header, data=json.dumps(data_pi2))
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_pi2, result)
    assert res == True

    # API: Get policy instances, shall contain pi1 and pi2
    data_policy_get = [ "pi1", "pi2" ]
    response=client.get(SERVER_URL+'A1-P/v1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policy_get, result)
    assert res == True

    # Set force delay 10
    response=client.post(SERVER_URL+'forcedelay?delay=10')
    assert response.status_code == 200
    assert response.data ==  b"Force delay: 10 sec set for all A1 responses"

    # API: Get policy instances, shall contain pi1 and pi2 and delayed 10 sec
    data_policy_get = [ "pi1", "pi2" ]
    response=client.get(SERVER_URL+'A1-P/v1/policies')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_policy_get, result)
    assert res == True

    # Reset force delay
    response=client.post(SERVER_URL+'forcedelay')
    assert response.status_code == 200
    assert response.data ==  b"Force delay: None sec set for all A1 responses"

    # API: GET policy instance pi1
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi1')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_pi1_updated, result)
    assert res == True

    # API: GET policy instance pi2
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi2')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_pi2, result)
    assert res == True

    # API: GET policy instance pi9, shall fail
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi9')
    assert response.status_code == 404

    # API: DELETE policy instance pi1
    response=client.delete(SERVER_URL+'A1-P/v1/policies/pi1')
    assert response.status_code == 204

    # API: DELETE policy instance pi9, shall fail
    response=client.delete(SERVER_URL+'A1-P/v1/policies/pi9')
    assert response.status_code == 404

    # API: Get policy status for pi1, shall fail
    data_get_errror = {
        "title" : "The policy identity does not exist.",
        "status" : 404,
        "detail" : "There is no existing policy instance with the identity: pi1",
        "instance" : "pi1"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi1/status')
    assert response.status_code == 404
    result=json.loads(response.data)
    res=compare(data_get_errror, result)
    assert res == True

    # Set status for policy instance pi2
    response=client.put(SERVER_URL+'status?policyid=pi2&status=OK')
    assert response.status_code == 200

    # API: Get policy status for pi2
    data_get_status = {
        "enforceStatus" : "OK"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi2/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_get_status, result)
    assert res == True

    # Set status for policy instance pi2
    response=client.put(SERVER_URL+'status?policyid=pi2&status=NOTOK&reason=notok_reason')
    assert response.status_code == 200

    # API: Get policy status for pi2
    data_get_status = {
        "enforceStatus" : "NOTOK",
        "enforceReason" : "notok_reason"
    }
    response=client.get(SERVER_URL+'A1-P/v1/policies/pi2/status')
    assert response.status_code == 200
    result=json.loads(response.data)
    res=compare(data_get_status, result)
    assert res == True

    #Found no way to test these functions
    #'sendstatus' will send a http request that will fail
    #since no server will receive the call
    #These function is instead tested when running the bash script in the 'test' dir
    # # Send status for pi2
    # response=client.post(SERVER_URL+'sendstatus?policyid=pi2')
    # assert response.status_code == 200
    # result=json.loads(response.data)
    # res=compare(data_get_status, result)
    # assert res == True

    # # Send status, shall fail
    # response=client.post(SERVER_URL+'sendstatus')
    # assert response.status_code == 400

    # # Send status pi9, shall fail
    # response=client.post(SERVER_URL+'sendstatus?policyid=pi9')
    # assert response.status_code == 404

    # Set status for policy instance , shall fail
    response=client.put(SERVER_URL+'status')
    assert response.status_code == 400

    # Set status for policy instance pi9, shall fail
    response=client.put(SERVER_URL+'status?policyid=pi9')
    assert response.status_code == 404

    # Set status for policy instance pi2, shall fail
    response=client.put(SERVER_URL+'status?policyid=pi2')
    assert response.status_code == 400


    # Get counter: intstance
    response=client.get(SERVER_URL+'counter/num_instances')
    assert response.status_code == 200
    assert response.data ==  b"1"

    # Get counter: types (shall be 0)
    response=client.get(SERVER_URL+'counter/num_types')
    assert response.status_code == 200
    assert response.data ==  b"0"

    # Get counter: interface
    response=client.get(SERVER_URL+'counter/interface')
    assert response.status_code == 200
    assert response.data ==  b"STD_1.1.3"

    # Get counter: remote hosts
    response=client.get(SERVER_URL+'counter/remote_hosts')
    assert response.status_code == 200

    # Get counter: test, shall fail
    response=client.get(SERVER_URL+'counter/test')
    assert response.status_code == 404
