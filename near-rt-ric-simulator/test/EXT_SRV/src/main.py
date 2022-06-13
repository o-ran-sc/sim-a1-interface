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

import json
import sys
import requests


from flask import request, Response, Flask, json
from var_declaration import a1_policy_instances, forced_settings, app
from maincommon import check_apipath

#Constants
TEXT_PLAIN='text/plain'

check_apipath()

# app is created in var_declarations

import payload_logging   # app var need to be initialized

#Check alive function
@app.route('/', methods=['GET'])
def test():
  return Response("OK", 200, mimetype=TEXT_PLAIN)

#Delete all created instances and status
@app.route('/serveradmin/deleteinstances', methods=['POST'])
def delete_instances():
    a1_policy_instances.clear()
    return Response("All a1 policy instances deleted", 200, mimetype=TEXT_PLAIN)

#Set|Reset force response to be returned from external server
#/a1policy/forceresponse?code=<responsecode>
@app.route('/serveradmin/forceresponse', methods=['POST'])
def forceresponse():

  query_param=request.args.get('code')
  forced_settings['code']=query_param

  if (query_param is None):
    return Response("Force response code has been resetted for all external server responses", 200, mimetype=TEXT_PLAIN)
  else:
    return Response("Force response code: " + str(forced_settings['code']) + " set for all external server response until it is resetted", 200, mimetype=TEXT_PLAIN)

#Set|Reset force delay response, in seconds, for all external server responses
#/a1policy/forcedelay?delay=<seconds>
@app.route('/serveradmin/forcedelay', methods=['POST'])
def forcedelay():

  query_param=request.args.get('delay')
  forced_settings['delay']=query_param

  if (query_param is None):
    return Response("Force delay has been resetted for all external server responses ", 200, mimetype=TEXT_PLAIN)
  else:
    return Response("Force delay: " + str(forced_settings['delay']) + " sec set for all external server responses until it is resetted ", 200, mimetype=TEXT_PLAIN)

port_number = 3333
if len(sys.argv) >= 2:
  if isinstance(sys.argv[1], int):
    port_number = sys.argv[1]

#Import base RestFUL API functions from Open API
app.add_api('EXT_SRV_api.yaml')

if __name__ == '__main__':
  app.run(port=port_number, host="127.0.0.1", threaded=False)
