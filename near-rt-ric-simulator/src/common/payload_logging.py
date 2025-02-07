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

from var_declaration import app
from flask import Flask, request, Response
from datetime import datetime

#Constants
TEXT_PLAIN='text/plain'

#Vars
payload_log=True

#Function to activate/deactivate http header and payload logging
@app.route('/payload_logging/<state>', methods=['POST', 'PUT'])
def set_payload_logging(state):
  global payload_log
  if (state == "on"):
    payload_log=True
  elif (state == "off"):
    payload_log=False
  else:
    return Response("Unknown state: "+state+" - use 'on' or 'off'", 400, mimetype=TEXT_PLAIN)

  return Response("Payload and header logging set to: "+state, 200, mimetype=TEXT_PLAIN)

# Generic function to log http header and payload - called before the request
@app.app.before_request
def log_request_info():
    if (payload_log is True):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Format timestamp with milliseconds
        print(f"\n[{timestamp}]")
        print('-----Request-----')
        print('Req Headers: ', request.headers)
        print('Req Body: ', request.get_data())

# Generic function to log http header and payload - called after the response
@app.app.after_request
def log_response_info(response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Format timestamp with milliseconds
    print(f"\n[{timestamp}]")
    if (payload_log is True):
        print('-----Response-----')
        print('Resp Headers: ', response.headers)
        print('Resp Body: ', response.get_data())
    return response

# Helper function to check loggin state
def is_payload_logging():
  return payload_log