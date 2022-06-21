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
    echo "Usage: ./build_and_start.sh "
    exit 1
}

if [ $# -ge 1 ]; then
    print_usage
fi

echo "Building Kafka message dispatcher image..."
cd ../KAFKA_DISPATCHER/

#Build the image
docker build -t kafka_dispatcher .

docker stop kafkamessagedispatcher > /dev/null 2>&1
docker rm -f kafkamessagedispatcher > /dev/null 2>&1

echo "Starting Kafka message dispatcher..."
echo "PWD path: "$PWD

#Run the container in interactive mode with host networking driver which allows docker to access localhost, unsecure port 7075, secure port 7175
docker run --network host --rm -it -p 7075:7075 -p 7175:7175 -e ALLOW_HTTP=true -e MSG_BROKER_URL=localhost:9092 -e KAFKA_TOPIC_RES=kafkatopicres --volume "$PWD/certificate:/usr/src/app/cert" --name kafkamessagedispatcher kafka_dispatcher
