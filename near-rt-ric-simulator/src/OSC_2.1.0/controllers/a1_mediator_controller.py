#  ============LICENSE_START===============================================
#  Copyright (C) 2021-2023 Nordix Foundation. All rights reserved.
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
# import datetime
import time

from datetime import datetime
from flask import request, Response
from jsonschema import validate
from var_declaration import policy_instances, policy_types, policy_status, policy_fingerprint, forced_settings, hosts_set, jobs, data_delivery
from utils import calcFingerprint
from maincommon import extract_host_name, is_duplicate_check
from payload_logging import is_payload_logging

#Constsants
APPL_JSON='application/json'

#Helper funtion to log http reponse
def log_resp_text(msg):
  global payload_log
  if (is_payload_logging()):
    print("-----Error description-----")
    print(str(msg))

# API Function: Health check
def a1_controller_get_healthcheck():

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  return (None, 200)

# API Function: Get all policy type ids
def a1_controller_get_all_policy_types():
  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  res = list(policy_instances.keys())
  res = list(map(int, res))
  return (res, 200)

# API Function: Get a policy type
def a1_controller_get_policy_type(policy_type_id):
  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_types.keys()):
    log_resp_text("Policy type id not found")
    return (None, 404)

  return Response(json.dumps(policy_types[policy_type_id]), 200, mimetype=APPL_JSON)

# API Function: Delete a policy type
def a1_controller_delete_policy_type(policy_type_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    log_resp_text("Policy type not found")
    return (None, 404)

  if (len(policy_instances[policy_type_id]) > 0):
    log_resp_text("Policy type cannot be removed, instances exists")
    return (None, 400)

  del policy_instances[policy_type_id]
  del policy_types[policy_type_id]

  return (None, 204)


# API Function: Create a policy type
def a1_controller_create_policy_type(policy_type_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  try:
    int(policy_type_id)
  except Exception:
    return Response("The policy type id is not an int", 400, mimetype='text/plain')

  policy_type_id=str(policy_type_id)

  if (policy_type_id in policy_instances.keys()):
    if (len(policy_instances[policy_type_id]) > 0):
      log_resp_text("Policy type id already exists")
      return (None, 400)

  try:
    data = request.data
    data = json.loads(data)
  except Exception:
    log_resp_text("Policy type validation failure")
    return (None, 400)

  if (('name' not in data.keys()) or ('description' not in data.keys()) or ('policy_type_id' not in data.keys()) or ('create_schema' not in data.keys())):
    log_resp_text("Parameters missing in policy type")
    return (None, 400)

  if (policy_type_id not in policy_instances.keys()):
    policy_instances[policy_type_id]={}

  policy_types[policy_type_id]=data

  return (None, 201)


# API Function: Get all policy ids for a type
def  a1_controller_get_all_instances_for_type(policy_type_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    log_resp_text("Policy type id not found")
    return (None, 404)
  return (list(policy_instances[policy_type_id].keys()), 200)

# API Function: Get a policy instance
def a1_controller_get_policy_instance(policy_type_id, policy_instance_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    log_resp_text("Policy type id not found")
    return (None, 404)

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    log_resp_text("Policy instance id not found")
    return (None, 404)

  return Response(json.dumps(policy_instances[policy_type_id][policy_instance_id]), 200, mimetype=APPL_JSON)

# API function: Delete a policy
def a1_controller_delete_policy_instance(policy_type_id, policy_instance_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    log_resp_text("Policy type id not found")
    return (None, 404)

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    log_resp_text("Policy instance id not found")
    return (None, 404)

  if (is_duplicate_check()):
    fp_previous=calcFingerprint(policy_instances[policy_type_id][policy_instance_id], policy_type_id)
  else:
    fp_previous=policy_instance_id

  del policy_fingerprint[fp_previous]
  del policy_instances[policy_type_id][policy_instance_id]
  del policy_status[policy_instance_id]

  return (None, 202)


# API function: Create/update a policy
def a1_controller_create_or_replace_policy_instance(policy_type_id, policy_instance_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)

  if (policy_type_id not in policy_instances.keys()):
    log_resp_text("Policy type id not found")
    return (None, 404)

  try:
    data = request.data
    data = json.loads(data)
  except Exception:
    log_resp_text("Policy json error")
    return (None, 400)

  try:
    validate(instance=data, schema=policy_types[policy_type_id]['create_schema'])
  except Exception:
    log_resp_text("Policy validation error")
    return (None, 400)

  fp_previous=None
  if policy_instance_id in policy_instances[policy_type_id].keys():
    if (is_duplicate_check()):
      fp_previous=calcFingerprint(policy_instances[policy_type_id][policy_instance_id], policy_type_id)
    else:
      fp_previous=policy_instance_id

  else:
    if (policy_instance_id in policy_fingerprint.values()):
      log_resp_text("Policy id already exist for other type")
      return (None, 400)

  if (is_duplicate_check()):
    fp=calcFingerprint(data, policy_type_id)
  else:
    fp=policy_instance_id

  if ((fp in policy_fingerprint.keys()) and is_duplicate_check()):
    p_id=policy_fingerprint[fp]
    if (p_id != policy_instance_id):
      log_resp_text("Policy json duplicate of other instance")
      return (None, 400)

  if (fp_previous is not None):
    del policy_fingerprint[fp_previous]

  policy_fingerprint[fp]=policy_instance_id

  policy_instances[policy_type_id][policy_instance_id]=data
  ps={}
  ps["instance_status"] = "NOT IN EFFECT"
  ps["has_been_deleted"] = "false"
  ps["created_at"] = str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
  policy_status[policy_instance_id]=ps

  return (None, 202)


# API function: Get policy status
def a1_controller_get_policy_instance_status(policy_type_id, policy_instance_id):

  extract_host_name(hosts_set, request)

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policy_type_id)
  if (policy_type_id not in policy_instances.keys()):
    log_resp_text("Policy type id not found")
    return (None, 404)

  if (policy_instance_id not in policy_instances[policy_type_id].keys()):
    log_resp_text("Policy instance id not found")
    return (None, 404)

  return Response(json.dumps(policy_status[policy_instance_id]), 200, mimetype=APPL_JSON)

# API function: Receive a data delivery package
def a1_controller_data_delivery():
 
  extract_host_name(hosts_set, request)
  if ((r := check_modified_response()) is not None):
    return r

  try:
    data = request.data
    data = json.loads(data)
    job = data['job']
    jobs.index(job)
  except ValueError:
    log_resp_text("no job id defined for this data delivery")
    return (None, 404)
  except Exception:
    log_resp_text("The data is corrupt or missing.")
    return (None, 400)
  data_delivery.append(data)
  return (None, 200) # Should A1 and the A1 Simulator return 201 for creating a new resource?

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
    except Exception:
      return

# Helper: Check if response shall be delayed or a forced response shall be sent
def check_modified_response():
  do_delay()
  return get_forced_response()