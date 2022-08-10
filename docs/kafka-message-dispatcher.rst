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

The O-RAN SC Kafka Message Dispatcher is an extension for A1 simulator. It creates an external web server building RESTful API. It is capable of recieving Rest calls from the northbound simulator version STD_2.0.0 and responses back to it.

The internal functionality of the dispatcher module is basically to publish kafka messages to the target-request-topic and consume from related response-topic. This mapping is provided in the below format. The logic is based on two-way synchronous communication between dispatcher-module and kafka-cluster. The time out is currently 30 seconds but it is a parametric value and can be changed as per need in the start script of A1 sim.

Policy-type to kafka-cluster-request/response topic mapping:

.. csv-table::
   :header: "API name", "|yaml-icon|"
   :widths: 10,5

   "The mapping file:", ":download:`link <../near-rt-ric-simulator/test/KAFKA_DISPATCHER/resources/policytype_to_topicmap.json>`"


The details of API definitions are being explained below:

See `Kafka Message Dispatcher API <./KAFKA_DISPATCHER_api.html>`_ for full details of the API.

The API is also described in YAML:


.. csv-table::
   :header: "API name", "|yaml-icon|"
   :widths: 10,5

   "Kafka Message Dispatcher API", ":download:`link <../near-rt-ric-simulator/test/KAFKA_DISPATCHER/api/KAFKA_DISPATCHER_api.yaml>`"

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
