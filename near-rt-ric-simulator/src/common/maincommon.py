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

import os
import sys
from pathlib import Path
from flask import Response

apipath=os.environ['APIPATH']

# Make sure the api path for the interface yaml file is set, otherwise exit
def check_apipath():
    if (apipath is None):
        print("Env APIPATH not set. Exiting....")
        sys.exit(1)

# Return a Response of currently supported interfaces
def get_supported_interfaces_response():
    p=Path(os.getcwd())
    pp=p.parts
    arr = os.listdir("../")
    del arr[arr.index('common')] # Remove the common lib
    del arr[arr.index('start.sh')] # Remove the start script
    return Response("Current interface: " + str(pp[len(pp)-1]) + "  All supported A1 interface yamls in this container: "+str(arr), 200, mimetype='text/plain')

