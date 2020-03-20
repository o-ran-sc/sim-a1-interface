#
# ============LICENSE_START=======================================================
#  Copyright (C) 2020 Nordix Foundation.
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============LICENSE_END=========================================================
#

FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN pip install connexion[swagger-ui]


COPY ./near-rt-ric-simulator/scripts/example_files/policy_instance_1_STD_QoSNudging_0.2.0.json policy_instance_1_STD_QoSNudging_0.2.0.json
COPY ./near-rt-ric-simulator/scripts/example_files/policy_instance_1_bis_STD_QoSNudging_0.2.0.json policy_instance_1_bis_STD_QoSNudging_0.2.0.json
COPY ./near-rt-ric-simulator/scripts/example_files/policy_instance_2_STD_QoSNudging_0.2.0.json policy_instance_2_STD_QoSNudging_0.2.0.json
COPY ./near-rt-ric-simulator/scripts/example_files/policy_type_STD_QoSNudging_0.2.0.json policy_type_STD_QoSNudging_0.2.0.json

COPY ./near-rt-ric-simulator/scripts/a1.py a1.py
COPY ./near-rt-ric-simulator/scripts/main.py main.py
COPY ./near-rt-ric-simulator/scripts/var_declaration.py var_declaration.py

COPY ./near-rt-ric-simulator/scripts/commands.sh commands.sh
COPY ./near-rt-ric-simulator/scripts/start_simulator.sh start_simulator.sh

COPY ./near-rt-ric-simulator/a1-openapi.yaml a1-openapi.yaml

CMD ["/bin/bash", "./run_me.sh"]
