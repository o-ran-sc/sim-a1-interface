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

import json
import datetime
import time

from datetime import datetime
from connexion import NoContent
from flask import Flask, request, Response
from jsonschema import validate
from var_declaration import policy_instances, policy_types, policy_status, policy_fingerprint, forced_settings, hosts_set
from utils import calcFingerprint
from maincommon import extract_host_name


# API Function: Health check
def get_healthcheck():

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  return (None, 200)

# API Function: Get all policy type ids
def get_all_policy_types():

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  return (list(policy_instances.keys()), 200)

# API Function: Get a policy type
def get_policy_type(policy_type_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_types.keys()):
    return (None, 404)

  return Response(json.dumps(policy_types[policy_type_id]), 200, mimetype='application/json')

# API Function: Delete a policy type
def delete_policy_type(policy_type_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    return (None, 404)

  if (len(policy_instances[policy_type_id]) > 0):
    return (None, 400)

  del policy_instances[policy_type_id]
  del policy_types[policy_type_id]

  return (None, 204)


# API Function: Create a policy type
def create_policy_type(policy_type_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id in policy_instances.keys()):
    if (len(policy_instances[policy_type_id]) > 0):
      return (None, 400)

  try:
    data = request.data
    data = json.loads(data)
  except:
    return (None, 400)

  if (('name' not in data.keys()) or ('description' not in data.keys()) or ('policy_type_id' not in data.keys()) or ('create_schema' not in data.keys())):
    return (None, 400)

  if (policy_type_id not in policy_instances.keys()):
    policy_instances[policy_type_id]={}

  policy_types[policy_type_id]=data

  return (None, 201)


# API Function: Get all policy ids for a type
def get_all_policy_identities(policy_type_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    return (None, 404)
  return (list(policy_instances[policy_type_id].keys()), 200)

# API Function: Get a policy instance
def get_policy_instance(policy_type_id, policy_instance_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    return (None, 404)

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    return (None, 404)

  return Response(json.dumps(policy_instances[policy_type_id][policy_instance_id]), 200, mimetype='application/json')

# API function: Delete a policy
def delete_policy_instance(policy_type_id, policy_instance_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    return (None, 404)

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    return (None, 404)

  fpPrevious=calcFingerprint(policy_type_id, policy_instances[policy_type_id][policy_instance_id])
  del policy_fingerprint[fpPrevious]
  del policy_instances[policy_type_id][policy_instance_id]
  del policy_status[policy_instance_id]

  return (None, 202)

# API function: Create/update a policy
def create_or_replace_policy_instance(policy_type_id, policy_instance_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    return (None, 404)

  try:
    data = request.data
    data = json.loads(data)
  except:
    return (None, 400)

  try:
    validate(instance=data, schema=policy_types[policy_type_id]['create_schema'])
  except:
    return (None, 400)

  fpPrevious=None
  retcode=201
  if policy_instance_id in policy_instances[policy_type_id].keys():
    retcode=200
    fpPrevious=calcFingerprint(policy_type_id, policy_instances[policy_type_id][policy_instance_id])
  else:
    if (policy_instance_id in policy_fingerprint.values()):
      return (None, 400)

  fp=calcFingerprint(policy_type_id, data)
  if (fp in policy_fingerprint.keys()):
    id=policy_fingerprint[fp]
    if (id != policy_instance_id):
      return (None, 400)

  if (fpPrevious is not None):
    del policy_fingerprint[fpPrevious]

  policy_fingerprint[fp]=policy_instance_id

  policy_instances[policy_type_id][policy_instance_id]=data
  ps={}
  ps["instance_status"] = "NOT IN EFFECT"
  ps["has_been_deleted"] = "false"
  ps["created_at"] = str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
  policy_status[policy_instance_id]=ps

  return (None, 202)

# API function: Get policy status
def get_policy_instance_status(policy_type_id, policy_instance_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)
  if (policy_type_id not in policy_instances.keys()):
    return (None, 404)

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    return (None, 404)

  return Response(json.dumps(policy_status[policy_instance_id]), 200, mimetype='application/json')

# Helper: Create a response object if forced http response code is set
def get_forced_response():

  response_code=forced_settings['code']
  if (response_code is not None):
    forced_settings['code'] = None
    return (None, response_code)
  return None

# Helper: Delay if delayed response code is set
def do_delay():

  if (forced_settings['delay'] is not None):
    try:
      val=int(forced_settings['delay'])
      time.sleep(val)
    except:
      return
  return

# Helper: Check if response shall be delayed or a forced response shall be sent
def check_modified_response():
  do_delay()
  return get_forced_response()