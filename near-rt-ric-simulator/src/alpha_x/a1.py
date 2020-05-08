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

import copy
import datetime
import json
import logging
import collections
import time

from jsonschema import validate
from connexion import NoContent
from flask import Flask, escape, request, Response, make_response
from var_declaration import policy_instances, policy_status, callbacks, forced_settings, policy_fingerprint, hosts_set, policy_types, policy_instance_to_type
from utils import calcFingerprint
from maincommon import *

# API Function: Get all policy ids
def get_all_policy_identities():

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policyTypeId=request.args.get('policyTypeId')

  if (policyTypeId is None):
    return (list(policy_instances.keys()), 200)

  ids=[]
  for key in policy_instance_to_type.keys():
    if (policy_instance_to_type[key] == policyTypeId):
      ids.append(key)

  return (ids, 200)

# API Function: Create or update a policy
def put_policy(policyId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policyTypeId=request.args.get('policyTypeId')

  if (policyTypeId is not None):
    if (policyTypeId not in policy_types.keys()):
      pjson=create_problem_json(None, "The policy  type does not exist.", 404, None, policyTypeId)
      return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

  try:
    data = request.data
    data = json.loads(data)
  except:
    pjson=create_problem_json(None, "The policy is corrupt or missing.", 400, None, policyId)
    return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  if (policyTypeId is not None):
    try:
      validate(instance=data, schema=policy_types[policyTypeId]['policySchema'])
    except:
      pjson=create_problem_json(None, "The policy does not validate towards the policy type schema.", 400, None, policyId)
      return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  fpPrevious=None
  retcode=201
  if policyId in policy_instances.keys():
    retcode=200
    fpPrevious=calcFingerprint(policyTypeId, policy_instances[policyId])
    if (policy_instance_to_type[policyId] != policyTypeId):
      pjson=create_problem_json(None, "The policy is not allowed to change type allocation.", 400, None, policyId)
      return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  fp=calcFingerprint(policyTypeId, data)
  if (fp in policy_fingerprint.keys()):
    id=policy_fingerprint[fp]
    if (id != policyId):
      pjson=create_problem_json(None, "The policy json already exists.", 400, None, policyId)
      return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

  if (fpPrevious is not None):
    del policy_fingerprint[fpPrevious]

  policy_fingerprint[fp]=policyId

  noti=request.args.get('notificationDestination')
  callbacks[policyId]=noti

  policy_instances[policyId]=data
  policy_instance_to_type[policyId]=policyTypeId

  if (policyTypeId is None):
    ps={}
    ps["enforceStatus"] = "UNDEFINED"
    policy_status[policyId]=ps
  else:
    policy_status[policyId]=None

  if (retcode == 200):
    return Response(json.dumps(data), 200, mimetype='application/json')
  else:
    headers={}
    headers['Location']='/A1-P/v1/policies/' + policyId
    return Response(json.dumps(data), 201, headers=headers, mimetype='application/json')

# API Function: Get a policy
def get_policy(policyId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  if policyId in policy_instances.keys():
    return Response(json.dumps(policy_instances[policyId]), 200, mimetype='application/json')

  pjson=create_problem_json(None, "The requested policy does not exist.", 404, None, policyId)
  return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

# API Function: Delete a policy
def delete_policy(policyId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  if policyId in policy_instances.keys():
    policyTypeId=policy_instance_to_type[policyId]
    fpPrevious=calcFingerprint(policyTypeId, policy_instances[policyId])
    policy_fingerprint.pop(fpPrevious)
    policy_instances.pop(policyId)
    policy_status.pop(policyId)
    callbacks.pop(policyId)
    policy_instance_to_type.pop(policyId)
    return Response('', 204, mimetype='application/json')

  pjson=create_problem_json(None, "The policy identity does not exist.", 404, "No policy instance has been deleted.", policyId)
  return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

# API Function: Get status for a policy
def get_policy_status(policyId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  if policyId in policy_instances.keys():

    policyTypeId=policy_instance_to_type[policyId]
    if (policyTypeId is not None):
      if policy_types[policyTypeId]['policySchema'] is None:
        pjson=create_problem_json(None, "The status schemas does not exist.", 400, "The policy type status schemas does not exists ", policyId)
        return Response(json.dumps(pjson), 400, mimetype='application/problem+json')

    if policy_status[policyId] is None:
      pjson=create_problem_json(None, "The policy status is not set.", 400, "The policy exists but has not status set", policyId)
      return Response(json.dumps(pjson), 400, mimetype='application/problem+json')
    return Response(json.dumps(policy_status[policyId]), status=200, mimetype='application/json')

  pjson=create_problem_json(None, "The policy identity does not exist.", 404, "There is no existing policy instance with the identity: " + policyId, policyId)
  return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

# API Function: Get all policy type ids
def get_all_policytype_identities():

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  return (list(policy_types.keys()), 200)

# API Function: Get a policy type
def get_policytype(policyTypeId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  if policyTypeId in policy_types.keys():
    return Response(json.dumps(policy_types[policyTypeId]), 200, mimetype='application/json')

  pjson=create_problem_json(None, "The requested policy type does not exist.", 404, None, policyTypeId)
  return Response(json.dumps(pjson), 404, mimetype='application/problem+json')

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

# Helper: Check if response shall be delayed or a forced response shall be sent
def check_modified_response():
  do_delay()
  return get_forced_response()

# Helper: Create a problem json object
def create_problem_json(type_of, title, status, detail, instance):

  error = {}
  if type_of is not None:
    error["type"] = type_of
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

    if code == '400':
      return(create_problem_json(None, "Bad request", 400, "Object in payload not properly formulated or not related to the method", None))
    elif code == '404':
      return(create_problem_json(None, "Not found", 404, "No resource found at the URI", None))
    elif code == '405':
      return(create_problem_json(None, "Method not allowed", 405, "Method not allowed for the URI", None))
    elif code == '409':
      return(create_problem_json(None, "Conflict", 409, "Request could not be processed in the current state of the resource", None))
    elif code == '429':
      return(create_problem_json(None, "Too many requests", 429, "Too many requests have been sent in a given amount of time", None))
    elif code == '507':
      return(create_problem_json(None, "Insufficient storage", 507, "The method could not be performed on the resource because the provider is unable to store the representation needed to successfully complete the request", None))
    elif code == '503':
      return(create_problem_json(None, "Service unavailable", 503, "The provider is currently unable to handle the request due to a temporary overload", None))
    else:
      return(create_problem_json(None, "Unknown", code, "Not implemented response code", None))
