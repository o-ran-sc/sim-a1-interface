.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 Nordix

.. _simulator-api:

=============
Simulator API
=============

This document describes the API used to manage policy types and manipulate the simulator.

The simulator supports different versions of the A1 interface. Some functions are common for all version, and some are
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
    Simulator is living.

**Examples:**
  **Call**: ::

    curl -X GET "http://localhost:8085/"

  Result:
    200: ::

      Simulator is living (OSC_2.1.0 responds OK)

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

  Result:
    200: ::

      1.1.x-alpha.2 OSC_2.1.0 STD_1.1.3

Counters
--------

The simulator keeps counts of different things that can be accessed.

/counter
~~~~~~~~

GET
+++

Get a counter. Counter-name can be one of the following: 'num_instances', 'num_types' or 'interface'.

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

  Result:
    200: ::

      10

Version Specific Functions
==========================

The methods available to control the simulator depends on the version of the A1 API the simulator is simulating.

OSC_2.1.0
---------

This section describes the available administrative functions for the OSC_2.1.0 version of A1.

To see the A1 functions for this version, see `OSC_2.1.0 API`_.

.. _OSC_2.1.0 API: https://gerrit.o-ran-sc.org/r/gitweb?p=sim/a1-interface.git;a=blob;f=near-rt-ric-simulator/api/OSC_2.1.0/openapi.yaml

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

  Result:
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

  Result:
    200: ::

      All policy instances and types deleted.

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

    curl -X PUT "http://localhost:8085/policytype?id=Policy%201&ric=ric1&service=Service%201&type=STD_PolicyModelUnconstrained_0.2.0"
      -H  "Content-Type: application/json"
      -d '{
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "STD_PolicyModelUnconstrained_0.2.0",
            "description": "Standard model of a policy with unconstrained scope id combinations",
            "type": "object",
            "properties": {
              "scope": {
                "type": "object",
                "properties": {
                  "ueId": {"type": "string"},
                  "groupId": {"type": "string"},
                  "sliceId": {"type": "string"},
                  "qosId": {"type": "string"},
                  "cellId": {"type": "string"}
                },
                "minProperties": 1,
                "additionalProperties": false
              },
              "qosObjectives": {
                "type": "object",
                "properties": {
                  "gfbr": {"type": "number"},
                  "mfbr": {"type": "number"},
                  "priorityLevel": {"type": "number"},
                  "pdb": {"type": "number"}
                },
                "additionalProperties": false
              },
              "qoeObjectives": {
                "type": "object",
                "properties": {
                  "qoeScore": {"type": "number"},
                  "initialBuffering": {"type": "number"},
                  "reBuffFreq": {"type": "number"},
                  "stallRatio": {"type": "number"}
                },
                "additionalProperties": false
              },
              "resources": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "cellIdList": {
                      "type": "array",
                      "minItems": 1,
                      "uniqueItems": true,
                      "items": {
                        "type": "string"
                      }
                    },
                    "preference": {
                      "type": "string",
                      "enum": [
                        "SHALL",
                        "PREFER",
                        "AVOID",
                        "FORBID"
                      ]
                    },
                    "primary": {"type": "boolean"}
                  },
                  "additionalProperties": false,
                  "required": ["cellIdList", "preference"]
                }
              }
            },
            "minProperties": 2,
            "additionalProperties": false,
            "required": ["scope"]
          }'

  Result:
    201: ::

      Policy type STD_PolicyModelUnconstrained_0.2.0 is OK

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

   curl -X DELETE "http://localhost:8085/policytype?id=Policy%201&ric=ric1&service=Service%201&type=STD_PolicyModelUnconstrained_0.2.0"

  Result:
    204: ::

      Policy type STD_PolicyModelUnconstrained_0.2.0 is OK

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

  Result:
    200: ::

      STD_PolicyModelUnconstrained_0.2.0

/forceresponse
~~~~~~~~~~~~~~

POST
++++

Force a specific response code for an A1 operation.

**URL path:**
  /forceresponse?responsecode=<http-response-code>

**Parameters:**
  responsecode: (*Required*)
    The HTTP response code to return.

**Responses:**
  200:
    Force response code:  <expected code> set for one single A1 response

**Examples:**
  **Call**: ::

    curl -X POST "http://localhost:8085/forceresponse?responsecode=400"

  Result:
    200: ::

      Force response code:  400 set for one single A1 response

/forcedelay
~~~~~~~~~~~

POST
++++

Force delayed response of all A1 operations.

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

  Result:
    200: ::

      Force delay: 2 sec set for all A1 responses

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

    curl -X PUT "http://localhost:8085/policyid=Policy1&status?status=Accepted

  Result:
    200: ::

      Status set to Accepted for policy Policy1.

A1 Standard 1.1.3
-----------------

This section describes the available administrative functions for the A1 Standard 1.1.3 version of A1.

To see the A1 functions for this version, see `A1 Standard 1.1.3 API`_.

.. _A1 Standard 1.1.3 API: https://gerrit.o-ran-sc.org/r/gitweb?p=sim/a1-interface.git;a=blob;f=near-rt-ric-simulator/api/STD_1.1.3/STD_A1.yaml

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

  Result:
    200: ::

      All policy instances deleted.

/deleteall
~~~~~~~~~~

POST
++++

Full reset.

**URL path:**
  /deleteinstances

**Parameters:**
  None.

**Responses:**
  200:
    All policy instances deleted.

**Examples:**
  **Call**: ::

    curl -X POST "http://localhost:8085/deleteall"

  Result:
    200: ::

      All policy instances deleted.

/forceresponse
~~~~~~~~~~~~~~

POST
++++

Force a specific response code for an A1 operation.

**URL path:**
  /forceresponse?responsecode=<http-response-code>

**Parameters:**
  responsecode: (*Required*)
    The HTTP response code to return.

**Responses:**
  200:
    Force response code: <expected code> set for one single A1 response

**Examples:**
  **Call**: ::

    curl -X POST "http://localhost:8085/forceresponse?responsecode=400"

  Result:
    200: ::

      Force response code: 400 set for one single A1 response

/forcedelay
~~~~~~~~~~~

POST
++++

Force delayed response of all A1 operations.

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

  Result:
    200: ::

      Force delay: 2 sec set for all A1 responses

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

    curl -X PUT "http://localhost:8085/status?policyid=Policy1&status=Accepted

  Result:
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

  Result:
    200

1.1.x-alpha.2
-------------

This section describes the available administrative functions for the 1.1.x-alpha.2 version of A1.

To see the A1 functions for this version, see `1.1.x-alpha.2 API`_.

.. _1.1.x-alpha.2 API: https://gerrit.o-ran-sc.org/r/gitweb?p=sim/a1-interface.git;a=blob;f=near-rt-ric-simulator/api/1.1.x-alpha.2/a1-openapi.yaml

/deleteinstances
~~~~~~~~~~~~~~~~

DELETE
++++++

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

    curl -X DELETE "http://localhost:8085/deleteinstances"

  Result:
    200: ::

      All policy instances deleted.

/deletetypes
~~~~~~~~~~~~

DELETE
++++++

Delete all policy types.

**URL path:**
  /deletetypes

**Parameters:**
  None.

**Responses:**
  200:
    All policy types deleted.

**Examples:**
  **Call**: ::

    curl -X DELETE "http://localhost:8085/deletetypes"

  Result:
    200: ::

      All policy types deleted.

/policytypes
~~~~~~~~~~~~

PUT
+++

Create or update a policy type.

**URL path:**
  /policytypes/{policy-type-id}

**Parameters:**
  None.

**Body:** (*Required*)
    A JSON object containing the schema for the type.

**Responses:**
  200:
    The policy type was either created or updated for policy type id: <policy-type-id>

**Examples:**
  **Call**: ::

    curl -X PUT "http://localhost:8085/policytype/Policy%201&ric=ric1&service=Service%201&type=STD_PolicyModelUnconstrained_0.2.0"
      -H  "Content-Type: application/json"
      -d '{
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "STD_PolicyModelUnconstrained_0.2.0",
            "description": "Standard model of a policy with unconstrained scope id combinations",
            "type": "object",
            "properties": {
              "scope": {
                "type": "object",
                "properties": {
                  "ueId": {"type": "string"},
                  "groupId": {"type": "string"},
                  "sliceId": {"type": "string"},
                  "qosId": {"type": "string"},
                  "cellId": {"type": "string"}
                },
                "minProperties": 1,
                "additionalProperties": false
              },
              "qosObjectives": {
                "type": "object",
                "properties": {
                  "gfbr": {"type": "number"},
                  "mfbr": {"type": "number"},
                  "priorityLevel": {"type": "number"},
                  "pdb": {"type": "number"}
                },
                "additionalProperties": false
              },
              "qoeObjectives": {
                "type": "object",
                "properties": {
                  "qoeScore": {"type": "number"},
                  "initialBuffering": {"type": "number"},
                  "reBuffFreq": {"type": "number"},
                  "stallRatio": {"type": "number"}
                },
                "additionalProperties": false
              },
              "resources": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "cellIdList": {
                      "type": "array",
                      "minItems": 1,
                      "uniqueItems": true,
                      "items": {
                        "type": "string"
                      }
                    },
                    "preference": {
                      "type": "string",
                      "enum": [
                        "SHALL",
                        "PREFER",
                        "AVOID",
                        "FORBID"
                      ]
                    },
                    "primary": {"type": "boolean"}
                  },
                  "additionalProperties": false,
                  "required": ["cellIdList", "preference"]
                }
              }
            },
            "minProperties": 2,
            "additionalProperties": false,
            "required": ["scope"]
          }'

  Result:
    200: ::

      The policy type was either created or updated for policy type id: STD_PolicyModelUnconstrained_0.2.0

DELETE
++++++

Delete a policy type.

**URL path:**
  /policytypes/{policy-type-id}

**Parameters:**
  None.

**Responses:**
  200:
    policy type successfully deleted for policy type id: <policy-type-id>

**Examples:**
  **Call**: ::

   curl -X DELETE "http://localhost:8085/policytype?id=Policy%201&ric=ric1&service=Service%201&type=STD_PolicyModelUnconstrained_0.2.0"

  Result:
    200: ::

      policy type successfully deleted for policy type id: STD_PolicyModelUnconstrained_0.2.0

/{policyId}/{enforceStatus}
~~~~~~~~~~~~~~~~~~~~~~~~~~~

PUT
+++

Set a status to a policy instance with an enforceStatus parameter only.

**URL path:**
  /{policyId}/{enforceStatus}

**Parameters:**
  None.

**Responses:**
  200:
    Status updated for policy: <policyId>

**Examples:**
  **Call**: ::

    curl -X PUT "http://localhost:8085/Policy1/ENFORCED

  Result:
    200: ::

      Status updated for policy: Policy1

/{policyId}/{enforceStatus}/{enforceReason}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PUT
++++

Send a status to a policy instance with both enforceStatus and enforceReason.

**URL path:**
  /{policyId}/{enforceStatus}/{enforceReason}

**Parameters:**
  None.

**Responses:**
  200:
    Status updated for policy: <policyId>

**Examples:**
  **Call**: ::

    curl -X PUT "http://localhost:8085/Policy1/NOT_ENFORCED/100"

  Result:
    200: ::

      Status updated for policy: Policy1
