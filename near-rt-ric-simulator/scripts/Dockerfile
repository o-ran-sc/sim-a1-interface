FROM python:3

WORKDIR /usr/src/app

RUN pip install connexion[swagger-ui]

COPY example_files/policy_instance_1_STD_QoSNudging_0.2.0.json policy_instance_1_STD_QoSNudging_0.2.0.json
COPY example_files/policy_instance_1_bis_STD_QoSNudging_0.2.0.json policy_instance_1_bis_STD_QoSNudging_0.2.0.json
COPY example_files/policy_instance_2_STD_QoSNudging_0.2.0.json policy_instance_2_STD_QoSNudging_0.2.0.json
COPY example_files/policy_type_STD_QoSNudging_0.2.0.json policy_type_STD_QoSNudging_0.2.0.json

COPY a1.py a1.py
COPY main.py main.py
COPY var_declaration.py var_declaration.py

COPY commands.sh commands.sh
COPY run_me.sh run_me.sh

COPY a1-openapi.yaml a1-openapi.yaml

CMD ["/bin/bash", "./run_me.sh"]
