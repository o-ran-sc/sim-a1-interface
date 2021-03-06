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
from flask import Flask, escape, request, Response, jsonify
from jsonschema import validate
from var_declaration import policy_instances, policy_types, policy_status, policy_fingerprint, forced_settings, hosts_set
from maincommon import check_apipath, apipath, get_supported_interfaces_response, extract_host_name
from time import sleep

#Constants
TEXT_PLAIN='text/plain'

check_apipath()

app = connexion.FlaskApp(__name__, specification_dir=apipath)

#Check alive function
@app.route('/', methods=['GET'])
def test():

    return Response("OK", 200, mimetype=TEXT_PLAIN)

@app.route('/ip', methods=['GET'])
def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return jsonify({'ip': request.environ['REMOTE_ADDR']}), 200
    else:
        return jsonify({'ip': request.environ['HTTP_X_FORWARDED_FOR']}), 200

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
  return Response("All policy instances deleted", 200, mimetype=TEXT_PLAIN)

#Delete all - all reset
@app.route('/deleteall', methods=['POST'])
def deleteall():

  policy_instances.clear()
  policy_types.clear()
  policy_status.clear()
  forced_settings['code']=None
  forced_settings['delay']=None
  policy_fingerprint.clear()
  return Response("All policy instances and types deleted", 200, mimetype=TEXT_PLAIN)

#Load a policy type
@app.route('/policytype', methods=['PUT'])
def policytype():

  policy_type_id=request.args.get('id')
  if (policy_type_id is None):
    return Response('Parameter <id> missing in request', status=400, mimetype=TEXT_PLAIN)
  try:
    int(policy_type_id)
  except Exception:
    return Response("The policy type id is not an int", 400, mimetype=TEXT_PLAIN)
  try:
    data = request.data
    data = json.loads(data)
  except Exception:
    return Response("The policy type is corrupt or missing", 400, mimetype=TEXT_PLAIN)

  if ('name' not in data.keys() or 'description' not in data.keys() or 'policy_type_id' not in data.keys() or'create_schema' not in data.keys()):
    return Response("The policy type missing atributes", 400, mimetype=TEXT_PLAIN)

  retcode=201
  if (policy_type_id in policy_types.keys()):
    retcode=200
    if (len(policy_instances[policy_type_id]) > 0):
      return Response("The policy type already exists and instances exists", 400, mimetype=TEXT_PLAIN)

  policy_types[policy_type_id]=data
  policy_instances[policy_type_id]={}
  return Response("Policy type " + policy_type_id + " is OK.", retcode, mimetype=TEXT_PLAIN)

#Delete a policy type
@app.route('/policytype', methods=['DELETE'])
def del_policytype():

  policy_type_id=request.args.get('id')
  if (policy_type_id is None):
    return Response('Parameter <id> missing in request', status=400, mimetype=TEXT_PLAIN)
  try:
    int(policy_type_id)
  except Exception:
    return Response("The policy type id is not an int", 400, mimetype=TEXT_PLAIN)

  if (policy_type_id in policy_types.keys()):
    if (len(policy_instances[policy_type_id]) > 0):
      return Response("The policy type already exists and instances exists", 400, mimetype=TEXT_PLAIN)

    del policy_types[policy_type_id]
    del policy_instances[policy_type_id]
    return Response("Policy type " + policy_type_id + " is OK.", 204, mimetype=TEXT_PLAIN)

  return Response("Policy type " + policy_type_id + " not found.", 204, mimetype=TEXT_PLAIN)


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
  except Exception:
    forced_settings['code']=None
  return Response("Force response code: " + str(forced_settings['code']) + " set for one single A1 response", 200, mimetype=TEXT_PLAIN)

#Set force delay response, in seconds, for all A1 responses
#/froceesponse?delay=<seconds>
@app.route('/forcedelay', methods=['POST'])
def forcedelay():

  try:
    forced_settings['delay']=int(request.args.get('delay'))
  except Exception:
    forced_settings['delay']=None
  return Response("Force delay: " + str(forced_settings['delay']) + " sec set for all A1 responses", 200, mimetype=TEXT_PLAIN)


#Set status and reason
#/status?policyid=<policyid>&status=<status>[&deleted=<boolean>][&created_at=<timestamp>]
@app.route('/status', methods=['PUT'])
def setstatus():

  policy_id=request.args.get('policyid')
  if (policy_id is None):
    return Response('Parameter <policyid> missing in request', status=400, mimetype=TEXT_PLAIN)

  if policy_id not in policy_status.keys():
    return Response('Policyid: '+policy_id+' not found.', status=404, mimetype=TEXT_PLAIN)
  status=request.args.get('status')
  if (status is None):
    return Response('Parameter <status> missing in request', status=400, mimetype=TEXT_PLAIN)
  policy_status[policy_id]["instance_status"]=status
  msg = "Status set to "+status
  deleted_policy=request.args.get('deleted')
  if (deleted_policy is not None):
    policy_status[policy_id]["has_been_deleted"]=deleted_policy
    msg = msg + " and has_been_deleted set to "+deleted_policy
  created_at = request.args.get('created_at')
  if (created_at is not None):
    policy_status[policy_id]["created_at"]=created_at
    msg = msg + " and created_at set to "+created_at
  msg=msg + " for policy: " + policy_id
  return Response(msg, 200, mimetype=TEXT_PLAIN)


#Metrics function
#Get a named counter
@app.route('/counter/<string:countername>', methods=['GET'])
def getcounter(countername):

  if (countername == "num_instances"):
    return Response(str(len(policy_fingerprint)), 200, mimetype=TEXT_PLAIN)
  elif (countername == "num_types"):
    return Response(str(len(policy_instances)),200, mimetype=TEXT_PLAIN)
  elif (countername == "interface"):
    p=Path(os.getcwd())
    pp=p.parts
    return Response(str(pp[len(pp)-1]),200, mimetype=TEXT_PLAIN)
  elif (countername == "remote_hosts"):
    hosts=",".join(hosts_set)
    return str(hosts),200
  elif (countername == "datadelivery"):
    return Response(str(0),200, mimetype=TEXT_PLAIN)
  else:
    return Response("Counter name: "+countername+" not found.",404, mimetype=TEXT_PLAIN)

port_number = 2222
if len(sys.argv) >= 2 :
  if isinstance(sys.argv[1], int):
    port_number = sys.argv[1]

app.add_api('openapi.yaml')

if __name__ == '__main__':
  app.run(port=port_number, host="127.0.0.1", threaded=False)