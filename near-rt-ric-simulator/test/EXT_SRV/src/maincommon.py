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

import os
import sys
from pathlib import Path
from flask import Response
import socket
import ssl

#Must exist
apipath=os.environ['APIPATH']
#May exist
remote_hosts_logging=os.getenv('REMOTE_HOSTS_LOGGING')

# Make sure the api path for the interface yaml file is set, otherwise exit
def check_apipath():
    if (apipath is None):
        print("Env APIPATH not set. Exiting....")
        sys.exit(1)
