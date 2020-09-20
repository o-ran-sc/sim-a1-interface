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

from unittest import TestCase
import sys
import os
import threading
import requests
import json

#Constants for the test case
INTERFACE_VERSION="STD_1.1.3"
PORT_NUMBER="2224"
HOST_IP="localhost"
SERVER_URL="http://"+HOST_IP+":"+PORT_NUMBER+"/"

cwd=os.getcwd()+"/"
# Env TESTS_BASE_PATH is set when executed via tox.ini
# If basic test is executed from cmd line, that env var is not needed
if 'TESTS_BASE_PATH' in os.environ:
     cwd=os.environ['TESTS_BASE_PATH']+"/"+INTERFACE_VERSION+"/"
TESTDATA=cwd+"/../../test/"+INTERFACE_VERSION+"/jsonfiles/"

#Env var to setup api version and host logging
os.environ['APIPATH'] = cwd+"/../../api/"+INTERFACE_VERSION
os.environ['REMOTE_HOSTS_LOGGING'] = "ON"

# Paths need to run the sim, including needed source file dirs
sys.path.append(os.path.abspath(cwd+'../../src/common'))
sys.path.append(os.path.abspath(cwd+'../../test/common'))
sys.path.append(os.path.abspath(cwd+'../../src/'+INTERFACE_VERSION))
os.chdir(cwd+"../../src/"+INTERFACE_VERSION)

import main
from compare_json import compare

class TestCase1(TestCase):
    from main import app
    server = None

    def startServer(self):
        self.app.run(port=PORT_NUMBER, host=HOST_IP, threaded=True)

    def setUp(self):
        self.server=threading.Thread(target=self.startServer, args=())
        self.server.daemon = True
        self.server.start()

    # executed after each test
    def tearDown(self):
        self.server.killed=True

    #from main import app
    def test_apis(self):

        # header for json payload
        header = {
            "Content-Type" : "application/json"
        }

        # Simulator hello world
        response=requests.get(SERVER_URL)
        self.assertEqual(response.status_code, 200)

        # Check used and implemented interfaces
        response=requests.get(SERVER_URL+'container_interfaces')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "Current interface: STD_1.1.3  All supported A1 interface yamls in this container: ['OSC_2.1.0', 'STD_1.1.3']")

        # Reset simulator instances
        response=requests.post(SERVER_URL+'deleteinstances')
        self.assertEqual(response.status_code, 200)

        # Reset simulator, all
        response=requests.post(SERVER_URL+'deleteall')
        self.assertEqual(response.status_code, 200)

        # API: Get policy instances, shall be empty
        data_policy_get = [ ]
        response=requests.get(SERVER_URL+'A1-P/v1/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policy_get, result)
        self.assertEqual(res, True)

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
        response=requests.put(SERVER_URL+'A1-P/v1/policies/pi1', headers=header, data=json.dumps(data_pi1))
        self.assertEqual(response.status_code, 201)
        result=json.loads(response.text)
        res=compare(data_pi1, result)
        self.assertEqual(res, True)

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
        response=requests.put(SERVER_URL+'A1-P/v1/policies/pi1', headers=header, data=json.dumps(data_pi1_updated))
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_pi1_updated, result)
        self.assertEqual(res, True)

        #API: Create policy instance pi9, bad json
        response=requests.put(SERVER_URL+'A1-P/v1/policies/pi9', headers=header, data="test")
        self.assertEqual(response.status_code, 400)

        # API: Get policy instances, shall contain pi1
        data_policy_get = [ "pi1" ]
        response=requests.get(SERVER_URL+'A1-P/v1/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policy_get, result)
        self.assertEqual(res, True)

        # API: Create policy instance pi2 (copy of pi1). Shall fail
        data_create_errror_pi1 = {
            "title" : "The policy json already exists.",
            "status" : 400,
            "instance" : "pi2"
        }
        response=requests.put(SERVER_URL+'A1-P/v1/policies/pi2', headers=header, data=json.dumps(data_pi1_updated))
        self.assertEqual(response.status_code, 400)
        result=json.loads(response.text)
        res=compare(data_create_errror_pi1, result)
        self.assertEqual(res, True)

        # Set force response code 409. ==="
        response=requests.post(SERVER_URL+'forceresponse?code=409')
        self.assertEqual(response.status_code, 200)

        # API: Get policy instances, shall fail
        data_get_errror = {
            "title" : "Conflict",
            "status" : 409,
            "detail" : "Request could not be processed in the current state of the resource"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies')
        self.assertEqual(response.status_code, 409)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        # Reset force response
        response=requests.post(SERVER_URL+'forceresponse')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "Force response code: None set for one single A1 response")

        ###
        ### Repeating the above two test for code coverage
        ###
        # Set force response code 400
        response=requests.post(SERVER_URL+'forceresponse?code=400')
        self.assertEqual(response.status_code, 200)

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
        response=requests.put(SERVER_URL+'A1-P/v1/policies/pi3', headers=header, data=json.dumps(data_pi3))
        self.assertEqual(response.status_code, 400)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        # Set force response code 404
        response=requests.post(SERVER_URL+'forceresponse?code=404')
        self.assertEqual(response.status_code, 200)

        # API: Get policy instance pi1, shall fail =="
        data_get_errror = {
            "title" : "Not found",
            "status" : 404,
            "detail" : "No resource found at the URI"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi1')
        self.assertEqual(response.status_code, 404)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        # Set force response code 405
        response=requests.post(SERVER_URL+'forceresponse?code=405')
        self.assertEqual(response.status_code, 200)

        # API: Delete policy instances pi1, shall fail =="
        data_get_errror = {
            "title" : "Method not allowed",
            "status" : 405,
            "detail" : "Method not allowed for the URI"
        }
        response=requests.delete(SERVER_URL+'A1-P/v1/policies/pi1')
        self.assertEqual(response.status_code, 405)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        # Set force response code 429
        response=requests.post(SERVER_URL+'forceresponse?code=429')
        self.assertEqual(response.status_code, 200)

        # API: Get policy status pi3, shall fail =="
        data_get_errror = {
            "title" : "Too many requests",
            "status" : 429,
            "detail" : "Too many requests have been sent in a given amount of time"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi3/status')
        self.assertEqual(response.status_code, 429)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        # Set force response code 507
        response=requests.post(SERVER_URL+'forceresponse?code=507')
        self.assertEqual(response.status_code, 200)

        # API: Get policy instances, shall fail
        data_get_errror = {
            "title" : "Insufficient storage",
            "status" : 507,
            "detail" : "The method could not be performed on the resource because the provider is unable to store the representation needed to successfully complete the request"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies')
        self.assertEqual(response.status_code, 507)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        # Set force response code 503. ==="
        response=requests.post(SERVER_URL+'forceresponse?code=503')
        self.assertEqual(response.status_code, 200)

        # API: Get policy instances, shall fail
        data_get_errror = {
            "title" : "Service unavailable",
            "status" : 503,
            "detail" : "The provider is currently unable to handle the request due to a temporary overload"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies')
        self.assertEqual(response.status_code, 503)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        # Set force response code 555. ==="
        response=requests.post(SERVER_URL+'forceresponse?code=555')
        self.assertEqual(response.status_code, 200)

        # API: Get policy instances, shall fail
        data_get_errror = {
            "title" : "Unknown",
            "status" : "555",
            "detail" : "Not implemented response code"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies')
        self.assertEqual(response.status_code, 555)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        ###
        ### End of repeated test
        ###


        # API: Get policy status
        data_policy_status = {
            "enforceStatus" : "UNDEFINED"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi1/status')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policy_status, result)
        self.assertEqual(res, True)

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
        response=requests.put(SERVER_URL+'A1-P/v1/policies/pi2', headers=header, data=json.dumps(data_pi2))
        self.assertEqual(response.status_code, 201)
        result=json.loads(response.text)
        res=compare(data_pi2, result)
        self.assertEqual(res, True)


        # API: Update policy instance pi2
        # Reuse same policy data
        response=requests.put(SERVER_URL+'A1-P/v1/policies/pi2?notificationDestination=http://'+HOST_IP+':'+PORT_NUMBER+'/statustest', headers=header, data=json.dumps(data_pi2))
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_pi2, result)
        self.assertEqual(res, True)

        # API: Get policy instances, shall contain pi1 and pi2
        data_policy_get = [ "pi1", "pi2" ]
        response=requests.get(SERVER_URL+'A1-P/v1/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policy_get, result)
        self.assertEqual(res, True)

        # Set force delay 10
        response=requests.post(SERVER_URL+'forcedelay?delay=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "Force delay: 10 sec set for all A1 responses")

        # API: Get policy instances, shall contain pi1 and pi2 and delayed 10 sec
        data_policy_get = [ "pi1", "pi2" ]
        response=requests.get(SERVER_URL+'A1-P/v1/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policy_get, result)
        self.assertEqual(res, True)

        # Reset force delay
        response=requests.post(SERVER_URL+'forcedelay')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "Force delay: None sec set for all A1 responses")

        # API: GET policy instance pi1
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi1')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_pi1_updated, result)
        self.assertEqual(res, True)

        # API: GET policy instance pi2
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi2')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_pi2, result)
        self.assertEqual(res, True)

        # API: GET policy instance pi9, shall fail
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi9')
        self.assertEqual(response.status_code, 404)

        # API: DELETE policy instance pi1
        response=requests.delete(SERVER_URL+'A1-P/v1/policies/pi1')
        self.assertEqual(response.status_code, 204)

        # API: DELETE policy instance pi9, shall fail
        response=requests.delete(SERVER_URL+'A1-P/v1/policies/pi9')
        self.assertEqual(response.status_code, 404)

        # API: Get policy status for pi1, shall fail
        data_get_errror = {
            "title" : "The policy identity does not exist.",
            "status" : 404,
            "detail" : "There is no existing policy instance with the identity: pi1",
            "instance" : "pi1"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi1/status')
        self.assertEqual(response.status_code, 404)
        result=json.loads(response.text)
        res=compare(data_get_errror, result)
        self.assertEqual(res, True)

        # Set status for policy instance pi2
        response=requests.put(SERVER_URL+'status?policyid=pi2&status=OK')
        self.assertEqual(response.status_code, 200)

        # API: Get policy status for pi2
        data_get_status = {
            "enforceStatus" : "OK"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi2/status')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_get_status, result)
        self.assertEqual(res, True)

        # Set status for policy instance pi2
        response=requests.put(SERVER_URL+'status?policyid=pi2&status=NOTOK&reason=notok_reason')
        self.assertEqual(response.status_code, 200)

        # API: Get policy status for pi2
        data_get_status = {
            "enforceStatus" : "NOTOK",
            "enforceReason" : "notok_reason"
        }
        response=requests.get(SERVER_URL+'A1-P/v1/policies/pi2/status')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_get_status, result)
        self.assertEqual(res, True)

        # Send status for pi2
        response=requests.post(SERVER_URL+'sendstatus?policyid=pi2')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_get_status, result)
        self.assertEqual(res, True)

        # Send status, shall fail
        response=requests.post(SERVER_URL+'sendstatus')
        self.assertEqual(response.status_code, 400)

        # Send status pi9, shall fail
        response=requests.post(SERVER_URL+'sendstatus?policyid=pi9')
        self.assertEqual(response.status_code, 404)

        # Set status for policy instance , shall fail
        response=requests.put(SERVER_URL+'status')
        self.assertEqual(response.status_code, 400)

        # Set status for policy instance pi9, shall fail
        response=requests.put(SERVER_URL+'status?policyid=pi9')
        self.assertEqual(response.status_code, 404)

        # Set status for policy instance pi2, shall fail
        response=requests.put(SERVER_URL+'status?policyid=pi2')
        self.assertEqual(response.status_code, 400)


        # Get counter: intstance
        response=requests.get(SERVER_URL+'counter/num_instances')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "1")

        # Get counter: types (shall be 0)
        response=requests.get(SERVER_URL+'counter/num_types')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "0")

        # Get counter: interface
        response=requests.get(SERVER_URL+'counter/interface')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "STD_1.1.3")

        # Get counter: remote hosts
        response=requests.get(SERVER_URL+'counter/remote_hosts')
        self.assertEqual(response.status_code, 200)

        # Get counter: test, shall fail
        response=requests.get(SERVER_URL+'counter/test')
        self.assertEqual(response.status_code, 404)
