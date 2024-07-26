#  ============LICENSE_START===============================================
#  Copyright (C) 2022 Nordix Foundation. All rights reserved.
#  Copyright (C) 2023-2024 OpenInfra Foundation Europe. All rights reserved.
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

import json
import sys
import requests


from flask import request, Response, Flask, json
from var_declaration import forced_settings, app
from maincommon import check_timeout, check_apipath

#Constants
TEXT_PLAIN='text/plain'

check_apipath()
check_timeout()

# app is created in var_declarations

import payload_logging   # app var need to be initialized

#Check alive function
@app.route('/', methods=['GET'])
def test():
  return Response("OK", 200, mimetype=TEXT_PLAIN)

#Set|Reset force response to be returned from dispatcher
#/dispatcheradmin/forceresponse?code=<responsecode>
@app.route('/dispatcheradmin/forceresponse', methods=['POST'])
def forceresponse():

  query_param=request.args.get('code')
  forced_settings['code']=query_param

  if (query_param is None):
    return Response("Force response code has been resetted for dispatcher responses", 200, mimetype=TEXT_PLAIN)
  else:
    return Response("Force response code: " + str(forced_settings['code']) + " set for all dispatcher response until it is resetted", 200, mimetype=TEXT_PLAIN)

#Set|Reset force delay response, in seconds, for all external server responses
#/a1policy/forcedelay?delay=<seconds>
@app.route('/dispatcheradmin/forcedelay', methods=['POST'])
def forcedelay():

  query_param=request.args.get('delay')
  forced_settings['delay']=query_param

  if (query_param is None):
    return Response("Force delay has been resetted for all dispatcher responses ", 200, mimetype=TEXT_PLAIN)
  else:
    return Response("Force delay: " + str(forced_settings['delay']) + " sec set for all dispatcher responses until it is resetted ", 200, mimetype=TEXT_PLAIN)

port_number = 7777
if len(sys.argv) >= 2:
  if isinstance(sys.argv[1], int):
    port_number = sys.argv[1]

#Import base RestFUL API functions from Open API
app.add_api('KAFKA_DISPATCHER_api.yaml')

if __name__ == '__main__':
  app.run(port=port_number, host="127.0.0.1")
