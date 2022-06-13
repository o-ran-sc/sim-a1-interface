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

echo "Building external server image..."
cd ../EXT_SRV/

#Build the image
docker build -t external_server .

docker stop externalserversimulator > /dev/null 2>&1
docker rm -f externalserversimulator > /dev/null 2>&1

echo "Starting external server for A1 simulator callouts..."
echo "PWD path: "$PWD

#Run the container in interactive mode, unsecure port 8085, secure port 8185
docker run --rm -it -p 9095:9095 -p 9195:9195 -e ALLOW_HTTP=true --volume "$PWD/certificate:/usr/src/app/cert" --name externalserversimulator external_server
