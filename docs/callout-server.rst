.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2022 Nordix

.. |nbsp| unicode:: 0xA0
   :trim:

.. |nbh| unicode:: 0x2011
   :trim:

.. |yaml-icon| image:: ./images/yaml_logo.png
                  :width: 40px

.. _calloutserver:

=====================
Callout Server
=====================

API Documentation
=================

The O-RAN SC external call-out server allows behavioral extensions to be added to the A1 Simulator. It creates an external call-out server, which provides a RESTful API. A1 Policy operations, for some A1 Policy Types, can then be redirected to the external call-out server, supporting supplemental simulator behavior for those A1 Policy Types. 

**Note:** call-out server functionality is only available for *'STD_2.0.0'* version simulators.

The external call-out server exposes a 'Callout server API' REST API. This internal API is invoked directly by the A1 Simulator, and is not intended to be used by any other client.  The 'Callout Server API' is documented in `Callout Server API <./EXT_SRV_api.html>`_ and in OpenAPI YAML format:

.. csv-table::
   :header: "API name", "|yaml-icon|"
   :widths: 10,5

   "Callout Server API", ":download:`link <../near-rt-ric-simulator/test/EXT_SRV/api/EXT_SRV_api.yaml>`"

External call-out servers also expose an 'Admin API' to manipulate the behavior of the call-out server itself. The 'Callout Server Admin API' is documented below: 

Admin Functions
================

Health Check
------------

GET
+++

Returns the status of the external server.

**URL path:**
 /

**Parameters:**
  None.

**Responses:**
  200:
    OK

**Examples:**

**Call**: ::

  curl -X GET "http://localhost:9095/"

**Result**:

200: ::

  OK


Delete all policy instances in external server
----------------------------------------------

POST
++++

Delete all policy instances.

**URL path:**

/serveradmin/deleteinstances

**Parameters:**

None.

**Responses:**

200:

All a1 policy instances deleted

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:9095/serveradmin/deleteinstances"

**Result**:

200: ::

  All a1 policy instances deleted


Response manipulation
---------------------
It is possible to manipulate the response of all operations on the external server

POST
++++

Force a specific response code for the all (the next) external server operation. Unless it is reset, it will always respond the same response code back.

**URL path:**

/serveradmin/forceresponse?code=<http-response-code>

**Parameters:**

code: (*Required*)

The HTTP response code to return.

**Responses:**

200:

Force response code: <expected code>  set for all external server response until it is resetted

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:9095/serveradmin/forceresponse?code=500"

**Result**:

200: ::

  Force response code: 500 set for all external server response until it is resetted


Reset response-manipulation
---------------------------
It is possible to reset the response manipulation on the external server

POST
++++

Clears specific response code for all (the next) external server operation.

**URL path:**

/serveradmin/forceresponse?code=<http-response-code>

**Parameters:**

code: (*Required*)

The HTTP response code to return.

**Responses:**

200:

Force response code has been resetted for all external server responses

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:9095/serveradmin/forceresponse?code=500"

**Result**:

200: ::

  Force response code has been resetted for all external server responses


Response time manipulation
--------------------------
It is possible to set a period of time to delay response time.

POST
++++

Force delayed response of all A1 responses. The setting will remain until the delay is set to '0'

**URL path:**

/serveradmin/forcedelay?delay=<delay-time-seconds>

**Parameters:**

delay: (*Required*)

The time in seconds to delay all responses.

**Responses:**

200:

Force delay: <expected_delay> sec set for all external server responses until it is resetted

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:9095/serveradmin/forcedelay?delay=5"

**Result**:

200: ::

  Force delay: 5 sec set for all external server responses until it is resetted


Reset response time manipulation
--------------------------------
It is also possible to reset delay response time.

POST
++++

The setting will clear the delay.

**URL path:**

/serveradmin/forcedelay

**Parameters:**

None.

The time in seconds to delay all responses.

**Responses:**

200:

Force delay has been resetted for all external server responses

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:9095/serveradmin/forcedelay"

**Result**:

200: ::

  Force delay has been resetted for all external server responses
