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

import os
import json
import time

from flask import Flask, request, Response
from kafka import KafkaProducer
from kafka.errors import KafkaError
from var_declaration import a1_policy_instances, forced_settings

MSG_BROKER_URL=os.getenv('MSG_BROKER_URL')
MSG_BROKER_PORT=os.getenv('MSG_BROKER_PORT')
TOPIC_NAME=os.getenv('TOPIC_NAME')

#Constsants
APPL_JSON='application/json'
APPL_PROB_JSON='application/problem+json'

#Python implementation of KAFKA_DISPATCHER_api.yaml - Open API -

# API Function: Get all a1 policy ids
def get_all_policies():

  if ((r := check_modified_response()) is not None):
    return r

  res = list(a1_policy_instances)
  return (res, 200)

# API Function: Get A1 policy
def get_policy(policyTypeId, policyId):

  if ((r := check_modified_response()) is not None):
    return r

  policy_id=str(policyId)

  policykeys=a1_policy_instances.keys()
  if (policy_id not in policykeys):
    pjson=create_problem_json(None, "The A1 policy requested does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  return Response(json.dumps(a1_policy_instances[policy_id]), 200, mimetype=APPL_JSON)

# API Function: Dispatch create or update operation to south bound address
def put_policy(policyTypeId, policyId):

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)
  policy_id=str(policyId)

  try:
    data = request.data
    data = json.loads(data)
  except Exception:
    pjson=create_problem_json(None, "The a1policy is corrupt or missing.", 400, None, policy_id)
    return Response(json.dumps(pjson), 400, mimetype=APPL_PROB_JSON)

  policykeys=a1_policy_instances.keys()

  retcode=201
  if policy_id in policykeys:
    retcode=200

  msg_for_producer = create_kafka_message(policy_type_id, policy_id, data, 'PUT')

  #Callout hooks towards kafka broker
  if (MSG_BROKER_URL is not None):
    resp = send_kafka_message(msg_for_producer)
    if (resp is not None):
      pjson=create_error_response(resp)
      return Response(json.dumps(pjson), 500, mimetype=APPL_PROB_JSON)

  a1_policy_instances[policy_id]=data

  if (retcode == 200):
    return Response(json.dumps(data), 200, mimetype=APPL_JSON)
  else:
    headers={}
    headers['Location']='/a1policy/' + policy_id
    return Response(json.dumps(data), 201, headers=headers, mimetype=APPL_JSON)

# API Function: Delete a a1policy
def delete_policy(policyTypeId, policyId):

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)
  policy_id=str(policyId)

  policykeys=a1_policy_instances.keys()
  if (policy_id not in policykeys):
    pjson=create_problem_json(None, "The a1policy does not exist.", 404, None, policy_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)

  msg_for_producer = create_kafka_message(policy_type_id, policy_id, None, 'DELETE')

  #Callout hooks towards kafka broker
  if (MSG_BROKER_URL is not None):
    resp = send_kafka_message(msg_for_producer)
    if (resp is not None):
      pjson=create_error_response(resp)
      return Response(json.dumps(pjson), 500, mimetype=APPL_PROB_JSON)

  del a1_policy_instances[policy_id]
  return Response('', 204, mimetype=APPL_JSON)

# Helper: Sends messages to the target broker and the topic
def send_kafka_message(broker_message):

  producer = create_kafka_producer()
  try:
    future = producer.send(TOPIC_NAME, broker_message)
    record_metadata = future.get(timeout=10)
    #print (record_metadata.topic)
    return None
  except Exception:
    #Return a generic unassigned HTTP status code as per iana, for all exceptions (419:Callout failed)
    #https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
    return 419

# Helper: Creates a Kafka producer for JSON messages
def create_kafka_producer():

  PRODUCER_URL=MSG_BROKER_URL + ":" + MSG_BROKER_PORT
  producer = KafkaProducer(
    bootstrap_servers=[PRODUCER_URL],
    value_serializer=lambda m: json.dumps(m).encode('ascii'),
  )
  return producer

# Helper: Builds a Kafka message
def create_kafka_message(policy_type_id, policy_id, payload, operation):

  kafka_message_format = {'action': operation_to_action(operation), 'payload': payload, 'policy_type_id': policy_type_id, 'policy_id': policy_id}
  kafka_message_json = json.dumps(kafka_message_format)
  return kafka_message_json

# Helper: Converts a HTTP operation to an explanation
def operation_to_action(argument):

    switcher = {
        'PUT': "CreatePolicy",
        'DELETE': "DeletePolicy",
    }
    return switcher.get(argument, None)

# Helper: Create a response object if forced http response code is set
def get_forced_response():
  if (forced_settings['code'] is not None):
    resp_code=forced_settings['code']
    pjson=create_error_response(int(resp_code))
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
    if code == 400:
      return(create_problem_json(None, "Bad request", 400, "Object in payload not properly formulated or not related to the method", None))
    elif code == 404:
      return(create_problem_json(None, "Not found", 404, "No resource found at the URI", None))
    elif code == 405:
      return(create_problem_json(None, "Method not allowed", 405, "Method not allowed for the URI", None))
    elif code == 409:
      return(create_problem_json(None, "Conflict", 409, "Request could not be processed in the current state of the resource", None))
    elif code == 429:
      return(create_problem_json(None, "Too many requests", 429, "Too many requests have been sent in a given amount of time", None))
    elif code == 507:
      return(create_problem_json(None, "Insufficient storage", 507, "The method could not be performed on the resource because the provider is unable to store the representation needed to successfully complete the request", None))
    elif code == 503:
      return(create_problem_json(None, "Service unavailable", 503, "The provider is currently unable to handle the request due to a temporary overload", None))
    else:
      return(create_problem_json(None, "Unknown", code, "Not implemented response code", None))
