#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2022 Nordix Foundation. All rights reserved.
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
    echo "Usage: ./build_and_start.sh duplicate-check|ignore-duplicate kafka-srv|kafka-srv-secure publish-resp|ignore-publish"
    exit 1
}

if [ $# -ne 3 ]; then
    print_usage
fi

if [ $1 == "duplicate-check" ]; then
    DUP_CHECK=1
elif  [ $1 == "ignore-duplicate" ]; then
    DUP_CHECK=0
else
    print_usage
fi

if [ $2 == "kafka-srv" ]; then
    URL="http://localhost:7075"
elif  [ $2 == "kafka-srv-secure" ]; then
    URL="https://localhost:7175"
else
    print_usage
fi

if [ $3 == "publish-resp" ]; then
    PUBLISH_RESP="-e PUBLISH_RESP=1"
elif  [ $3 == "ignore-publish" ]; then
    PUBLISH_RESP=""
else
    print_usage
fi

URL_FLAG=""
if [ ! -z "$URL" ]; then
    URL_FLAG="-e KAFKA_DISPATCHER_URL=$URL"
fi

# Stop and remove container images if they run

echo "Stopping A1 simulator image..."
docker stop a1StdSimulator > /dev/null 2>&1
docker rm -f a1StdSimulator > /dev/null 2>&1

echo "Stopping kafka dispatcher server image..."
docker stop kafkamessagedispatcher > /dev/null 2>&1
docker rm -f kafkamessagedispatcher > /dev/null 2>&1

# Initialize path variables for certificate and build operations

dirstd2=$PWD

cd ../../
dirnrtsim=$PWD

cd test/KAFKA_DISPATCHER/
dirkafkasrv=$PWD

# Build containers

cd $dirnrtsim
echo "Building A1 simulator image..."
docker build -t a1test .

if [ ! -z "$URL" ]; then
    cd $dirkafkasrv
    echo "Building kafka server image..."
    docker build -t kafka_dispatcher .
fi

# Run containers

# Runs kafka server in detached mode
# In order to tail logs use:: docker logs -f kafkamessagedispatcher
if [ ! -z "$URL" ]; then
    docker run -d --network host --rm -it -p 7075:7075 -p 7175:7175 -e ALLOW_HTTP=true -e MSG_BROKER_URL=localhost:9092 -e TIME_OUT=30 $PUBLISH_RESP --volume "$dirkafkasrv/certificate:/usr/src/app/cert" --name kafkamessagedispatcher kafka_dispatcher
fi

# Runs A1 simulator in detached mode
# In order to tail logs use:: docker logs -f a1StdSimulator
docker run -d --network host --rm -it -p 8085:8085 -p 8185:8185 -e A1_VERSION=STD_2.0.0 -e ALLOW_HTTP=true -e REMOTE_HOSTS_LOGGING=1 -e DUPLICATE_CHECK=$DUP_CHECK $URL_FLAG --volume "$dirnrtsim/certificate:/usr/src/app/cert" --name a1StdSimulator a1test
