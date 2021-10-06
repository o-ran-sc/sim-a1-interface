.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2021 Nordix

.. _simulator-api:

=============
Simulator API
=============

This document describes the API used to manage policy types and manipulate the simulator.

The simulator supports different versions of the A1 interface. Some functions are common for all versions, and some are
specific for a certain version.

Common Functions
================

Health Check
------------

The status of the simulator.

/
~~

GET
+++

Returns the status of the simulator.

**URL path:**
 /

**Parameters:**
  None.

**Responses:**
  200:
    OK

**Examples:**

**Call**: ::

  curl -X GET "http://localhost:8085/"

**Result**:

200: ::

  OK

Supported Interfaces
--------------------

The simulator can support different versions of the A1 interface. With this API the supported versions can be listed.

/container_interfaces
~~~~~~~~~~~~~~~~~~~~~

GET
+++

Returns the status of the simulator. (Not available for A1 Standard 1.1.3)

**URL path:**

/container_interfaces

**Parameters:**

None.

**Responses:**

200:
    List of supported interfaces.

**Examples:**

**Call**: ::

  curl -X GET "http://localhost:8085/container_interfaces"


**Result**:

200: ::

  Current interface: STD_2.0.0  All supported A1 interface yamls in this container: ['OSC_2.1.0', 'STD_1.1.3', 'STD_2.0.0']

Counters
--------

The simulator keeps counts of different things that can be accessed.

/counter
~~~~~~~~

GET
+++

Get a counter. Counter-name can be one of the following: 'num_instances', 'num_types', 'interface', 'remote_hosts' or 'datadelivery'.

**URL path:**

/counter/{counter-name}

**Parameters:**

None.

**Responses:**

200:

The counter value for the given counter.

**Examples:**

**Call**: ::

  curl -X GET "http://localhost:8085/counter/num_instances"

**Result**:

200: ::

  10


Reset simulator
---------------

There are two ways to reset the simulator, delete all instances or make a complete reset which resets the simulator to its original state.

/deleteinstances
~~~~~~~~~~~~~~~~

POST
++++

Delete all policy instances.

**URL path:**

/deleteinstances

**Parameters:**

None.

**Responses:**

200:

All policy instances deleted.

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:8085/deleteinstances"

**Result**:

200: ::

  All policy instances deleted.

/deleteall
~~~~~~~~~~~~~~~~

POST
++++

Full reset.

**URL path:**

/deleteall

**Parameters:**

None.

**Responses:**

200:

All policy instances and types deleted.

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:8085/deleteall"

**Result**:

200: ::

  All policy instances and types deleted.

200  ::
  All policy instances deleted  (Only for STD_1.1.3 since it has no types)

Response manipulation
---------------------
It is possible to manipulate the response of all operations on the A1 interface (admin interface is not affected)

/forceresponse
~~~~~~~~~~~~~~

POST
++++

Force a specific response code for one (the next) A1 operation. After that response, the reponse code will go back to normal.

**URL path:**

/forceresponse?code=<http-response-code>

**Parameters:**

code: (*Required*)

The HTTP response code to return.

**Responses:**

200:

Force response code:  <expected code> set for one single A1 response

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:8085/forceresponse?code=400"

**Result**:

200: ::

  Force response code:  400 set for one single A1 response

/forcedelay
~~~~~~~~~~~

POST
++++

Force delayed response of all A1 responses. The setting will remain until the delay is set to '0'

**URL path:**

/forcedelay?delay=<delay-time-seconds>

**Parameters:**

delay: (*Required*)

The time in seconds to delay all responses.

**Responses:**

200:

Force delay: <expected delay> sec set for all A1 responses

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:8085/forcedelay?delay=2"

**Result**:

200: ::

  Force delay: 2 sec set for all A1 responses


Configure logging
-----------------
Detailed logging of the http headers and payload are activated by default. However, it is possible to turn this logging on or off.
The 'off' state will only logg ip, url and respose code.

/payload_logging/
~~~~~~~~~~~~~~~~~

POST
++++

Configure detailed logging on or off
**URL path:**

/payload_logging/<state>

**Parameters:**

state: (*Required*)

The state, 'on' or 'off'.

**Responses:**

200:

Force delay: <expected delay> sec set for all A1 responses

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:8085/payload_logging/on"

**Result**:

200: ::

  Payload and header logging set to: on


Version Specific Functions
==========================

The methods available to control the simulator depends on the version of the A1 API the simulator is simulating.

OSC_2.1.0
---------

This section describes the available administrative functions for the OSC_2.1.0 version of A1.

To see the A1 functions for this version, see `OSC_2.1.0 API`_.

.. _OSC_2.1.0 API: https://gerrit.o-ran-sc.org/r/gitweb?p=sim/a1-interface.git;a=blob;f=near-rt-ric-simulator/api/OSC_2.1.0/openapi.yaml



/policytype
~~~~~~~~~~~

PUT
+++

Create a policy type.

**URL path:**

/policytype?id=<policy-type-id>

**Parameters:**

id: (*Required*)

The ID of the policy type.

**Body:** (*Required*)

A JSON object containing the schema for the type.

**Responses:**

200:

Policy type <policy-type-id> is OK.

201:

Policy type <policy-type-id> is OK.

**Examples:**

**Call**: ::

  curl -X PUT "http://localhost:8085/policytype?id=1"
    -H  "Content-Type: application/json"
    -d '{
        "name": "pt1",
        "description": "pt1 policy type",
        "policy_type_id": 1,
        "create_schema": {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "title": "STD_QoSNudging_0.2.0",
          "description": "QoS policy type",
          "type": "object",
          "properties": {
            "scope": {
              "type": "object",
              "properties": {
                "ueId": {
                  "type": "string"
                },
                "qosId": {
                  "type": "string"
                }
              },
              "additionalProperties": false,
              "required": [
                "ueId",
                "qosId"
              ]
            },
            "statement": {
              "type": "object",
              "properties": {
                "priorityLevel": {
                  "type": "number"
                }
              },
              "additionalProperties": false,
              "required": [
                "priorityLevel"
              ]
            }
          }
        }
      }'

**Result**:

201: ::

  Policy type 1 is OK

DELETE
++++++

Delete a policy type.

**URL path:**

/policytype?id=<policy-type-id>

**Parameters:**

id: (*Required*)

The ID of the policy type.

**Responses:**

204:

Policy type <policy-type-id> is OK.

**Examples:**

**Call**: ::

  curl -X DELETE "http://localhost:8085/policytype?id=1"

**Result**:

204



/policytypes
~~~~~~~~~~~~

GET
+++

Get a list of policy types.

**URL path:**

/policytypes

**Parameters:**

None.

**Responses:**

200:

A list of policy types.

**Examples:**

**Call**: ::

  curl -X GET "http://localhost:8085/policytypes"

**Result**:

200: ::

  ["1"]


/status
~~~~~~~

PUT
+++

Set status and optional reason, delete and time stamp.

**URL path:**

/status?policyid=<policyid>&status=<status>&deleted=<value>&created_at=<time-stamp>

**Parameters:**

policyid: (*Required*)

The ID of a policy.

status: (*Required*)

The status of a policy.

deleted: (*Optional*)

True or false for real values, but accepts anything for error testing.

created_at: (*Optional*)

Time stamp for the status.

**Responses:**

200:

Status set to <status> for policy <policy-id>

**Examples:**

**Call**: ::

  curl -X PUT "http://localhost:8085/status?policyid=1&status=Accepted"

**Result**:

200: ::

  Status set to Accepted for policy Policy1.

A1 Standard 1.1.3
-----------------

This section describes the available administrative functions for the A1 Standard 1.1.3 version of A1.

To see the A1 functions for this version, see `A1 Standard 1.1.3 API`_.

.. _A1 Standard 1.1.3 API: https://gerrit.o-ran-sc.org/r/gitweb?p=sim/a1-interface.git;a=blob;f=near-rt-ric-simulator/api/STD_1.1.3/STD_A1.yaml


/status
~~~~~~~

PUT
+++

Set status and optional reason, delete and time stamp.

**URL path:**

/status?policyid=<policyid>&status=<status>&reason=<reason>

**Parameters:**

policyid: (*Required*)

The ID of a policy.

status: (*Required*)

The status of a policy.

reason: (*Optional*)

The reason for the status.

**Responses:**

200:

Status set to <status> for policy <policy-id>

**Examples:**

**Call**: ::

  curl -X PUT "http://localhost:8085/status?policyid=Policy1&status=Accepted"

**Result**:

200: ::

  Status set to Accepted for policy Policy1

/sendstatus
~~~~~~~~~~~

POST
++++

Send status for policy.

**URL path:**

/sendstatus?policyid=<policy-id>

**Parameters:**

policyid: (*Required*)

The ID of the policy to send status for.

**Responses:**

200:

Is a JSON with the response of the actual post request to the callback server, whatever that is.

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:8085/sendstatus?policyid=Policy2"

**Result**:

200


A1 Standard 2.0.0
-----------------

This section describes the available administrative functions for the A1 Standard 2.0.0 version of A1.

To see the A1 functions for this version, see `A1 Standard 2.0.0 API`_.

.. _A1 Standard 2.0.0 API: https://gerrit.o-ran-sc.org/r/gitweb?p=sim/a1-interface.git;a=blob;f=near-rt-ric-simulator/api/STD_2.0.0/ORAN_A1-p_V2.0.0_api.yaml


/policytype
~~~~~~~~~~~

PUT
+++

Create or update a policy type.

**URL path:**

/policytype?id={policy-type-id}

**Parameters:**

policy-type-id: (*Required*)

The ID of the policy type.

**Body:** (*Required*)

A JSON object containing the schema for the type.

**Responses:**

200:

The policy type <policy-type-id> is ok

201:

The policy type <policy-type-id> is ok

**Examples:**

**Call**: ::

  curl -X PUT "http://localhost:8085/policytype?id=STD_PolicyModelUnconstrained_0.2.0"
    -H  "Content-Type: application/json"
    -d '{
          "policySchema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "STD_1_0.2.0",
            "description": "STD 1 policy type",
            "type": "object",
            "properties": {
              "scope": {
                "type": "object",
                "properties": {
                  "ueId": {
                    "type": "string"
                  },
                  "qosId": {
                    "type": "string"
                  }
                },
                "additionalProperties": false,
                "required": [
                  "ueId",
                  "qosId"
                ]
              },
              "statement": {
                "type": "object",
                "properties": {
                  "priorityLevel": {
                    "type": "number"
                  }
                },
                "additionalProperties": false,
                "required": [
                  "priorityLevel"
                ]
              }
            }
          },
          "statusSchema": {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "STD_1_0.2.0",
            "description": "STD 1 policy type status",
            "type": "object",
            "properties": {
              "enforceStatus": {
                "type": "string"
              },
              "enforceReason": {
                "type": "string"
              },
              "additionalProperties": false,
              "required": [
                "enforceStatus"
              ]
            }
          }
        }'

**Result**:

200: ::

  Policy type STD_PolicyModelUnconstrained_0.2.0 is OK

201: ::

  Policy type STD_PolicyModelUnconstrained_0.2.0 is OK

DELETE
++++++

Delete a policy type.

**URL path:**

/policytype?id={policy-type-id}

**Parameters:**

None.

**Responses:**

204


**Examples:**

**Call**: ::

  curl -X DELETE "http://localhost:8085/policytype?id=STD_PolicyModelUnconstrained_0.2.0"

**Result**:

204



/policytypes
~~~~~~~~~~~~

GET
+++

Get a list of policy types.

**URL path:**

/policytypes

**Parameters:**

None.

**Responses:**

200:

A list of policy types.

**Examples:**

**Call**: ::

  curl -X GET "http://localhost:8085/policytypes"

**Result**:

200: ::

  ["STD_PolicyModelUnconstrained_0.2.0"]


/{policyId}/{enforceStatus}
~~~~~~~~~~~~~~~~~~~~~~~~~~~

PUT
+++

Set a status to a policy instance with an enforceStatus parameter only.

**URL path:**

/status?policyid={policyId}&status={status}&reason={reason}

**Parameters:**

None.

**Responses:**

200:

Status updated for policy: <policyId>

**Examples:**

**Call**: ::

  curl -X PUT "http://localhost:8085/status?policyid=Policy1&status=ENFORCED"

**Result**:

200: ::

  Status updated for policy: Policy1

/{policyId}/{enforceStatus}/{enforceReason}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

/sendstatus
~~~~~~~~~~~

POST
++++

Send status for policy.

**URL path:**

/sendstatus?policyid=<policy-id>

**Parameters:**

policyid: (*Required*)

The ID of the policy to send status for.

**Responses:**

200:

Is a JSON with the response of the actual post request to the callback server, whatever that is.

**Examples:**

**Call**: ::

  curl -X POST "http://localhost:8085/sendstatus?policyid=Policy2"

**Result**:

200
