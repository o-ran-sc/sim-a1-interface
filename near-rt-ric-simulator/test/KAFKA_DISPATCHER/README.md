# O-RAN-SC Kafka Dispatcher Module extension for Near-RealTime RIC Simulator

The O-RAN SC dispatcher module is an extension for Near-RealTime RIC simulator. It creates a web server building RESTful APIs. It is capable of recieving Rest calls from the northbound simulator version and respond back to it.

The kafka dispatcher module supports GET, PUT and DELETE operations (version of the open API yaml file\):

| Yaml file version          |     Version id      |
| -------------------------- |-------------------- |
| KAFKA_DISPATCHER_api.yaml  |      0.0.1          |

The overall folder structure is \(relative to the location of this README file\):

| Dir              | Description |
| ---------------- | ----------- |
|.                 |Dockerfile, tox.ini and README |
|api               |The open api yaml |
|src               |Python source code |
|certificate       |A self-signed certificate and a key |
|docs              |Auto generated API descriptions in HTML format |

The dispatcher module handles the requests that are defined in the open API yaml file. All these requests are implemented in the dispatcher.py file in the src folder. In addition, a number of administrative functions are also supported and implemented by the main.py in the source folder.

The section below outlines the supported open api rest-based operations as well as the adminstrative operations.

# Ports and certificates

The dispatcher module normally opens the port 7075 for http. If a certificate and a key are provided the kafka dispatcher module will open port 7175 for https instead. The port 7175 is only opened if a valid certificate and key is found.
The certificate and key shall be placed in the same directory and the directory shall be mounted to /usr/src/app/cert in the container.

| Port     | Protocol |
| -------- | ----- |
| 7075     | http  |
| 7175     | https |

The directory certificate contains a self-signed cert. Use the script generate_cert_and_key.sh to generate a new certificate and key. The password of the certificate must be set 'test'.
The same urls are availables on both the http port 7075 and the https port 7175. If using curl and https, the flag -k shall be given to make curl ignore checking the certificate.

# Supported operations in Kafka Dispatcher Module 0.0.1


For the complete yaml specification, see [openapi.yaml](../api/KAFKA_DISPATCHER_api.yaml)

URIs for server:

| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET, Get the kafka request and response topic map corresponding to policy type | localhost:7075/policytypetotopicmapping/ANR |
|  GET, Dispatch policy status query opertion as kafka message to kafka cluster | localhost:7075/policytypes/ANR/kafkadispatcher/alpha/status |
|  PUT, Dispatch create and update operation as kafka message to kafka cluster | localhost:7075/policytypes/ANR/kafkadispatcher/alpha |
|  DELETE, Dispatch policy delete opertion as kafka message to kafka cluster | localhost:7075/policytypes/ptype1/kafkadispatcher/alpha |

URIs for admin operations:

| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET, Get status of dispatcher module | http://localhost:7075/ |
|  POST, Force a specific response code for all dispatcher module operations | localhost:7075/dispatcheradmin/forceresponse?code=500 |
|  POST, Reset force response code | localhost:7075/dispatcheradmin/forceresponse |
|  POST, Force delayed response of all dispatcher module operations | localhost:7075/dispatcheradmin/forcedelay?delay=5 |
|  POST, Reset force delayed response | localhost:7075/dispatcheradmin/forcedelay |


## License

Copyright (C) 2022 Nordix Foundation.
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
