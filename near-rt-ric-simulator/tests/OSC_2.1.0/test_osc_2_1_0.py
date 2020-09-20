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

# This test case test the OSC_2.1.0 version of the simulator

from unittest import TestCase
import sys
import os
import threading
import requests
import json


#Constants for the test case
INTERFACE_VERSION="OSC_2.1.0"
PORT_NUMBER="2223"
HOST_IP="localhost"
SERVER_URL="http://"+HOST_IP+":"+PORT_NUMBER+"/"

cwd=os.getcwd()+"/"
# Env TESTS_BASE_PATH is set when executed via tox.ini
# If basic test is executed from cmd line, that env var is not needed
if 'TESTS_BASE_PATH' in os.environ:
     cwd=os.environ['TESTS_BASE_PATH']+"/"+INTERFACE_VERSION+"/"
TESTDATA=cwd+"/../../test/"+INTERFACE_VERSION+"/jsonfiles/"

#Env var to setup version and host logging
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

    def test_apis(self):

        # Header for json payload
        header = {
            "Content-Type" : "application/json"
        }

        # Simulator hello world
        response=requests.get(SERVER_URL)
        self.assertEqual(response.status_code, 200)

        # Check used and implemented interfaces
        response=requests.get(SERVER_URL+'container_interfaces')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "Current interface: OSC_2.1.0  All supported A1 interface yamls in this container: ['OSC_2.1.0', 'STD_1.1.3']")

        # Reset simulator instances
        response=requests.post(SERVER_URL+'deleteinstances')
        self.assertEqual(response.status_code, 200)

        # Reset simulator, all
        response=requests.post(SERVER_URL+'deleteall')
        self.assertEqual(response.status_code, 200)

        # API: Healthcheck
        response=requests.get(SERVER_URL+'a1-p/healthcheck')
        self.assertEqual(response.status_code, 200)

        # API: Get policy types, shall be empty
        data_policytypes_get = [ ]
        response=requests.get(SERVER_URL+'a1-p/policytypes')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policytypes_get, result)
        self.assertEqual(res, True)

        # API: Delete a policy type, shall fail
        response=requests.delete(SERVER_URL+'a1-p/policytypes/1')
        self.assertEqual(response.status_code, 404)

        # API: Get policy instances for type 1, shall fail
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies')
        self.assertEqual(response.status_code, 404)

        # API: Put a policy type: 1
        with open(TESTDATA+'pt1.json') as json_file:
            policytype_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1', headers=header, data=json.dumps(policytype_1))
            self.assertEqual(response.status_code, 201)

        # API: Put a policy type: 1 again
        with open(TESTDATA+'pt1.json') as json_file:
            policytype_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1', headers=header, data=json.dumps(policytype_1))
            self.assertEqual(response.status_code, 201)

        # API: Delete a policy type
        response=requests.delete(SERVER_URL+'a1-p/policytypes/1')
        self.assertEqual(response.status_code, 204)

        # API: Get policy type ids, shall be empty
        data_policytypes_get = [ ]
        response=requests.get(SERVER_URL+'a1-p/policytypes')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policytypes_get, result)
        self.assertEqual(res, True)

        # API: Put a policy type: 1
        with open(TESTDATA+'pt1.json') as json_file:
            policytype_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1', headers=header, data=json.dumps(policytype_1))
            self.assertEqual(response.status_code, 201)

        # API: Get policy type ids, shall contain '1'
        data_policytypes_get = [ 1 ]
        response=requests.get(SERVER_URL+'a1-p/policytypes')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policytypes_get, result)
        self.assertEqual(res, True)

        # API: Get instances for type 1, shall be empty
        data_policies_get = [ ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policies_get, result)
        self.assertEqual(res, True)

        # API: Create policy instance pi1 of type: 1
        with open(TESTDATA+'pi1.json') as json_file:
            policy_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1/policies/pi1', headers=header, data=json.dumps(policy_1))
            self.assertEqual(response.status_code, 202)

        # API: Get policy instance pi1 of type: 1
        with open(TESTDATA+'pi1.json') as json_file:
            policy_1 = json.load(json_file)
            response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1')
            self.assertEqual(response.status_code, 200)
            result=json.loads(response.text)
            res=compare(policy_1, result)
            self.assertEqual(res, True)

        # API: Update policy instance pi1 of type: 1
        with open(TESTDATA+'pi1.json') as json_file:
            policy_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1/policies/pi1', headers=header, data=json.dumps(policy_1))
            self.assertEqual(response.status_code, 202)

        # API: Update policy type: 1, shall fail
        with open(TESTDATA+'pt1.json') as json_file:
            policytype_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1', headers=header, data=json.dumps(policytype_1))
            self.assertEqual(response.status_code, 400)

        # API: Get instances for type 1, shall contain 'pi1'
        data_policies_get = [ "pi1" ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policies_get, result)
        self.assertEqual(res, True)

        # API: Create policy instance pi2 (copy of pi1) of type: 1. Shall fail
        with open(TESTDATA+'pi1.json') as json_file:
            policy_2 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1/policies/pi2', headers=header, data=json.dumps(policy_2))
            self.assertEqual(response.status_code, 400)

        # Set force response code 401
        response=requests.post(SERVER_URL+'forceresponse?code=401')
        self.assertEqual(response.status_code, 200)

        # API: Get policy type 1. Shall fail with forced code
        response=requests.get(SERVER_URL+'a1-p/policytypes/1')
        self.assertEqual(response.status_code, 401)

        # API: Get policy status
        policy_status = {
            "instance_status" : "NOT IN EFFECT",
            "has_been_deleted" : "false",
            "created_at" : "????"
        }
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(policy_status, result)
        self.assertEqual(res, True)

        # Load a policy type: 2
        with open(TESTDATA+'pt2.json') as json_file:
            policytype_2 = json.load(json_file)
            response=requests.put(SERVER_URL+'policytype?id=2', headers=header, data=json.dumps(policytype_2))
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.text, "Policy type 2 is OK.")

        # Load a policy type: 2, again
        with open(TESTDATA+'pt2.json') as json_file:
            policytype_2 = json.load(json_file)
            response=requests.put(SERVER_URL+'policytype?id=2', headers=header, data=json.dumps(policytype_2))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, "Policy type 2 is OK.")

        # API: Get policy type ids, shall contain '1' and '2'
        data_policytypes_get = [ 1,2 ]
        response=requests.get(SERVER_URL+'a1-p/policytypes')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policytypes_get, result)
        self.assertEqual(res, True)

        # Get policy type ids, shall contain type 1 and 2 =="
        data_policytypes_get = [ "1","2" ]
        response=requests.get(SERVER_URL+'policytypes')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policytypes_get, result)
        self.assertEqual(res, True)

        # API: Get policy type 2
        with open(TESTDATA+'pt2.json') as json_file:
            policytype_2 = json.load(json_file)
            response=requests.get(SERVER_URL+'a1-p/policytypes/2')
            self.assertEqual(response.status_code, 200)
            result=json.loads(response.text)
            res=compare(policytype_2, result)
            self.assertEqual(res, True)

        # Delete a policy type
        response=requests.delete(SERVER_URL+'policytype?id=2')
        self.assertEqual(response.status_code, 204)

        # API: Get policy type ids, shall contain '1'
        data_policytypes_get = [ 1]
        response=requests.get(SERVER_URL+'a1-p/policytypes')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policytypes_get, result)
        self.assertEqual(res, True)

        # Load a policy type: 2
        with open(TESTDATA+'pt2.json') as json_file:
            policytype_2 = json.load(json_file)
            response=requests.put(SERVER_URL+'policytype?id=2', headers=header, data=json.dumps(policytype_2))
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.text, "Policy type 2 is OK.")

        # API: Get policy type 2
        with open(TESTDATA+'pt2.json') as json_file:
            policytype_2 = json.load(json_file)
            response=requests.get(SERVER_URL+'a1-p/policytypes/2')
            self.assertEqual(response.status_code, 200)
            result=json.loads(response.text)
            res=compare(policytype_2, result)
            self.assertEqual(res, True)

        # API: Get instances for type 2, shall be empty
        data_policies_get = [ ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/2/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policies_get, result)
        self.assertEqual(res, True)

        # API: Create policy instance pi1 of type: 2, shall fail
        with open(TESTDATA+'pi1.json') as json_file:
            policy_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/2/policies/pi1', headers=header, data=json.dumps(policy_1))
            self.assertEqual(response.status_code, 400)

        # API: Create policy instance pi2 of type: 2. Missing param, shall fail
        with open(TESTDATA+'pi2_missing_param.json') as json_file:
            policy_2 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/2/policies/pi1', headers=header, data=json.dumps(policy_2))
            self.assertEqual(response.status_code, 400)

        # API: Create policy instance pi2 of type: 2
        with open(TESTDATA+'pi2.json') as json_file:
            policy_2 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/2/policies/pi2', headers=header, data=json.dumps(policy_2))
            self.assertEqual(response.status_code, 202)

        with open(TESTDATA+'pi2.json') as json_file:
            policy_2 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/2/policies/pi2', headers=header, data=json.dumps(policy_2))
            self.assertEqual(response.status_code, 202)

        # API: Get instances for type 1, shall contain pi1
        data_policies_get = [ "pi1" ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policies_get, result)
        self.assertEqual(res, True)

        # API: Get instances for type 2, shall contain pi2
        data_policies_get = ["pi2" ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/2/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policies_get, result)
        self.assertEqual(res, True)

        # API: Create policy instance pi11 (copy of pi1) of type: 1. Shall fail
        with open(TESTDATA+'pi1.json') as json_file:
            policy_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1/policies/pi11', headers=header, data=json.dumps(policy_1))
            self.assertEqual(response.status_code, 400)

        # Set force response code 409. ==="
        response=requests.post(SERVER_URL+'forceresponse?code=401')
        self.assertEqual(response.status_code, 200)

        # API: Get policy status for pi1, shall fail
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
        self.assertEqual(response.status_code, 401)

        # Set force delay 10
        response=requests.post(SERVER_URL+'forcedelay?delay=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "Force delay: 10 sec set for all A1 responses")

        # API: Get policy status for pi1. Shall delay 10 sec
        policy_status = {
            "instance_status" : "NOT IN EFFECT",
            "has_been_deleted" : "false",
            "created_at" : "????"
        }
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(policy_status, result)
        self.assertEqual(res, True)

        # Reset force delay
        response=requests.post(SERVER_URL+'forcedelay')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "Force delay: None sec set for all A1 responses")

        #  Set status for pi1
        response=requests.put(SERVER_URL+'status?policyid=pi1&status=IN%20EFFECT')
        self.assertEqual(response.status_code, 200)

        # API: Get policy status for pi1
        policy_status = {
            "instance_status" : "IN EFFECT",
            "has_been_deleted" : "false",
            "created_at" : "????"
        }
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(policy_status, result)
        self.assertEqual(res, True)

        #  Set status for pi1
        response=requests.put(SERVER_URL+'status?policyid=pi1&status=IN%20EFFECT&deleted=true&created_at=2020-03-30%2012:00:00')
        self.assertEqual(response.status_code, 200)

        # API: Get policy status for pi1
        policy_status = {
            "instance_status" : "IN EFFECT",
            "has_been_deleted" : "true",
            "created_at" : "????"
        }
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies/pi1/status')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(policy_status, result)
        self.assertEqual(res, True)

        # Get counter: intstance
        response=requests.get(SERVER_URL+'counter/num_instances')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "2")

        # Get counter: types (shall be 2)
        response=requests.get(SERVER_URL+'counter/num_types')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "2")

        # Get counter: interface
        response=requests.get(SERVER_URL+'counter/interface')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "OSC_2.1.0")

        # Get counter: remote hosts
        response=requests.get(SERVER_URL+'counter/remote_hosts')
        self.assertEqual(response.status_code, 200)

        # Get counter: test, shall fail
        response=requests.get(SERVER_URL+'counter/test')
        self.assertEqual(response.status_code, 404)

        # API: DELETE policy instance pi1
        response=requests.delete(SERVER_URL+'a1-p/policytypes/1/policies/pi1')
        self.assertEqual(response.status_code, 202)

        # API: Get instances for type 1, shall be empty
        data_policies_get = [ ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policies_get, result)
        self.assertEqual(res, True)

        # API: Get instances for type 2, shall contain pi2
        data_policies_get = ["pi2" ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/2/policies')
        self.assertEqual(response.status_code, 200)
        result=json.loads(response.text)
        res=compare(data_policies_get, result)
        self.assertEqual(res, True)

        # Get counter: instances
        response=requests.get(SERVER_URL+'counter/num_instances')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text,  "1")


        ### Tests to increase code coverage

        # Set force response code 500
        response=requests.post(SERVER_URL+'forceresponse?code=500')
        self.assertEqual(response.status_code, 200)

        # API: Healthcheck
        response=requests.get(SERVER_URL+'a1-p/healthcheck')
        self.assertEqual(response.status_code, 500)

        # Set force response code 501
        response=requests.post(SERVER_URL+'forceresponse?code=501')
        self.assertEqual(response.status_code, 200)

        # API: Get policy types
        data_policytypes_get = [ ]
        response=requests.get(SERVER_URL+'a1-p/policytypes')
        self.assertEqual(response.status_code, 501)

        # Set force response code 502
        response=requests.post(SERVER_URL+'forceresponse?code=502')
        self.assertEqual(response.status_code, 200)

        # API: Delete a policy type, shall fail
        response=requests.delete(SERVER_URL+'a1-p/policytypes/55')
        self.assertEqual(response.status_code, 502)

        # Set force response code 503. ==="
        response=requests.post(SERVER_URL+'forceresponse?code=503')
        self.assertEqual(response.status_code, 200)

        with open(TESTDATA+'pi1.json') as json_file:
            policy_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/1/policies/pi11', headers=header, data=json.dumps(policy_1))
            self.assertEqual(response.status_code, 503)

        # Set force response code 504
        response=requests.post(SERVER_URL+'forceresponse?code=504')
        self.assertEqual(response.status_code, 200)

        # API: Get instances for type 1, shall fail
        data_policies_get = [ ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies')
        self.assertEqual(response.status_code, 504)

        # Set force response code 505. ==="
        response=requests.post(SERVER_URL+'forceresponse?code=505')
        self.assertEqual(response.status_code, 200)

        # API: delete instance pi1, shall fail
        response=requests.delete(SERVER_URL+'a1-p/policytypes/1/policies/pi1')
        self.assertEqual(response.status_code, 505)

        # API: Delete a policy type having instances, shall fail
        response=requests.delete(SERVER_URL+'a1-p/policytypes/2')
        self.assertEqual(response.status_code, 400)

        # API: delete instance pi1 in type 5, shall fail
        response=requests.delete(SERVER_URL+'a1-p/policytypes/5/policies/pi1')
        self.assertEqual(response.status_code, 404)

        # API: delete instance pi99 in type 1, shall fail
        response=requests.delete(SERVER_URL+'a1-p/policytypes/1/policies/pi99')
        self.assertEqual(response.status_code, 404)

        # API: Create policy instance pi80 of type: 5
        with open(TESTDATA+'pi1.json') as json_file:
            policy_80 = json.load(json_file)
            response=requests.put(SERVER_URL+'a1-p/policytypes/5/policies/pi80', headers=header, data=json.dumps(policy_80))
            self.assertEqual(response.status_code, 404)

        # API: Get policy type
        data_policytypes_get = [ ]
        response=requests.get(SERVER_URL+'a1-p/policytypes/55')
        self.assertEqual(response.status_code, 404)

        # API: Get status, bad type - shall fail
        response=requests.get(SERVER_URL+'a1-p/policytypes/99/policies/pi1/status')
        self.assertEqual(response.status_code, 404)

        # API: Get status, bad instance - shall fail
        response=requests.get(SERVER_URL+'a1-p/policytypes/1/policies/pi111/status')
        self.assertEqual(response.status_code, 404)

        # Load policy type, no type in url - shall faill
        with open(TESTDATA+'pt2.json') as json_file:
            policytype_2 = json.load(json_file)
            response=requests.put(SERVER_URL+'policytype', headers=header, data=json.dumps(policytype_2))
            self.assertEqual(response.status_code, 400)

        # Load policy type - duplicatee - shall faill
        with open(TESTDATA+'pt1.json') as json_file:
            policytype_1 = json.load(json_file)
            response=requests.put(SERVER_URL+'policytype?id=2', headers=header, data=json.dumps(policytype_1))
            self.assertEqual(response.status_code, 400)
