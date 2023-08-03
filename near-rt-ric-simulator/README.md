# O-RAN-SC A1 Simulator

The O-RAN SC A1 simulator simulates the A1 as an generic REST API which can receive and send northbound messages. The simulator validates the payload and applies policy.

The simulator supports multiple A1 interface versions (version of the open API yaml file\):

| Yaml file version     | Version id|
| --------------------- | ------------------- |
| OSC 2.1.0,            |      OSC\_2.1.0     |
| A1 Standard 1.1.3,    |      STD\_1.1.3     |
| A1 Standard 2.0.0,    |      STD\_2.0.0     |

All versions are supported by the same container, see section 'Configuring the simulator' below for details about how to the start the simulator with the intended version id.

The overall folder structure is \(relative to the location of this README file\):

| Dir              | Description |
| ---------------- | ----------- |
|.                 |Dockerfile and README |
|api               |The open api yaml for each supported version |
|src               |Python source code for each supported version |
|test              |Basic test using script|
|tests             |Basic test using pytest unit test|
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
|  PUT, deliver data produced by data producer | http://localhost:8085/data-delivery json payload = {"job":"101",    "payload":"another payload"}|

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
|  Turn on http header and payload logging | http://localhost:8085payload_logging/on |
|  Turn off http header and payload logging | http://localhost:8085payload_logging/off |

# Supported operations in simulator A1 Standard 1.1.3

For the complete yaml specification, see [STD_A1.yaml](../near-rt-ric-simulator/api/STD_1.1.3/STD_A1.yaml).

URIs for A1:

| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET all policy identities | http://localhost:8085/A1-P/v1/policies |
|  PUT a policy instance(create or update it) | http://localhost:8085/A1-P/v1/policies/{policyId} |
|  GET a policy | http://localhost:8085/A1-P/v1/policies/{policyId} |
|  DELETE a policy instance | http://localhost:8085/A1-P/v1/policies/{policyId} |
|  GET a policy status | http://localhost:8085/A1-P/v1/policies/{policyid}/status |

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
|  Turn on http header and payload logging | http://localhost:8085payload_logging/on |
|  Turn off http header and payload logging | http://localhost:8085payload_logging/off |

# Supported operations in simulator A1 Standard 2.0.0

For the complete yaml specification, see [ORAN_A1-p_V2.0.0_api.yaml](../near-rt-ric-simulator/api/STD_2.0.0/ORAN_A1-p_V2.0.0_api.yaml).

URIs for A1:

| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET all policy type identities | http://localhost:8085/A1-P/v2/policytypes |
|  GET a policy type | http://localhost:8085/A1-P/v2/policytypes/{policyTypeId} |
|  GET all policy identities | http://localhost:8085/A1-P/v2/policytypes/{policyTypeId}/policies |
|  PUT a policy instance(create or update it) | http://localhost:8085/A1-P/v2/policytypes/{policyTypeId}/policies/{policyId} |
|  GET a policy | http://localhost:8085/A1-P/v2/policytypes/{policyTypeId}/policies/{policyId} |
|  DELETE a policy instance | http://localhost:8085/A1-P/v2/policytypes/{policyTypeId}/policies/{policyId} |
|  GET a policy status | http://localhost:8085/A1-P/v2/policytypes/{policyTypeId}/policies/{policyid}/status |

Swagger UI at: http://localhost:8085/A1-P/v2/ui/

For the documentation of the admin API, see [A1 Standard 2.0.0](https://docs.o-ran-sc.org/projects/o-ran-sc-sim-a1-interface/en/latest/simulator-api.html#a1-standard-2-0-0).

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
|  PUT, set status and optional reason | http://localhost:8085/status?status=&lt;status&gt;[&amp;reason=&lt;reason&gt;] |
|  POST, send status for policy | http://localhost:8085/sendstatus?policyid=&lt;policyid&gt; |
|  POST, deliver data | http://localhost:8085/datadelivery |
|  GET a counter <br> (counter-name: 'num\_instances', 'num\_types'(always 0), 'interface', 'remote\_hosts' or 'datadelivery') | http://localhost:8085/counter/&lt;counter-name&gt; |
|  Turn on http header and payload logging | http://localhost:8085payload_logging/on |
|  Turn off http header and payload logging | http://localhost:8085payload_logging/off |


# Configuring the simulator
An env variable, A1\_VERSION need to be passed to the container at start to select the desired interface version. The variable shall be set to one of the version-ids shown in the table in the first section. For example A1\_VERSIION=STD\_1.1.3.

An env variable, REMOTE_HOSTS_LOGGING, can be set (any value is ok) and the the counter remote\_hosts will log the host names of all remote hosts that has accessed the A1 URIs. If host names cannot be resolved, the ip address of the remote host is logged instead. This logging is default off so must be configured to be enabled. If not configured, the counter remote\_hosts will return a fixed text indicating that host name logging is not enabled. Use this feature with caution, remote host lookup may take time in certain environments.

And optional env variable, DUPLICATE_CHECK, can be set to '1' to turn on duplicate check of policy json. A duplicate policy is when the policy json is exactly same as for a different policy id of the same type.  This function is default set off if the variable is not set at all or set to '0'.

The simulator can also run using the https protocol. The enable https, a valid certificate and key need to provided. There is self-signed certificate available in the certificate dir and that dir shall be mounted to the container to make it available

By default, this image has default certificates under /usr/src/app/cert
file "cert.crt" is the certificate file
file "key.crt" is the key file
file "generate_cert_and_key.sh" is a shell script to generate certificate and key
file "pass" stores the password when you run the shell script

Start the a1-interface container without specifing external certificates:

'docker run --rm -it -p 8085:8085 -p 8185:8185 -e A1\_VERSION=STD\_1.1.3 -e REMOTE_HOSTS_LOGGING=1 -e DUPLICATE_CHECK=0 a1test'

It will listen to https 8185 port(using default certificates) by default.
Http can be enabled on port 8085 using an environment variable "ALLOW_HTTP".
If this environment variable is left out or set to false, the nginx server will send
"444 Connection Closed Without Response" when making a call using http.
Example command to enable http:

'docker run -it -p 8085:8085 -p 8185:8185 -e A1\_VERSION=OSC\_2.1.0 -e ALLOW_HTTP=true -e DUPLICATE_CHECK=0 a1test'

This certificates/key can be overriden by mounting a volume when using "docker run" or "docker-compose"
In 'docker run', use field:
--volume "$PWD/certificate:/usr/src/app/cert" a1test
In 'docker-compose.yml', use field:
volumes:
      - ./certificate:/usr/src/app/cert:ro

In docker run the full command could look like this:<br>
'docker run -it -p 8085:8085 -p 8185:8185 -e A1\_VERSION=STD\_1.1.3 -e ALLOW_HTTP=true -e REMOTE_HOSTS_LOGGING=1 -e DUPLICATE_CHECK=0 --volume /PATH_TO_CERT_DIR/certificate:/usr/src/app/cert a1test'

http port 8085 and https port 8185

The variable for A1 version is set with the '-e' flag.

With logging of remote host enabled "-e REMOTE_HOSTS_LOGGING=1 "

With policy json duplicate check set to off (0)

With certificate dir mounted  "--volume /PATH_TO_CERT_DIR/certificate:/usr/src/app/cert"

# Updating the openapi specs
The openapi specifications are stored in the 'api/&lt;version&gt;/'. If adding/replacing with a new file, make sure to copy the 'operationId' parameter for each operation to the new file.

# Start and test of the simulator
See also 'Basic test and code coverage'.

First, download the sim/a1-interface repo on gerrit:
git clone "https://gerrit.o-ran-sc.org/oransc/sim/a1-interface"

Goto the main directory, 'a1-interface/near-rt-ric-simulator'.
There is a folder 'test/&lt;version&gt;/' for each supported simulator version. This folder contains a script to build and start the simulator (as a container in interactive mode), a script for basic testing as well as json files for the test script.

Go to the test folder of the selected version, 'test/&lt;version&gt;/.

Note that test can be performed both using the nonsecure http port and the secure https port.

Build and start the simulator containers: STD_1.1.3 and OSC_2.1.0, using:

./build_and_start.sh duplicate-check|ignore-duplicate

Build and start the simulator container version STD_2.0.0, using two alternatives: ext-srv or kafka-srv. However, both can not be used at the same time to start A1 sim.

In order to start with ext-srv:
./build_and_start.sh duplicate-check|ignore-duplicate ext-srv|ext-srv-secure|ignore-ext-srv

In order to start with kafka-srv:
./build_and_start.sh duplicate-check|ignore-duplicate kafka-srv|kafka-srv-secure publish-resp|ignore-publish

STD_2.0.0 version is now including an external server that is a Python server building RESTful API. The external server supports HTTP/HTTPS protocols.
The description of the start parameters are explained below:
ext-srv: Runs external server that supports HTTP protocol only.
ext-srv-secure: Runs external server that supports HTTPS protocol as well.
ignore-ext-srv: Ignores external server to run.

STD_2.0.0 version also includes an kafka message dispatcher that is a Python server building RESTful APIs. The kafka server supports HTTP/HTTPS protocols.
The description of the start parameters are explained below:
kafka-srv: Runs kafka server that supports HTTP protocol only.
kafka-srv-secure: Runs kafka server that supports HTTPS protocol as well.
publish-resp: The flag controls the dispatcher module to decide auto responding to each requests for test purposes only.
ignore-publish: If the A1 sim is being started using ignore flag, then the dispatcher module will look for a respone message published by south-bound module.

This will build and start the container in interactive mode. The built container only resides in the local docker repository.
Note, the default port is 8085 for http and 8185 for https. When running the simulator as a container, the defualt ports can be re-mapped to any port on the localhost.

In a second terminal, go to the same folder and run the basic test script, basic_test.sh nonsecure|secure or commands.sh nonsecure|secure duplicate-check|ignore-duplicate for STD_1.1.3 and OSC_2.1.0 versions.

For the STD_2.0.0 version, in a second terminal, go to the same folder and run the basic test script for external server activated case:
./basic_test.sh nonsecure|secure duplicate-check|ignore-duplicate ext-srv|ext-srv-secure|ignore-ext-srv
The description of the test script parameters are explained below:
nonsecure|secure: Runs test cases with either support of HTTP/HTTPS protocol.
duplicate-check|ignore-duplicate: Runs test cases with either support of duplicate/ignore-duplicate flag for the policies.
ext-srv|ext-srv-secure|ignore-ext-srv: If the simulator started with ext-srv or ext-srv-secure parameter, then one of these options can be used. Otherwise, ignore-ext-srv parameter should be used.

For the STD_2.0.0 version, in a second terminal, go to the same folder and run the basic test script for kafka dispatcher server activated case:
./basic_test.sh nonsecure|secure duplicate-check|ignore-duplicate ext-srv|ext-srv-secure|ignore-ext-srv
The description of the test script parameters are explained below:
nonsecure|secure: Runs test cases with either support of HTTP/HTTPS protocol.
duplicate-check|ignore-duplicate: Runs test cases with either support of duplicate/ignore-duplicate flag in accordance with the one which used while starting A1 sim.
ext-srv|ext-srv-secure|ignore-ext-srv: If the simulator started with kafka-srv or kafka-srv-secure parameter, then ignore-ext-srv option should be used.

Note that the arg for duplicate check must match in both scripts.
This script runs a number of tests towards the simulator to make sure it works properply.

# Basic test and code coverage

Basic test, or unit test, using a python script is also supported. This test basically the same thing as the bash script mentioned in the section above. Follow the instruction of how to clone the repo described in that section.
Only http is tested as the internal flask server is only using http (https is part of the webserver inteface).

Navigate to 'near-rt-ric-simulator/tests'. Choose the version to test and use that file for test.

Use 'python3 -m pytest \<filename>' to run unit test only with no coverage check. Before running that command, the dependencies which are pytest and connexion should be installed in your virtual environment. If the latest connexion version arises DeprecationWarning, you may try to install connexion with version 2.6.0.

Or use 'coverage run  -m pytest \<filename>' to run unit test and produce coverage data.

List coverage data by 'coverage report -m --include=../../*' - the include flag makes the list to only contain coverage data from the simulator python file.

To use the 'coverage' cmd, coverage need to be installed use 'pip install coverage'

## License

Copyright (C) 2023 Nordix Foundation.
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
