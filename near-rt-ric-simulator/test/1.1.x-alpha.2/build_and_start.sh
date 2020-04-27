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
# Args: nonsecure|secure

if [ $# -ne 1 ]; then
    echo "Usage: ./build_and_start.sh nonsecure|secure"
    exit 1
fi
if [ "$1" != "nonsecure" ] && [ "$1" != "secure" ]; then
    echo "Usage: ./build_and_start.sh nonsecure|secure"
    exit 1
fi

echo "Building image"
cd ../../

#Build the image
docker build -t a1test .

echo "Starting $1 mode"
if [ $1 == "nonsecure" ]; then
    #Run the container in interactive mode, unsecure port
    docker run -it -p 8085:8085 -e A1_VERSION=1.1.x-alpha.2 -e REMOTE_HOSTS_LOGGING=1 a1test
else
    #Run the container in interactive mode, secure port.
    docker run -it -p 8185:8185 -e A1_VERSION=1.1.x-alpha.2 -e REMOTE_HOSTS_LOGGING=1 --read-only --volume "$PWD/certificate:/usr/src/app/cert" a1test
fi


