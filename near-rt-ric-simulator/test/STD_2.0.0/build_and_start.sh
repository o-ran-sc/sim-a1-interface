#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2021-2022 Nordix Foundation. All rights reserved.
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
# Make sure to run the simulator with the same arg as this script

print_usage() {
    echo "Usage: ./build_and_start.sh duplicate-check|ignore-duplicate ext-srv|ext-srv-secure|ignore-ext-srv"
    exit 1
}

if [ $# -ne 2 ]; then
    print_usage
fi

if [ $1 == "duplicate-check" ]; then
    DUP_CHECK=1
elif  [ $1 == "ignore-duplicate" ]; then
    DUP_CHECK=0
else
    print_usage
fi

if [ $2 == "ext-srv" ]; then
    URL="http://localhost:9095/a1policy/"
elif  [ $2 == "ext-srv-secure" ]; then
    URL="https://localhost:9195/a1policy/"
elif  [ $2 == "ignore-ext-srv" ]; then
    URL=""
else
    print_usage
fi

URL_FLAG=""
if [ ! -z "$URL" ]; then
    URL_FLAG="-e EXT_SRV_URL=$URL"
fi

# Stop and remove container images if they run

echo "Stopping A1 simulator image..."
docker stop a1StdSimulator > /dev/null 2>&1
docker rm -f a1StdSimulator > /dev/null 2>&1

echo "Stopping external server image..."
docker stop externalserversimulator > /dev/null 2>&1
docker rm -f externalserversimulator > /dev/null 2>&1

# Initialize path variables for certificate and build operations

dirstd2=$PWD

cd ../../
dirnrtsim=$PWD

cd test/EXT_SRV/
dirextsrv=$PWD

# Build containers

cd $dirnrtsim
echo "Building A1 simulator image..."
docker build -t a1test .

if [ ! -z "$URL" ]; then
    cd $dirextsrv
    echo "Building external server image..."
    docker build -t external_server .
fi

# Run containers

# Runs external_server in detached mode
# In order to tail logs use:: docker logs -f externalserversimulator
if [ ! -z "$URL" ]; then
    docker run -d --network host --rm -it -p 9095:9095 -p 9195:9195 -e ALLOW_HTTP=true --volume "$dirextsrv/certificate:/usr/src/app/cert" --name externalserversimulator external_server
fi

# Runs A1 simulator
docker run --network host --rm -it -p 8085:8085 -p 8185:8185 -e A1_VERSION=STD_2.0.0 -e ALLOW_HTTP=true -e REMOTE_HOSTS_LOGGING=1 -e DUPLICATE_CHECK=$DUP_CHECK $URL_FLAG --volume "$dirnrtsim/certificate:/usr/src/app/cert" --name a1StdSimulator a1test
