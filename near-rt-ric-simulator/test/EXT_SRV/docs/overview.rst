.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 Nordix

.. |nbsp| unicode:: 0xA0
   :trim:

.. |nbh| unicode:: 0x2011
   :trim:


A1 Simulator EXT SRV
=====================

The A1 Simulator terminates the A1 interface and provides a way to test Non-RT RIC services without the need to deploy Near |nbh| RT |nbsp| RICs.

Apart from providing the A1 API, the simulator also provides an administrative API to manage policy types and manipulate
the simulator, see ":ref:`ext-srv-api`".

The A1 Simulator supports running multiple simulations using different versions of the A1 Application protocol, and supports realistic stateful simulation of A1 Enrichment Information and A1 Policy behaviours.

For information on how to run the simulator, see the *README.md* file in the repository.
