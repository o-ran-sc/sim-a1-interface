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

# Script to build and start the container

echo "Building image"
cd ../../

#Build the image
docker build -t a1test .

echo "Starting $1 mode"
#Run the container in interactive mode, unsecure port 8085, secure port 8185.
docker run -it -p 8085:8085 -p 8185:8185 -e A1_VERSION=1.1.x-alpha.2 -e ALLOW_HTTP=true -e REMOTE_HOSTS_LOGGING=1 --volume "$PWD/certificate:/usr/src/app/cert" a1test


