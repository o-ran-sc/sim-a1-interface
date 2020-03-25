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
from var_declaration import policy_instances, policy_types, policy_status, policy_fingerprint, forced_settings
from utils import calcFingerprint

# API Function: Health check
def get_healthcheck():

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  return Response('', 200, mimetype='application/json')

# API Function: Get all policy type ids
def get_all_policy_types():

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  return (list(policy_instances.keys()), 200)

# API Function: Get a policy type
def get_policy_type(policy_type_id):

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_types.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  return Response(json.dumps(policy_types[policy_type_id]), 200, mimetype='application/problem+json')

# API Function: Delete a policy type
def delete_policy_type(policy_type_id):

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  if (len(policy_instances[policy_type_id]) > 0):
    pjson=create_problem_json(None, "The policy type cannot be deleted, instances exists.", 400, None, policy_type_id)
    return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  del policy_instances[policy_type_id]
  del policy_types[policy_type_id]

  return Response('', 204, mimetype='application/json')

# API Function: Create a policy type
def create_policy_type(policy_type_id):

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id in policy_instances.keys()):
    if (len(policy_instances[policy_type_id]) > 0):
      pjson=create_problem_json(None, "The policy type cannot be updated, instances exists.", 400, None, policy_type_id)
      return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  try:
    data = request.data
    data = json.loads(data)
  except:
    pjson=create_problem_json(None, "The policy type is corrupt or missing.", 400, None, policy_type_id)
    return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  if (('name' not in data.keys()) or ('description' not in data.keys()) or ('policy_type_id' not in data.keys()) or ('create_schema' not in data.keys())):
    pjson=create_problem_json(None, "The policy type is missing attributes.", 400, None, policy_type_id)
    return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  retcode=201
  if (policy_type_id in policy_instances.keys()):
    retcode=200
  else:
    policy_instances[policy_type_id]={}

  policy_types[policy_type_id]=data

  if (retcode == 200):
    return Response(json.dumps(data), 200, mimetype='application/json')
  else:
    return Response(json.dumps(data), 201, mimetype='application/json')



# API Function: Get all policy ids for a type
def get_all_policy_identities(policy_type_id):

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')
  return (list(policy_instances[policy_type_id].keys()), 200)

# API Function: Get a policy instance
def get_policy_instance(policy_type_id, policy_instance_id):

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    pjson=create_problem_json(None, "The policy instance does not exist.", 404, None, policy_instance_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  return Response(json.dumps(policy_instances[policy_type_id][policy_instance_id]), 200, mimetype='application/json')

# API function: Delete  A POLICY
def delete_policy_instance(policy_type_id, policy_instance_id):

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    pjson=create_problem_json(None, "The policy instance does not exist.", 404, None, policy_instance_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  fpPrevious=calcFingerprint(policy_instances[policy_type_id][policy_instance_id])
  del policy_fingerprint[fpPrevious]
  del policy_instances[policy_type_id][policy_instance_id]
  del policy_status[policy_instance_id]

  return Response('', 204, mimetype='application/problem+json')

# API function: Create/update a policy
def create_or_replace_policy_instance(policy_type_id, policy_instance_id):

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  try:
    data = request.data
    data = json.loads(data)
  except:
    pjson=create_problem_json(None, "The policy is corrupt or missing.", 400, None, policy_instance_id)
    return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  try:
    validate(instance=data, schema=policy_types[policy_type_id]['create_schema'])
  except:
    pjson=create_problem_json(None, "The policy does not match type.", 400, None, policy_instance_id)
    return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  fpPrevious=None
  retcode=201
  if policy_instance_id in policy_instances[policy_type_id].keys():
    retcode=200
    fpPrevious=calcFingerprint(policy_instances[policy_type_id][policy_instance_id])
  else:
    if (policy_instance_id in policy_fingerprint.values()):
      pjson=create_problem_json(None, "The policy id already exists for other type.", 400, None, policy_instance_id)
      return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  fp=calcFingerprint(data)
  if (fp in policy_fingerprint.keys()):
    id=policy_fingerprint[fp]
    if (id != policy_instance_id):
      pjson=create_problem_json(None, "The policy json already exists.", 400, None, policy_instance_id)
      return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  if (fpPrevious is not None):
    del policy_fingerprint[fpPrevious]

  policy_fingerprint[fp]=policy_instance_id

  policy_instances[policy_type_id][policy_instance_id]=data
  ps={}
  ps["instance_status"] = "NOT IN EFFECT"
  ps["has_been_deleted"] = "false"
  ps["created_at"] = str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
  policy_status[policy_instance_id]=ps

  if (retcode == 200):
    return Response(json.dumps(data), 200, mimetype='application/json')
  else:
    return Response(json.dumps(data), 201, mimetype='application/json')

# API function: Get policy status
def get_policy_instance_status(policy_type_id, policy_instance_id):

  do_delay()
  r = get_forced_response()
  if (r is not None):
    return r

  policy_type_id=str(policy_type_id)
  if (policy_type_id not in policy_instances.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    pjson=create_problem_json(None, "The policy instance does not exist.", 404, None, policy_instance_id)
    return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  return Response(json.dumps(policy_status[policy_instance_id]), 200, mimetype='application/json')

# Helper: Create a response object if forced http response code is set
def get_forced_response():

  if (forced_settings['code'] is not None):
    pjson=create_error_response(forced_settings['code'])
    forced_settings['code']=None
    return Response(json.dumps(pjson), pjson['status'], mimetype='application/problem+json')
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

# Helper: Create a problem json object
def create_problem_json(type_of, title, status, detail, instance):

  error = {}
  if type_of is not None:
    error["type"] = type_of
  else:
    error["type"] = "about:blank"
  if title is not None:
    error["title"] = title
  if status is not None:
    error["status"] = status
  if detail is not None:
    error["detail"] = detail
  if instance is not None:
    error["instance"] = instance
  return error

# Helper: Create a problem json based on a generic http response code
def create_error_response(code):

    if code == '405':
      return(create_problem_json(None, "Method not allowed", 405, "Method not allowed for the URI", None))
    elif code == '429':
      return(create_problem_json(None, "Too many requests", 429, "Too many requests have been sent in a given amount of time", None))
    elif code == '507':
      return(create_problem_json(None, "Insufficient storage", 507, "The method could not be performed on the resource because the provider is unable to store the representation needed to successfully complete the request", None))
    elif code == '503':
      return(create_problem_json(None, "Service unavailable", 503, "The provider is currently unable to handle the request due to a temporary overload", None))
    else:
      return(create_problem_json(None, "Not found", code, "No resource found at the URI", None))

