.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2022 Nordix

.. |nbsp| unicode:: 0xA0
   :trim:

.. |nbh| unicode:: 0x2011
   :trim:

.. |yaml-icon| image:: ./images/yaml_logo.png
                  :width: 40px

========================
Kafka Message Dispatcher
========================

API Documentation
=================

The O-RAN SC Kafka Message Dispatcher is a specific implementation of an A1 Simulator ref:`calloutserver`, which further redirects A1 Policy operations to a Kafka message topic, to be consumed by an external function. 

A1 Policy are redirected as Kafka messages to a configured Kafka Topic to an external receiver, then responses from the external receiver are collected from another configured Kafka Topic. This provides a Kafka-based request-response abstraction for adding supplemental simulator behavior for particular A1 Policy Types. After a request message is sent, a response message will be expected within some configurable timeout interval (default: 30 sec). The topics to be used for particular A1 Policy Types is configured using a JSON map (Example: `policytype_to_topicmap.json <../near-rt-ric-simulator/test/KAFKA_DISPATCHER/resources/policytype_to_topicmap.json>` 

**Note:** As with other A1 Simulator call-out servers, the Kafka message dispatcher functionality is only available for *'STD_2.0.0'* version simulators.

The Kafka message dispatcher exposes a 'Kafka Message Dispatcher' REST API. This internal API is invoked directly by the A1 Simulator, and is not intended to be used by any other client.  This API is documented in `Kafka Message Dispatcher API (HTML)<./KAFKA_DISPATCHER_api.html>`_ and in OpenAPI YAML format: 

.. csv-table::
   :header: "API name", "|yaml-icon|"
   :widths: 10,5

   "Kafka Message Dispatcher API", ":download:`link <../near-rt-ric-simulator/test/KAFKA_DISPATCHER/api/KAFKA_DISPATCHER_api.yaml>`"

The Kafka message dispatcher also exposes an 'Admin API' to manipulate the behavior of the Kafka message dispather itself. The 'Kafka Message Dispatcher Admin API' is documented below: 

Admin Functions
================

Health Check
------------

GET
+++

Returns the status of the Kafka Message Dispatcher.

**URL path:**
 /

**Parameters:**
  None.

**Responses:**
  200:
    OK

**Examples:**

**Call**: ::

  curl -X GET "http://localhost:7075/"

**Result**:

200: ::

  OK


Response manipulation
---------------------
It is possible to manipulate the response of all operations on the Kafka Message Dispatcher module

POST
++++

Force a specific response code for the all (the next) Kafka Message Dispatcher module operations. Unless it is reset, it will always respond the same response code back.

**URL path:**

/dispatcheradmin/forceresponse?code=<http-response-code>

**Parameters:**

code: (*Required*)

The HTTP response code to return.

**Responses:**

200:

Force response code: <expected code> set for all all dispatcher response until it is resetted

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:7075/dispatcheradmin/forceresponse?code=500"

**Result**:

200: ::

  Force response code: 500 set for all dispatcher response until it is resetted


Reset response-manipulation
---------------------------
It is possible to reset the response manipulation on the Kafka Message Dispatcher module

POST
++++

Clears specific response code for all (the next) Kafka Message Dispatcher module operation.

**URL path:**

/dispatcheradmin/forceresponse

**Parameters:**

code: (*Required*)

The HTTP response code to return.

**Responses:**

200:

Force response code has been resetted for dispatcher responses

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:7075/dispatcheradmin/forceresponse"

**Result**:

200: ::

  Force response code has been resetted for dispatcher responses


Response time manipulation
--------------------------
It is possible to set a period of time to delay response time.

POST
++++

Force delayed response of all dispatcher responses. The setting will remain until the delay is cleared.

**URL path:**

/dispatcheradmin/forcedelay?delay=<delay-time-seconds>

**Parameters:**

delay: (*Required*)

The time in seconds to delay all responses.

**Responses:**

200:

Force delay: <expected_delay> sec set for all dispatcher responses until it is resetted

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:7075/dispatcheradmin/forcedelay?delay=5"

**Result**:

200: ::

  Force delay: 5 sec set for all dispatcher responses until it is resetted


Reset response time manipulation
--------------------------------
It is also possible to reset delay response time.

POST
++++

The setting will clear the delay.

**URL path:**

/dispatcheradmin/forcedelay

**Parameters:**

None.

The time in seconds to delay all responses.

**Responses:**

200:

Force delay has been resetted for all dispatcher responses

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:7075/dispatcheradmin/forcedelay"

**Result**:

200: ::

  Force delay has been resetted for all dispatcher responses
