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

import copy
import datetime
import json
import logging
import collections
import time

from connexion import NoContent
from flask import Flask, escape, request, Response, make_response
from jsonschema import validate
from var_declaration import policy_instances, policy_types, policy_status, callbacks, forced_settings, policy_fingerprint, hosts_set
from utils import calcFingerprint
from maincommon import check_apipath, apipath, get_supported_interfaces_response, extract_host_name, is_duplicate_check

#Constsants
APPL_JSON='application/json'
APPL_PROB_JSON='application/problem+json'

# API Function: Get all policy type ids
def get_all_policy_types():

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  res = list(policy_types.keys())
  return (res, 200)

# API Function: Get a policy type
def get_policy_type(policyTypeId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)

  if (policy_type_id not in policy_types.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  return Response(json.dumps(policy_types[policy_type_id]), 200, mimetype=APPL_JSON)

# API Function: Get all policy ids
def get_all_policy_identities(policyTypeId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)

  if (policy_type_id not in policy_types.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  return (list(policy_instances[policy_type_id].keys()), 200)

# API Function: Create or update a policy
def put_policy(policyTypeId, policyId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)
  policy_id=str(policyId)

  if (policy_type_id not in policy_types.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  try:
    data = request.data
    data = json.loads(data)
  except Exception:
    pjson=create_problem_json(None, "The policy is corrupt or missing.", 400, None, policy_id)
    return Response(json.dumps(pjson), 400, mimetype=APPL_PROB_JSON)

  try:
    validate(instance=data, schema=policy_types[policy_type_id]['policySchema'])
  except Exception:
    return (None, 400)

  fp_previous=None
  retcode=201
  if policy_id in policy_instances[policy_type_id].keys():
    retcode=200
    if (is_duplicate_check()):
      fp_previous=calcFingerprint(policy_instances[policy_type_id][policy_id], policy_type_id)
    else:
      fp_previous=policy_id
  else:
    if (policy_id in policy_fingerprint.values()):
      pjson=create_problem_json(None, "The policy id already exist for other policy type.", 400, None, policy_id)
      return Response(json.dumps(pjson), 400, mimetype=APPL_PROB_JSON)

  if (is_duplicate_check()):
    fp=calcFingerprint(data, policy_type_id)
  else:
    fp=policy_id

  if ((fp in policy_fingerprint.keys()) and is_duplicate_check()):
    p_id=policy_fingerprint[fp]
    if (p_id != policy_id):
      pjson=create_problem_json(None, "Duplicate, the policy json already exists.", 400, None, policy_id)
      return Response(json.dumps(pjson), 400, mimetype=APPL_PROB_JSON)

  if (fp_previous is not None):
    del policy_fingerprint[fp_previous]

  policy_fingerprint[fp]=policy_id

  noti=request.args.get('notificationDestination')
  callbacks[policy_id]=noti

  policy_instances[policy_type_id][policy_id]=data

  if (policy_types[policy_type_id]['statusSchema'] is not None):
    ps = {}
    ps["enforceStatus"] = ""
    ps["enforceReason"] = ""
    policy_status[policy_id] = ps

  if (retcode == 200):
    return Response(json.dumps(data), 200, mimetype=APPL_JSON)
  else:
    headers={}
    headers['Location']='/A1-P/v2/policytypes/' + policy_type_id + '/policies/' + policy_id
    return Response(json.dumps(data), 201, headers=headers, mimetype=APPL_JSON)

# API Function: Get a policy
def get_policy(policyTypeId, policyId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)
  policy_id=str(policyId)

  if (policy_type_id not in policy_types.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  if (policy_id not in policy_instances[policy_type_id].keys()):
    pjson=create_problem_json(None, "The requested policy does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  return Response(json.dumps(policy_instances[policy_type_id][policy_id]), 200, mimetype=APPL_JSON)


# API Function: Delete a policy
def delete_policy(policyTypeId, policyId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)
  policy_id=str(policyId)

  if (policy_type_id not in policy_types.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  if (policy_id not in policy_instances[policy_type_id].keys()):
    pjson=create_problem_json(None, "The requested policy does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  if (is_duplicate_check()):
    fp_previous=calcFingerprint(policy_instances[policy_type_id][policy_id], policy_type_id)
  else:
    fp_previous=policy_id

  policy_fingerprint.pop(fp_previous)
  policy_instances[policy_type_id].pop(policy_id)
  policy_status.pop(policy_id)
  callbacks.pop(policy_id)
  return Response('', 204, mimetype=APPL_JSON)


# API Function: Get status for a policy
def get_policy_status(policyTypeId, policyId):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)
  policy_id=str(policyId)

  if (policy_type_id not in policy_types.keys()):
    pjson=create_problem_json(None, "The policy type does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  if (policy_id not in policy_instances[policy_type_id].keys()):
    pjson=create_problem_json(None, "The requested policy does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  return Response(json.dumps(policy_status[policy_id]), status=200, mimetype=APPL_JSON)

# Helper: Create a response object if forced http response code is set
def get_forced_response():
  if (forced_settings['code'] is not None):
    pjson=create_error_response(forced_settings['code'])
    forced_settings['code']=None
    return Response(json.dumps(pjson), pjson['status'], mimetype=APPL_PROB_JSON)
  return None

# Helper: Delay if delayed response code is set
def do_delay():
  if (forced_settings['delay'] is not None):
    try:
      val=int(forced_settings['delay'])
      time.sleep(val)
    except Exception:
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
