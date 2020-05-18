# O-RAN-SC Near-RealTime RIC Simulator

The O-RAN SC Near-RealTime RIC simulates the A1 as an generic REST API which can receive and send northbound messages. The simulator validates the payload and applies policy.

The simulator supports multiple A1 interface versions (version of the open API yaml file\):
| Yaml file version     | Version id|
| --------------------- | ------------------- |
| OSC 2.1.0,            |      OSC\_2.1.0     |
| A1 Standard 1.1.3,    |      STD\_1.1.3     |
| 1.1.x-alpha.2 ,       |      1.1.x-alpha.2  |

All versions are supported by the same container, see section 'Configuring the simulator' below for details about how to the start the simulator with the intended version id.

The overall folder structure is \(relative to the location of this README file\):
| Dir              | Description |
| ---------------- | ----------- |
|.                 |Dockerfile and README |
|api               |The open api yaml for each supported version |
|src               |Python source code for each supported version |
|test              |Basic test |
|certificate       |A self-signed certificate and a key

The simulator handles the requests that are defined in the A1 open API yaml file. All these requests are implemented in the a1.py file in the source folder. In addition, a number of administrative functions are also supported and implemented by the main.py in the source folder.

The section below outlines the supported open api REST operations as well as the adminstrative REST operations. For the
documentation of the common parts in the admin API, see [Common Functions](https://docs.o-ran-sc.org/projects/o-ran-sc-sim-a1-interface/en/latest/simulator-api.html#common-functions).

# Ports and certificates

The simulator normally opens the port 8085 for http. If a certificate and a key are provided the simulator will open port 8185 for https instead. The port 8185 is only opened if a valid certificate and key is found.
The certificate and key shall be placed in the same dir and the dir shall be mounted to /usr/src/app/cert in the container.

| Port     | Protocol |
| -------- | ----- |
| 8085     | http  |
| 8185     | https |

The dir certificate contains a self-signed cert. Use the script generate_cert_and_key.sh to generate a new certificate and key. The password of the certificate must be set 'test'.
The same urls are availables on both the http port 8085 and the https port 8185. If using curl and https, the flag -k shall be given to make curl ignore checking the certificate.

# Supported operations in simulator OSC 2.1.0

For the complete yaml specification, see [openapi.yaml](../near-rt-ric-simulator/api/OSC_2.1.0/openapi.yaml).

URIs for A1:
| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET, do a healthcheck |  http://localhost:8085/a1-p/healthcheck |
|  GET, get all policy type ids | http://localhost:8085/a1-p/policytypes |
|  DELETE, delete a policy type | http://localhost:8085/a1-p/policytypes/{policy\_type\_id} |
|  GET, get a policy type | http://localhost:8085/a1-p/policytypes/{policy\_type\_id} |
|  PUT, create/update a policy type | http://localhost:8085/a1-p/policytypes/{policy\_type\_id} |
|  GET, get all policy ids for a type | http://localhost:8085/a1-p/policytypes/{policy\_type\_id}/policies |
|  DELETE, delete a policy | http://localhost:8085/a1-p/policytypes/{policy\_type\_id}/policies/{policy\_instance\_id} |
|  GET, get a policy | http://localhost:8085/a1-p/policytypes/{policy\_type\_id}/policies/{policy\_instance\_id} |
|  PUT, create/update a policy | http://localhost:8085/a1-p/policytypes/{policy\_type\_id}/policies/{policy\_instance\_id} |
|  GET, get policy status | http://localhost:8085/a1-p/policytypes/{policy\_type\_id}/policies/{policy\_instance\_id}/status |

Swagger UI at: http://localhost:8085/ui/

For the documentation of the admin API, see [OSC_2.1.0](https://docs.o-ran-sc.org/projects/o-ran-sc-sim-a1-interface/en/latest/simulator-api.html#osc-2-1-0).

URIs for admin operations:
| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET, a basic healthcheck | http://localhost:8085/ |
|  GET, a list of all supported interfaces | http://localhost:8085/container\_interfaces |
|  POST, delete all policy instances | http://localhost:8085/deleteinstances |
|  POST, full reset | http://localhost:8085/deleteall |
|  PUT, create/update a policy type | http://localhost:8085/policytype?id=&lt;policytypeid&gt; |
|  DELETE, delete a policy type | http://localhost:8085/policytype?id=&lt;policytypeid&gt; |
|  GET, list of policy type id | http://localhost:8085/policytypes |
|  POST, force a specific response code for an A1 operation | http://localhost:8085/forceresponse?code=&lt;http-code&gt; |
|  POST, force delayed response of all A1 operations | http://localhost:8085/forcedelay?delay=&lt;seconds&gt; |
|  PUT, set status and optional reason, delete and timestamp | http://localhost:8085/status?status=&lt;status&gt;&amp;reason=&lt;reason&gt;[&amp;deleted=&lt;boolean&gt;][&amp;created\_at=&lt;timestamp&gt;]  |
|  GET a counter  <br> (counter-name: 'num\_instances', 'num\_types', 'interface' or 'remote\_hosts') | http://localhost:8085/counter/&lt;counter-name&gt; |


# Supported operations in simulator A1 Standard 1.1.3

For the complete yaml specification, see [STD_A1.yaml](../near-rt-ric-simulator/api/STD_1.1.3/STD_A1.yaml).

URIs for A1:
| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET all policy identities | http://localhost:8085/A1-P/v1/policies |
|  PUT a policy instance(create or update it) | http://localhost:8085/A1-P/v1/policies/{policyId} |
|  GET a policy | http://localhost:8085/A1-P/v1/policies/{policyId} |
|  DELETE a policy instance | http://localhost:8085/A1-P/v1/policies/{policyId} |
|  GET a policy status | http://localhost:8085/A1-P/v1/policies/{policyid} |
Swagger UI at: http://localhost:8085/A1-P/v1/ui/

For the documentation of the admin API, see [A1 Standard 1.1.3](https://docs.o-ran-sc.org/projects/o-ran-sc-sim-a1-interface/en/latest/simulator-api.html#a1-standard-1-1-3).

URIs for admin operations:
| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET, a basic healthcheck | http://localhost:8085/ |
|  GET, a list of all supported interfaces | http://localhost:8085/container\_interfaces |
|  POST, delete all policy instances | http://localhost:8085/deleteinstances |
|  POST, full reset | http://localhost:8085/deleteall |
|  POST, force a specific response code for an A1 operation | http://localhost:8085/forceresponse?code=&lt;http-code&gt; |
|  POST, force delayed response of all A1 operations | http://localhost:8085/forcedelay?delay=&lt;seconds&gt; |
|  PUT, set status and optional reason | http://localhost:8085/status?status=&lt;status&gt;[&amp;reason=&lt;reason&gt;] |
|  POST, send status for policy | http://localhost:8085/sendstatus?policyid=&lt;policyid&gt; |
|  GET a counter <br> (counter-name: 'num\_instances', 'num\_types'(always 0), 'interface' or 'remote\_hosts') | http://localhost:8085/counter/&lt;counter-name&gt; |



# Supported operations in simulator 1.1.x-alpha.2

For the complete yaml specification, see [a1-openapi.yaml](../near-rt-ric-simulator/api/1.1.x-alpha.2/a1-openapi.yaml).

The available requests and the addresses are currently:
| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET all policy identities (respectively for a policy type if query parameter used) | http://localhost:8085/A1-P/v1/policies?policyTypeId={policyTypeId} |
|  PUT a policy instance(create or update it) | http://localhost:8085/A1-P/v1/policies/{policyId}?policyTypeId={policyTypeId} |
|  GET a policy | http://localhost:8085/A1-P/v1/policies/{policyId} |
|  DELETE a policy instance | http://localhost:8085/A1-P/v1/policies/{policyId} |
|  GET a policy status | http://localhost:8085/A1-P/v1/policystatus |
|  GET all policy types | http://localhost:8085/A1-P/v1/policytypes |
|  GET the schemas for a policy type | http://localhost:8085/A1-P/v1/policytypes/{policyTypeId} |

Nota Bene: It could happen that this page is not updated as soon as the yaml file is. The yaml file can be found under /near-rt-ric-simulator/a1-openapi.yaml.

For the documentation of the admin API, see [1.1.x-alpha.2](https://docs.o-ran-sc.org/projects/o-ran-sc-sim-a1-interface/en/latest/simulator-api.html#x-alpha-2).

Additionally, there are requests that are defined in main.py as an administrative API. The goal is to handle information that couldn't be handled using the A1 interface. The available requests and the addresses are currently:
| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET, a basic healthcheck | http://localhost:8085/ |
|  PUT a policy type | http://localhost:8085/policytypes/{policyTypeId} |
|  DELETE a policy type | http://localhost:8085/policytypes/{policyTypeId} |
|  DELETE all policy instances | http://localhost:8085/deleteinstances |
|  DELETE all policy types | http://localhost:8085/deletetypes |
|  PUT a status to a policy instance with an enforceStatus parameter only | http://localhost:8085/{policyId}/{enforceStatus} |
|  PUT a status to a policy instance with both enforceStatus and enforceReason | http://localhost:8085/{policyId}/{enforceStatus}/{enforceReason} |
|  GET a counter  <br> (counter-name: 'num\_instances', 'num\_types', 'interface' or 'remote\_hosts') | http://localhost:8085/counter/{counter-name} |

The backend server publishes live API documentation at the URL `http://localhost:8085/A1-P/v1/ui/`

# Configuring the simulator
An env variable, A1\_VERSION need to be passed to the container at start to select the desired interface version. The variable shall be set to one of the version-ids shown in the table in the first section. For example A1\_VERSIION=STD\_1.1.3.
An env variable, REMOTE_HOSTS_LOGGING, can be set (any value is ok) and the the counter remote\_hosts will log the host names of all remote hosts that has accessed the A1 URIs. If host names cannot be resolved, the ip address of the remote host is logged instead. This logging is default off so must be configured to be enabled. If not configured, the counter remote\_hosts will return a fixed text indicating that host name logging is not enabled. Use this feature with caution, remote host lookup may take time in certain environments.
The simulator can also run using the https protocol. The enable https, a valid certificate and key need to provided. There is self-signed certificate available in the certificate dir and that dir shall be mounted to the container to make it available

In docker run the full command could look like this:<br> 'docker run -it -p 8085:8085 -p 8185:8185 -e A1\_VERSION=STD\_1.1.3 -e REMOTE_HOSTS_LOGGING=1 --volume /PATH_TO_CERT_DIR/certificate:/usr/src/app/cert a1test'
http port 8085 and https port 8185
The variable for A1 version is set with the '-e' flag.
With logging of remote host enabled "-e REMOTE_HOSTS_LOGGING=1 "
With certificate dir mounted  "--volume /PATH_TO_CERT_DIR/certificate:/usr/src/app/cert"

# Updating the openapi specs
The openapi specifications are stored in the 'api/&lt;version&gt;/'. If adding/replacing with a new file, make sure to copy the 'operationId' parameter for each operation to the new file.

# Start and test of the simulator
First, download the sim/a1-interface repo on gerrit:
git clone "https://gerrit.o-ran-sc.org/oransc/sim/a1-interface"

Goto the main directory, 'a1-interface/near-rt-ric-simulator'.
There is a folder 'test/&lt;version&gt;/' for each supported simulator version. This folder contains a script to build and start the simulator (as a container in interactive mode), a script for basic testing as well as json files for the test script.

Go to the test folder of the selected version, 'test/&lt;version&gt;/.

Note that test can be performed both using the nonsecure http port and the secure https port.

Build and start the simulator container using: ./build\_and\_start.sh
This will build and start the container in interactive mode. The built container only resides in the local docker repository.
Note, the default port is 8085 for http and 8185 for https. When running the simulator as a container, the defualt ports can be re-mapped to any port on the localhost.

In a second terminal, go to the same folder and run the basic test script, basic\_test.sh nonsecure|secure or commands.sh nonsecure|secure depending on version.
This script runs a number of tests towards the simulator to make sure it works properply.

Only for version 1.1.x-alpha.2
Let the simulator run in one terminal; in another terminal, one can run the command ./commands.sh nonsecure|secure. It contains the main requests, and will eventually leave the user with a policy type STD\_QoSNudging\_0.2.0 and a policy instance pi1 with an enforceStatus set to NOT\_ENFORCED and an enforce Reason set to 300.
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
