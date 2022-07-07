.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2022 Nordix

.. |nbsp| unicode:: 0xA0
   :trim:

.. |nbh| unicode:: 0x2011
   :trim:

=====================
Callout Server
=====================

API Documentation
=================

The O-RAN SC external server is an extension for Near-RealTime RIC simulator. It creates an external web server building RESTful API. It is capable of recieving Rest calls from the northbound simulator version STD_2.0.0 and responses back to it.

The details of API definitions are being explained below:

.. Generates content from EXT_SRV_api.yaml
.. openapi:: ../near-rt-ric-simulator/test/EXT_SRV/api/EXT_SRV_api.yaml


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
