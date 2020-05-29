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

FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN pip install connexion[swagger-ui]

#install nginx
RUN apt-get update
RUN apt-get install -y nginx=1.14.*
RUN apt-get install -y nginx-extras

#install curl
RUN apt-get install -y curl

COPY src src
COPY api api
COPY nginx.conf nginx.conf
COPY certificate /usr/src/app/cert

RUN chmod +x src/start.sh
CMD src/start.sh ${A1_VERSION}
