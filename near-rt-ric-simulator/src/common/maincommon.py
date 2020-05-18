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

# Return a Response of currently supported interfaces
def get_supported_interfaces_response():
    p=Path(os.getcwd())
    pp=p.parts
    arr = os.listdir("../")
    del arr[arr.index('common')] # Remove the common lib
    del arr[arr.index('start.sh')] # Remove the start script
    arr.sort()
    return Response("Current interface: " + str(pp[len(pp)-1]) + "  All supported A1 interface yamls in this container: "+str(arr), 200, mimetype='text/plain')

# Remote host lookup and store host name in a set
def extract_host_name(hosts_set, request):
    if (remote_hosts_logging is not None):
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            host_ip=str(request.environ['REMOTE_ADDR'])
        else:
            host_ip=str(request.environ['HTTP_X_FORWARDED_FOR'])
        prefix='::ffff:'
        if (host_ip.startswith('::ffff:')):
            host_ip=host_ip[len(prefix):]
        try:
            name, alias, addresslist = socket.gethostbyaddr(host_ip)
            hosts_set.add(name)
        except Exception as e:
            hosts_set.add(host_ip)
    else:
        hosts_set.add("logging_of_remote_host_names_not_enabled")
