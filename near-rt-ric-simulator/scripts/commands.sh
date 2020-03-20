#!/bin/bash
#  ============LICENSE_START===============================================
#  Copyright (C) 2020 Nordix Foundation. All rights reserved.
#  ========================================================================
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  ============LICENSE_END=================================================
#

# Different commands for the simulator.
# By running this, nothing should return an error.

# Make a test
curl -v "http://localhost:8085/"

# PUT a policy type STD_QoSNudging_0.2.0
curl -X PUT -v "http://localhost:8085/policytypes/STD_QoSNudging_0.2.0" -H "accept: application/json" -H "Content-Type: application/json" --data-binary @example_files/policy_type_STD_QoSNudging_0.2.0.json

# GET policy types
curl -v "http://localhost:8085/A1-P/v1/policytypes"

# GET policy type STD_QoSNudging_0.2.0
curl -v "http://localhost:8085/A1-P/v1/policytypes/STD_QoSNudging_0.2.0"

# PUT a policy instance pi1
curl -X PUT -v "http://localhost:8085/A1-P/v1/policies/pi1?policyTypeId=STD_QoSNudging_0.2.0" -H "accept: application/json" -H "Content-Type: application/json" --data-binary @example_files/policy_instance_1_STD_QoSNudging_0.2.0.json

# PUT a policy instance pi2
curl -X PUT -v "http://localhost:8085/A1-P/v1/policies/pi2?policyTypeId=STD_QoSNudging_0.2.0" -H "accept: application/json" -H "Content-Type: application/json" --data-binary @example_files/policy_instance_2_STD_QoSNudging_0.2.0.json

# SET status for pi1 and pi2
curl -X PUT "http://localhost:8085/pi1/NOT_ENFORCED/300"
curl -X PUT "http://localhost:8085/pi2/ENFORCED"

# GET policies
curl -v "http://localhost:8085/A1-P/v1/policies"

# DELETE policy instance pi2
curl -X DELETE -v "http://localhost:8085/A1-P/v1/policies/pi2"

# PUT a different policy instance pi1 (i.e. update it)
curl -X PUT -v "http://localhost:8085/A1-P/v1/policies/pi1?policyTypeId=STD_QoSNudging_0.2.0" -H "accept: application/json" -H "Content-Type: application/json" --data-binary @example_files/policy_instance_1_bis_STD_QoSNudging_0.2.0.json

# GET policy instance pi1
curl -v "http://localhost:8085/A1-P/v1/policies/pi1"

# GET policy status for pi1
curl -v "http://localhost:8085/A1-P/v1/policystatus/pi1"
