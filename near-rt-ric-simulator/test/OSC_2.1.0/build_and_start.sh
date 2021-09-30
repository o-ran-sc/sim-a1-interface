#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2021 Nordix Foundation. All rights reserved.
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
    echo "Usage: ./build_and_start.sh duplicate-check|ignore-duplicate "
    exit 1
}

if [ $# -ne 1 ]; then
    print_usage
fi
if [ $1 == "duplicate-check" ]; then
    DUP_CHECK=1
elif  [ $1 == "ignore-duplicate" ]; then
    DUP_CHECK=0
else
    print_usage
fi

echo "Building image"
cd ../../

#Build the image
docker build -t a1test .

docker stop a1OscSimulator > /dev/null 2>&1
docker rm -f a1OscSimulator > /dev/null 2>&1

echo "Starting ric-sim"
#Run the container in interactive mode, unsecure port 8085, secure port 8185.
docker run --rm -it -p 8085:8085 -p 8185:8185 -e A1_VERSION=OSC_2.1.0 -e ALLOW_HTTP=true -e REMOTE_HOSTS_LOGGING=1 -e DUPLICATE_CHECK=$DUP_CHECK --volume "$PWD/certificate:/usr/src/app/cert" --name a1OscSimulator a1test

