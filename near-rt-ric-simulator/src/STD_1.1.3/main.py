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

import connexion
import json
import sys
import os
import requests


from pathlib import Path
from flask import Flask, escape, request, Response
from jsonschema import validate
from var_declaration import policy_instances, policy_status, callbacks, forced_settings, policy_fingerprint, hosts_set
from maincommon import *


check_apipath()

app = connexion.App(__name__, specification_dir=apipath)

#Check alive function
@app.route('/', methods=['GET'])
def test():

  return Response("OK", 200, mimetype='text/plain')

#Return the current and all supported yamls for the this container
@app.route('/container_interfaces', methods=['GET'])
def container_interfaces():

    return get_supported_interfaces_response()

#Delete all created instances and status
@app.route('/deleteinstances', methods=['POST'])
def delete_instances():

  policy_instances.clear()
  policy_status.clear()
  callbacks.clear()
  forced_settings['code']=None
  forced_settings['delay']=None
  policy_fingerprint.clear()
  return Response("All policy instances deleted", 200, mimetype='text/plain')

#Delete all - all reset
#(same as delete_instances but kept to in order to use the same interface as other version of the simulator)
@app.route('/deleteall', methods=['POST'])
def delete_all():
  return delete_instances()

#Set force response for one A1 response
#/forceresponse?code=<responsecode>
@app.route('/forceresponse', methods=['POST'])
def forceresponse():

  try:
    forced_settings['code']=request.args.get('code')
  except:
    forced_settings['code']=None
  return Response("Force response code: " + str(forced_settings['code']) + " set for one single A1 response", 200, mimetype='text/plain')

#Set force delay response, in seconds, for all A1 responses
#/froceesponse?delay=<seconds>
@app.route('/forcedelay', methods=['POST'])
def forcedelay():

  try:
    forced_settings['delay']=request.args.get('delay')
  except:
    forced_settings['delay']=None
  return Response("Force delay: " + str(forced_settings['delay']) + " sec set for all A1 responses", 200, mimetype='text/plain')


#Set status and reason
#/status?policyid=<policyid>&status=<status>[&reason=<reason>]
@app.route('/status', methods=['PUT'])
def setstatus():

  policyId=request.args.get('policyid')
  if (policyId is None):
    return Response('Parameter <policyid> missing in request', status=400, mimetype='text/plain')
  if policyId not in policy_instances.keys():
    return Response('Policyid: '+policyId+' not found.', status=404, mimetype='text/plain')
  status=request.args.get('status')
  if (status is None):
    return Response('Parameter <status> missing in request', status=400, mimetype='text/plain')
  reason=request.args.get('reason')
  ps = {}
  ps["enforceStatus"] = status
  msg="Status set to "+status
  if (reason is not None):
    ps["enforceReason"] = reason
    msg=msg+" and "+reason
  policy_status[policyId] = ps
  msg=msg+" for policy: " + policyId
  return Response(msg, 200, mimetype='text/plain')

#Send status
#/status?policyid=<policyid>
@app.route('/sendstatus', methods=['POST'])
def sendstatus():
  policyid=request.args.get('policyid')
  if (policyid is None):
    return Response('Parameter <policyid> missing in request', status=400, mimetype='text/plain')

  if (policyid not in policy_status.keys()):
    return Response('Policyid: '+policyid+' not found.', status=404, mimetype='text/plain')

  ps=policy_status[policyid]
  cb=callbacks[policyid]
  try:
    resp=requests.post(cb,json=json.dumps(ps), verify=False)
  except:
    return Response('Post status failed, could not send to: '+str(cb), status=500, mimetype='text/plain')
  if (resp.status_code<199 & resp.status_code > 299):
    return Response('Post status failed with code: '+resp.status_code, status=500, mimetype='text/plain')

  data = resp.json()
  return Response(data, 200, mimetype='application/json')

#Receive status (only for testing callbacks)
#/statustest
@app.route('/statustest', methods=['POST', 'PUT'])
def statustest():
  try:
    data = request.data
    data = json.loads(data)
  except:
    return Response("The status data is corrupt or missing.", 400, mimetype='text/plain')

  return Response(json.dumps(data), 200, mimetype='application/json')

#Metrics function
#Get a named counter
@app.route('/counter/<string:countername>', methods=['GET'])
def getCounter(countername):

  if (countername == "num_instances"):
    return Response(str(len(policy_instances)), 200, mimetype='text/plain')
  elif (countername == "num_types"):
    return Response("0",200, mimetype='text/plain')
  elif (countername == "interface"):
    p=Path(os.getcwd())
    pp=p.parts
    return Response(str(pp[len(pp)-1]),200, mimetype='text/plain')
  elif (countername == "remote_hosts"):
    hosts=",".join(hosts_set)
    return str(hosts),200
  else:
    return Response("Counter name: "+countername+" not found.",404, mimetype='text/plain')

port_number = 2222
if len(sys.argv) >= 2:
  if isinstance(sys.argv[1], int):
    port_number = sys.argv[1]

app.add_api('STD_A1.yaml')

app.run(port=port_number, host="127.0.0.1")