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
from var_declaration import policy_instances, policy_status, callbacks, forced_settings, policy_fingerprint, hosts_set, policy_types, policy_instance_to_type
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
  policy_instance_to_type.clear()
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

  policy_instances.clear()
  policy_instance_to_type.clear()
  policy_types.clear()
  policy_status.clear()
  callbacks.clear()
  forced_settings['code']=None
  forced_settings['delay']=None
  policy_fingerprint.clear()
  return Response("All policy instances and types deleted", 200, mimetype='text/plain')

#Load a policy type
@app.route('/policytype', methods=['PUT'])
def policytype():

  policyTypeId=request.args.get('id')
  if (policyTypeId is None):
    return Response('Parameter <id> missing in request', status=400, mimetype='text/plain')

  try:
    data = request.data
    data = json.loads(data)
  except:
    return Response("The policy type is corrupt or missing", 400, mimetype='text/plain')

  if ('policySchema' not in data) or len(data) > 2:
    return Response("The policy type does not include a policySchema or is corrupt", 400, mimetype='text/plain')

  retcode=201
  if (policyTypeId in policy_types.keys()):
    retcode=200
    if (policyTypeId in policy_instance_to_type.values()):
       return Response("The policy type already exists and instances exists", 400, mimetype='text/plain')

  policy_types[policyTypeId]=data

  return Response("Policy type " + policyTypeId + " is OK", retcode, mimetype='text/plain')

#Delete a policy type
@app.route('/policytype', methods=['DELETE'])
def del_policytype():

  policyTypeId=request.args.get('id')
  if (policyTypeId is None):
    return Response('Parameter <id> missing in request', status=400, mimetype='text/plain')

  if (policyTypeId in policy_types.keys()):
    if (policyTypeId in policy_instance_to_type.values()):
       return Response("The policy type exists but instances exists", 400, mimetype='text/plain')

    del policy_types[policyTypeId]
    return Response("Policy type " + policyTypeId + " deleted OK", 204, mimetype='text/plain')

  return Response("Policy type " + policyTypeId + " not found", 404, mimetype='text/plain')

# Get all policy type ids
@app.route('/policytypes', methods=['GET'])
def get_policytype_ids():

  return (json.dumps(list(policy_types.keys())), 200)

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
#If policy has status schema the no query parameters is allowed but a status json shall be provided
#/status?policyid=<policyid>[&status=<status>[&reason=<reason>]]
@app.route('/status', methods=['PUT'])
def setstatus():

  policyId=request.args.get('policyid')
  if (policyId is None):
    return Response('Parameter <policyid> missing in request', status=400, mimetype='text/plain')
  if policyId not in policy_instances.keys():
    return Response('Policyid: '+policyId+' not found.', status=404, mimetype='text/plain')
  policyTypeId=policy_instance_to_type[policyId]
  statusSchema=None
  if policyTypeId is not None:
    if 'statusSchema' in policy_types[policyTypeId].keys():
      statusSchema=policy_types[policyTypeId]['statusSchema']
  status=request.args.get('status')

  if policyTypeId is None:
    if status is None:
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
  else:
    if status is not None:
       return Response('Policy has schema defined. Not possible to set status by value', status=400, mimetype='text/plain')
    if statusSchema is None:
      return Response('Policy has not status schema defined. Not possible to set status', status=400, mimetype='text/plain')

    try:
      data = request.data
      data = json.loads(data)
    except:
      return Response("The policy status json is corrupt or missing", 400, mimetype='text/plain')
    try:
      validate(instance=data, schema=statusSchema)
    except:
      return Response("The policy status does not validate towards the policy type status schema.", 400, mimetype='text/plain')
    policy_status[policyId] = data
    msg="Status set to: "+json.dumps(data)+" for policy "+ policyId
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
    return Response(str(len(policy_types)),200, mimetype='text/plain')
  elif (countername == "interface"):
    p=Path(os.getcwd())
    pp=p.parts
    return Response(str(pp[len(pp)-1]),200, mimetype='text/plain')
  elif (countername == "remote_hosts"):
    hosts=",".join(hosts_set)
    return str(hosts),200
  else:
    return Response("Counter name: "+countername+" not found.",404, mimetype='text/plain')

port_number = 8085
if len(sys.argv) >= 2:
  if isinstance(sys.argv[1], int):
    port_number = sys.argv[1]

port_number_secure=8185

app.add_api('alpha_x_A1.yaml')
context=get_security_context()
if (context == None):
  print("Start on non-secure port: "+str(port_number))
  app.run(port=port_number, host="::")
else:
  print("Start on secure port: "+str(port_number_secure))
  app.run(port=port_number_secure, host="::", ssl_context=context)
