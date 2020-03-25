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

if [ $# -ne 1 ]; then
    echo "Expected folder name of simulator."
    echo "The container shall be started with env variable 'A1_VERSION' set to the folder name of the A1 version to use."
    echo "Exiting...."
    exit 1
fi
echo "Version folder for simulator: "$1

#Set path to open api
export APIPATH=$PWD/api/$1
echo "APIPATH set to: "$APIPATH

cd src

#Include common module(s)
export PYTHONPATH=$PWD/common
echo "PYTHONPATH set to: "$PYTHONPATH

cd $1

echo "Path to main.py: "$PWD
python -u main.py
