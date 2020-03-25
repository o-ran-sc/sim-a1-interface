# O-RAN-SC Near-RealTime RIC Simulator

The O-RAN SC Near-RealTime RIC simulates the A1 as an generic REST API which can receive and send northbound messages. The simulator validates the payload and applies policy.

The simulator supports multiple A1 interface versions (version of the open API yaml file):
- OSC 2.1.0,                   version-id: OSC\_2.1.0
- A1 Standard 1.1.3,           version-id: STD\_1.1.3
- 1.1.x-alpha.2 ,              version-id: 1.1.x-alpha.2

All versions are supported by the same container, see section 'Configuring the simulator' below for details about how to the start the simulator with the correct version.

The overall folder structure is (relative to the location of this README file):
.                 Dockerfile and README
api               The open api yaml for each supported version
src               Python source code for each supported version
test              Basic test

The simulator handles the requests that are defined in the A1 open API yaml file. All these requests are in the a1.py file in the source folder. In addition, a number of administrative functions are also supported and implemented by the main.py in the source folder.

The section below outlines the supported open api REST operations as well as the adminstrative REST operations.

# Supported operations in simulator OSC 2.1.0

URIs for A1:
 - GET, do a healthcheck: 'http://localhost:8085/healthcheck'
 - GET, get all policy type ids: http://localhost:8085/policytypes
 - DELETE, delete a policy type: http://localhost:8085/policytypes/{policy\_type\_id}
 - GET, get a policy type: http://localhost:8085/policytypes/{policy\_type\_id}
 - PUT, create/update a policy type: http://localhost:8085/policytypes/{policy\_type\_id}
 - GET, get all policy ids for a type: http://localhost:8085/policytypes/{policy\_type\_id}/policies
 - DELETE, delete a policy: http://localhost:8085/policytypes/{policy\_type\_id}/policies/{policy\_instance\_id}
 - GET, get a policy: http://localhost:8085/policytypes/{policy\_type\_id}/policies/{policy\_instance\_id}
 - PUT, create/update a policy: http://localhost:8085/policytypes/{policy\_type\_id}/policies/{policy\_instance\_id}
 - GET, get policy status: http://localhost:8085/policytypes/{policy\_type\_id}/policies/{policy\_instance\_id}/status
<br>Swagger UI at:`http://localhost:8085/ui/`

URIs for admin operations:
 - GET, a basic healthcheck: http://localhost:8085/
 - GET, a list of all supported interfaces: http://localhost:8085/container\_interfaces
 - POST, delete all policy instances: http://localhost:8085/deleteinstances
 - POST, full reset: http://localhost:8085/deleteall
 - PUT, create/update a policy type: http://localhost:8085/policytype?id=&lt;policytypeid&gt;
 - DELETE, delete a policy type: http://localhost:8085/policytype?id=&lt;policytypeid&gt;
 - GET, list of policy type id: http://localhost:8085/policytypes
 - POST, force a specific response code for an A1 operation: http://localhost:8085/forceresponse?responsecode=&lt;http-code&gt;
 - POST, force delayed response of all A1 operations: http://localhost:8085/forcedelay?delay=&lt;seconds&gt;
 - PUT, set status and optional reason, delete and timestamp: http://localhost:8085/status?status=&lt;status&gt;&ampreason=&lt;reason&gt;[&ampdeleted=&lt;boolean&gt;][&ampcreated\_at=&lt;timestamp&gt;]
 - POST, send status for policy: http://localhost:8085/sendstatus?policyid=&lt;policyid&gt;
 - GET a counter: http://localhost:8085/counter/&lt;counter-name&gt;
   (counter-name: 'num\_instances', 'num\_types' or 'interface')

# Supported operations in simulator A1 Standard 1.1.3

URIs for A1:
 - GET all policy identities http://localhost:8085/A1-P/v1/policies
 - PUT a policy instance(create or update it): http://localhost:8085/A1-P/v1/policies/{policyId}
 - GET a policy: http://localhost:8085/A1-P/v1/policies/{policyId}
 - DELETE a policy instance: http://localhost:8085/A1-P/v1/policies/{policyId}
 - GET a policy status: http://localhost:8085/A1-P/v1/policies/{policyid}
<br>Swagger UI at:`http://localhost:8085/A1-P/v1/ui/`

URIs for admin operations:
 - GET, a basic healthcheck: http://localhost:8085/
 - GET, a list of all supported interfaces: http://localhost:8085/container\_interfaces
 - POST, delete all policy instances: http://localhost:8085/deleteinstances
 - POST, full reset: http://localhost:8085/deleteall
 - POST, force a specific response code for an A1 operation: http://localhost:8085/forceresponse?responsecode=&lt;http-code&gt;
- POST, force delayed response of all A1 operations: http://localhost:8085/forcedelay?delay=&lt;seconds&gt;
 - PUT, set status and optional reason: http://localhost:8085/status?status=&lt;status&gt;&ampreason=&lt;reason&gt;
 - POST, send status for policy: http://localhost:8085/sendstatus?policyid=&lt;policyid&gt;
 - GET a counter: http://localhost:8085/counter/&lt;counter-name&gt;
   (counter-name: 'num\_instances', 'num\_types'(always 0) or 'interface')


# Supported operations in simulator 1.1.x-alpha.2

 The available requests and the addresses are currently:
 - GET all policy identities (respectively for a policy type if query parameter used): http://localhost:8085/A1-P/v1/policies?policyTypeId={policyTypeId}
 - PUT a policy instance(create or update it): http://localhost:8085/A1-P/v1/policies/{policyId}?policyTypeId={policyTypeId}
 - GET a policy: http://localhost:8085/A1-P/v1/policies/{policyId}
 - DELETE a policy instance: http://localhost:8085/A1-P/v1/policies/{policyId}
 - GET a policy status: http://localhost:8085/A1-P/v1/policystatus
 - GET all policy types: http://localhost:8085/A1-P/v1/policytypes
 - GET the schemas for a policy type: http://localhost:8085/A1-P/v1/policytypes/{policyTypeId}

Nota Bene: It could happen that this page is not updated as soon as the yaml file is. The yaml file can be found under /near-rt-ric-simulator/a1-openapi.yaml.

Additionally, there are requests that are defined in main.py as an administrative API. The goal is to handle information that couldn't be handled using the A1 interface. The available requests and the addresses are currently:
 - GET, a basic healthcheck: http://localhost:8085/
 - PUT a policy type: http://localhost:8085/policytypes/{policyTypeId}
 - DELETE a policy type: http://localhost:8085/policytypes/{policyTypeId}
 - DELETE all policy instances: http://localhost:8085/deleteinstances
 - DELETE all policy types: http://localhost:8085/deletetypes
 - PUT a status to a policy instance with an enforceStatus parameter only: http://localhost:8085/{policyId}/{enforceStatus}
 - PUT a status to a policy instance with both enforceStatus and enforceReason: http://localhost:8085/{policyId}/{enforceStatus}/{enforceReason}

The backend server publishes live API documentation at the URL `http://localhost:8085/A1-P/v1/ui/`

# Configuring the simulator
A env variable, A1\_VERSION need to be passed to the container at start to select the desired interface version. The variable shall be set to one of the version-ids shown in the table in the first section. For example A1\_VERSIION=STD\_1.1.3.
In docker run the full command could look like this 'docker run -it -p 8085:8085 -e A1\_VERSION=STD\_1.1.3 a1test' where the variable is set with the '-e' flag.

# Updating the openapi specs
The openapi specifications are stored in the 'api/&lt;version&gt;/'. If adding/replacing with a new file, make sure to copy the 'operationId' parameter for each operation to the new file.

# Start and test of the simulator
First, download the sim/a1-interface repo on gerrit:
git clone "https://gerrit.o-ran-sc.org/oransc/sim/a1-interface"

Goto the main directory, 'a1-interface/near-rt-ric-simulator'.
There is a folder 'test/&lt;version&gt;/' for each supported simulator version. This folder contains a script to build and start the simulator (as a container in interactive mode), a script for basic testing as well as json files for the test script.

Go to the test folder of the selected version, 'test/&lt;version&gt;/.

Build and start the simulator container using: ./build\_and\_start.sh
This will build and start the container in interactive mode. The built container only resides in the local docker repository.
Note, the default port is 8085 which can be easily changed in the the script above as well as in the test script.

In a second terminal, go to the same folder and run the basic test script, basic\_test.sh or commands.sh depending on version.
This script runs a number of tests towards the simulator to make sure it works properply.

Only for version 1.1.x-alpha.2
Let the simulator run in one terminal; in another terminal, one can run the command ./commands.sh. It contains the main requests, and will eventually leave the user with a policy type STD\_QoSNudging\_0.2.0 and a policy instance pi1 with an enforceStatus set to NOT\_ENFORCED and an enforce Reason set to 300.
All the response codes should be 20X, otherwise something went wrong.

## License

Copyright (C) 2019 Nordix Foundation.
Licensed under the Apache License, Version 2.0 (the "License")
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

For more information about license please see the [LICENSE](LICENSE.txt) file for details.
