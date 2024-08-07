#  ============LICENSE_START===============================================
#  Copyright (C) 2022 Nordix Foundation. All rights reserved.
#  Copyright (C) 2023-2024 OpenInfra Foundation Europe. All rights reserved.
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

FROM python:3.8-slim-buster

RUN pip3 install "connexion[swagger-ui,flask,uvicorn]"
RUN pip3 install kafka-python

#install nginx and curl
RUN apt-get update && apt-get install -y nginx=1.14.* nginx-extras curl

WORKDIR /usr/src/app

COPY api api
COPY nginx.conf nginx.conf
COPY certificate /usr/src/app/cert
COPY src src
COPY resources resources

ARG user=nonrtric
ARG group=nonrtric

RUN groupadd $user && \
    useradd -r -g $group $user
RUN chown -R $user:$group /usr/src/app
RUN chown -R $user:$group /var/log/nginx
RUN chown -R $user:$group /var/lib/nginx
RUN chown -R $user:$group /etc/nginx/conf.d
RUN touch /var/run/nginx.pid
RUN chown -R $user:$group /var/run/nginx.pid

USER ${user}

RUN chmod +x src/start.sh
CMD src/start.sh
