.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2022 Nordix

.. |nbsp| unicode:: 0xA0
   :trim:

.. |nbh| unicode:: 0x2011
   :trim:

.. |yaml-icon| image:: ./images/yaml_logo.png
   :width: 40px

Kafka Dispatcher Module
=======================

The internal functionality of the dispatcher module is basically to publish kafka messages to the target-request-topic and consume from related response-topic. This mapping is provided in the below format. The logic is based on two-way synchronous communication between dispatcher-module and kafka-cluster. The time out is currently 30 seconds but it is a parametric value and can be changed as per need in the start script of A1 sim.

Policy-type to kafka-cluster-request/response topic mapping:

.. csv-table::
   :header: "API name", "|yaml-icon|"
   :widths: 10,5

   "The mapping file:", ":download:`link <../resources/policytype_to_topicmap.json>`"

For information on how to run kafka dispatcher module, see the *README.md* file in the repository.
