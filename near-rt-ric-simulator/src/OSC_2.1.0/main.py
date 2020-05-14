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
from var_declaration import policy_instances, policy_types, policy_status, policy_fingerprint, forced_settings, hosts_set
from maincommon import *


check_apipath()

app = connexion.FlaskApp(__name__, specification_dir=apipath)

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
def deleteinstances():

  for i in policy_instances.keys():
    policy_instances[i]={}

  policy_status.clear()
  forced_settings.clear()
  forced_settings['code']=None
  forced_settings['delay']=None
  policy_fingerprint.clear()
  return Response("All policy instances deleted", 200, mimetype='text/plain')

#Delete all - all reset
@app.route('/deleteall', methods=['POST'])
def deleteall():

  policy_instances.clear()
  policy_types.clear()
  policy_status.clear()
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
    val=int(policyTypeId)
  except:
    return Response("The policy type id is not an int", 400, mimetype='text/plain')
  try:
    data = request.data
    data = json.loads(data)
  except:
    return Response("The policy type is corrupt or missing", 400, mimetype='text/plain')

  if ('name' not in data.keys() or 'description' not in data.keys() or 'policy_type_id' not in data.keys() or'create_schema' not in data.keys()):
    return Response("The policy type missing atributes", 400, mimetype='text/plain')

  retcode=201
  if (policyTypeId in policy_types.keys()):
    retcode=200
    if (len(policy_instances[policyTypeId]) > 0):
      return Response("The policy type already exists and instances exists", 400, mimetype='text/plain')

  policy_types[policyTypeId]=data
  policy_instances[policyTypeId]={}
  return Response("Policy type " + policyTypeId + " is OK.", retcode, mimetype='text/plain')

#Delete a policy type
@app.route('/policytype', methods=['DELETE'])
def del_policytype():

  policyTypeId=request.args.get('id')
  if (policyTypeId is None):
    return Response('Parameter <id> missing in request', status=400, mimetype='text/plain')
  try:
    val=int(policyTypeId)
  except:
    return Response("The policy type id is not an int", 400, mimetype='text/plain')

  if (policyTypeId in policy_types.keys()):
    if (len(policy_instances[policyTypeId]) > 0):
      return Response("The policy type already exists and instances exists", 400, mimetype='text/plain')

    del policy_types[policyTypeId]
    del policy_instances[policyTypeId]
    return Response("Policy type " + policyTypeId + " is OK.", 204, mimetype='text/plain')

  return Response("Policy type " + policyTypeId + " not found.", 204, mimetype='text/plain')


# Get all policy type ids
@app.route('/policytypes', methods=['GET'])
def get_policytype_ids():

  return (json.dumps(list(policy_instances.keys())), 200)

#Set force response for one A1 response
#/forceresponse?code=<responsecode>
@app.route('/forceresponse', methods=['POST'])
def forceresponse():

  try:
    forced_settings['code']=int(request.args.get('code'))
  except:
    forced_settings['code']=None
  return Response("Force response code: " + str(forced_settings['code']) + " set for one single A1 response", 200, mimetype='text/plain')

#Set force delay response, in seconds, for all A1 responses
#/froceesponse?delay=<seconds>
@app.route('/forcedelay', methods=['POST'])
def forcedelay():

  try:
    forced_settings['delay']=int(request.args.get('delay'))
  except:
    forced_settings['delay']=None
  return Response("Force delay: " + str(forced_settings['delay']) + " sec set for all A1 responses", 200, mimetype='text/plain')


#Set status and reason
#/status?policyid=<policyid>&status=<status>[&deleted=<boolean>][&created_at=<timestamp>]
@app.route('/status', methods=['PUT'])
def setstatus():

  policyId=request.args.get('policyid')
  if (policyId is None):
    return Response('Parameter <policyid> missing in request', status=400, mimetype='text/plain')

  if policyId not in policy_status.keys():
    return Response('Policyid: '+policyId+' not found.', status=404, mimetype='text/plain')
  status=request.args.get('status')
  if (status is None):
    return Response('Parameter <status> missing in request', status=400, mimetype='text/plain')
  policy_status[policyId]["instance_status"]=status
  msg = "Status set to "+status
  deleted_policy=request.args.get('deleted')
  if (deleted_policy is not None):
    policy_status[policyId]["has_been_deleted"]=deleted_policy
    msg = msg + " and has_been_deleted set to "+deleted_policy
  created_at = request.args.get('created_at')
  if (created_at is not None):
    policy_status[policyId]["created_at"]=created_at
    msg = msg + " and created_at set to "+created_at
  msg=msg + " for policy: " + policyId
  return Response(msg, 200, mimetype='text/plain')


#Metrics function
#Get a named counter
@app.route('/counter/<string:countername>', methods=['GET'])
def getCounter(countername):

  if (countername == "num_instances"):
    return Response(str(len(policy_fingerprint)), 200, mimetype='text/plain')
  elif (countername == "num_types"):
    return Response(str(len(policy_instances)),200, mimetype='text/plain')
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

app.add_api('openapi.yaml')

print("Start on non-secure port: "+str(port_number))
app.run(port=port_number, host="::")