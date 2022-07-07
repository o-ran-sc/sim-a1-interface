# O-RAN-SC External Server extension for Near-RealTime RIC Simulator

The O-RAN SC external server is an extension for Near-RealTime RIC simulator. It creates an external web server building RESTful API. It is capable of recieving Rest calls from the northbound simulator version and responses back to it.

The external server supports GET, PUT and DELETE operations (version of the open API yaml file\):

| Yaml file version     | Version id          |
| --------------------- | ------------------- |
| EXT_SRV_api.yaml      |      0.0.1          |

The overall folder structure is \(relative to the location of this README file\):

| Dir              | Description |
| ---------------- | ----------- |
|.                 |Dockerfile, tox.ini and README |
|api               |The open api yaml |
|src               |Python source code |
|certificate       |A self-signed certificate and a key |
|docs              |Auto generated API descriptions in HTML format |

The external server handles the requests that are defined in the open API yaml file. All these requests are implemented in the server.py file in the src folder. In addition, a number of administrative functions are also supported and implemented by the main.py in the source folder.

The section below outlines the supported open api rest-based operations as well as the adminstrative operations.

# Ports and certificates

The external server normally opens the port 9095 for http. If a certificate and a key are provided the external server will open port 9195 for https instead. The port 9195 is only opened if a valid certificate and key is found.
The certificate and key shall be placed in the same directory and the directory shall be mounted to /usr/src/app/cert in the container.

| Port     | Protocol |
| -------- | ----- |
| 9095     | http  |
| 9195     | https |

The directory certificate contains a self-signed cert. Use the script generate_cert_and_key.sh to generate a new certificate and key. The password of the certificate must be set 'test'.
The same urls are availables on both the http port 9095 and the https port 9195. If using curl and https, the flag -k shall be given to make curl ignore checking the certificate.

# Supported operations in External Server 0.0.1


For the complete yaml specification, see [openapi.yaml](../api/EXT_SRV_api.yaml)

URIs for server:

| Function              | Path and parameters |
| --------------------- | ------------------- |
|  GET, Get all A1 policy ids | localhost:9095/a1policies |
|  GET, Query for an A1 policy | localhost:9095/a1policy/{a1policyId} |
|  PUT, Create an A1 policy | localhost:9095/a1policy/{a1policyId} |
|  DELETE, Delete an A1 policy | localhost:9095/a1policy/{a1policyId} |

URIs for admin operations:

| Function              | Path and parameters |
| --------------------- | ------------------- |
|  POST, Delete all A1 policy instances | localhost:9095/serveradmin/deleteinstances |
|  POST, Force a specific response code for all A1 operation | localhost:9095/serveradmin/forceresponse?code=500 |
|  POST, Reset force response code | localhost:9095/serveradmin/forceresponse |
|  POST, Force delayed response of all A1 operations | localhost:9095/serveradmin/forcedelay?delay=5 |
|  POST, Reset force delayed response | localhost:9095/serveradmin/forcedelay |


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
