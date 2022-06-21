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

from flask import request, Response
from datetime import datetime
from kafka.consumer.fetcher import ConsumerRecord
from kafka import TopicPartition
from var_declaration import forced_settings
from maincommon import create_kafka_producer, create_kafka_consumer, create_kafka_event, create_kafka_response_event, byte_to_str, get_random_string


MSG_BROKER_URL=os.getenv('MSG_BROKER_URL')

TIME_OUT=os.getenv('TIME_OUT')

#Constsants
APPL_JSON='application/json'
TEXT_PLAIN='text/plain'
APPL_PROB_JSON='application/problem+json'

# API Function: Dispatch create or update events to Kafka cluster
def put_policy(policyTypeId, policyId):

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id = str(policyTypeId)
  policy_id = str(policyId)

  try:
    # Error based unit test rel only, for more info please check basic_test_with_cust_header
    req_id_from_header = request.headers.get('requestid')
    # Differentiate if the PUT is update or create operation since the endpoint is the same
    update_oper_from_header = request.headers.get('updateoper')
    data = request.data
    data = json.loads(data)
  except Exception:
    pjson=create_problem_json(None, "The a1policy is corrupt or missing.", 400, None, policy_id)
    return Response(json.dumps(pjson), 400, mimetype=APPL_PROB_JSON)

  # Decide if the operation is update or create
  if (update_oper_from_header is not None):
    kafka_event = create_kafka_event(policy_type_id, policy_id, data, 'UPDATE')
  else:
    kafka_event = create_kafka_event(policy_type_id, policy_id, data, 'CREATE')

  # Synch callout hooks towards kafka broker
  if (MSG_BROKER_URL is not None):
    return publish_and_consume(kafka_event, req_id_from_header, policy_type_id)

  return Response('', 200, mimetype=TEXT_PLAIN)


# API Function: Dispatch delete events to south Kafka cluster
def delete_policy(policyTypeId, policyId):

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id = str(policyTypeId)
  policy_id = str(policyId)

  req_id_from_header = request.headers.get('requestid')
  print('req_id_from_header', req_id_from_header)

  # Synch callout hooks towards kafka broker
  kafka_event = create_kafka_event(policy_type_id, policy_id, None, 'DELETE')
  if (MSG_BROKER_URL is not None):
    return publish_and_consume(kafka_event, req_id_from_header, policy_type_id)

  return Response('', 200, mimetype=TEXT_PLAIN)


# API Function: Get status for a policy
def get_policy_status(policyTypeId, policyId):

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id=str(policyTypeId)
  policy_id=str(policyId)

  req_id_from_header = request.headers.get('requestid')
  print('req_id_from_header', req_id_from_header)

  # Synch callout hooks towards kafka broker
  kafka_event = create_kafka_event(policy_type_id, policy_id, None, 'GET')
  if (MSG_BROKER_URL is not None):
    return publish_and_consume(kafka_event, req_id_from_header, policy_type_id)

  return Response('', 200, mimetype=TEXT_PLAIN)


def get_policy_type_to_topic_mapping(policyTypeId):

  if ((r := check_modified_response()) is not None):
    return r

  policy_type_id = str(policyTypeId)

  m_file = open('../resources/policytype_to_topicmap.json')
  map_in_dict = json.load(m_file)

  if policy_type_id in map_in_dict.keys():
    topic_address = map_in_dict[policy_type_id]
    return Response(json.dumps(topic_address), 200, mimetype=APPL_JSON)
  else:
    pjson=create_problem_json(None, "The policy type to topic mapping does not exist.", 404, None, policy_type_id)
    return Response(json.dumps(pjson), 404, mimetype=APPL_PROB_JSON)


# Helper: Publishes and consumes (to/from) the target broker and the topic in two-way synch
def publish_and_consume(kafka_event, req_id_from_header, pol_type_id):

  # Instantiate KafkaProducer with keyword arguments
  producer = create_kafka_producer()

  # Assigns an id to each request that is supposed to get a result
  # if a req_id already exists in req headers, it means that test generated req_id is in use for testing only
  if (req_id_from_header is None):
    req_id = get_random_string(16)
  else:
    req_id = req_id_from_header

  try:

    resp = get_policy_type_to_topic_mapping(pol_type_id)
    # if the policy type to topic mapping could not be found, then returns 404
    # else gets target topic to publish the message to
    if (resp.status_code == 404):
      return resp
    else:
      data = json.loads(resp.data)
      target_topic_req = data['request_topic']
      target_topic_res = data['response_topic']

    # synch-publish
    # KafkaProducer.send(topicname, value=broker_message, key=req_id, headers=None, partition=None, timestamp_ms=None)
    fut_rec_metadata = producer.send(target_topic_req, kafka_event, req_id)
    record_metadata = fut_rec_metadata.get()
    print('Future:', record_metadata)
    publish_time_in_ms = record_metadata.timestamp

    # For test purposes only, publish the success response event with no error-info to response topic
    # if basic_test_with_cust_header.sh is being used, then comment this line
    # else comment out this line for the basic_test.sh
    kafka_response_event = create_kafka_response_event(200, "")
    producer.send(target_topic_res, kafka_response_event, req_id)

    # synch-consume
    consumer_record = consume_record_for(req_id, target_topic_res)
    if (isinstance(consumer_record, ConsumerRecord)):

      print("Consumer Record:", consumer_record)
      cons_rec_value = consumer_record.value
      cons_rec_val_in_dict = json.loads(cons_rec_value)
      resp_code = cons_rec_val_in_dict['response-code']

      # if response code success, then check for time-out
      if (int(resp_code) == 200):
        # time-out control block, default time-out duration is thirty seconds
        consume_time_in_ms = consumer_record.timestamp
        elapsed_time_in_ms = consume_time_in_ms - publish_time_in_ms
        print('Elapsed time in ms:', elapsed_time_in_ms)
        if (elapsed_time_in_ms < int(TIME_OUT)):
          return Response('', 200, mimetype=APPL_JSON)
        else:
          # returns time-out response code
          pjson=create_error_response(408)
          return Response(json.dumps(pjson), 408, mimetype=APPL_PROB_JSON)
      else:
        # for all other responses returns special error of this module by wrapping actual resp code
        pjson=create_error_response(419)
        return Response(json.dumps(pjson), 419, mimetype=APPL_PROB_JSON)

    elif (isinstance(consumer_record, Response)):
      # Returns time-out response
      return consumer_record
    else:
      # returns special error of this module
      pjson=create_error_response(419)
      return Response(json.dumps(pjson), 419, mimetype=APPL_PROB_JSON)

  except Exception as err:
    print('Error while publish and consume', err)
    pjson=create_error_response(419)
    return Response(json.dumps(pjson), 419, mimetype=APPL_PROB_JSON)
  finally:
    producer.close()


# Helper: Searches for req_id by seeking every five seconds up to thirty seconds
# Helper: If the req_id is found, then ConsumerRecord will be returned
# Helper: If the req_id is not found, then Response Request Timeout will be returned
def consume_record_for(req_id, target_topic_res):

  try:
    print ('req_id looking for in consumer:', req_id)
    consumer = create_kafka_consumer()
    topic_partition = TopicPartition(target_topic_res, 0)
    consumer.assign([topic_partition])

    poll_retries = 0
    starting_offset = 0
    prev_last_offset = 0
    while (poll_retries < 6):
      # Manually specify the fetch offset for a TopicPartition
      consumer.seek(topic_partition, starting_offset)
      # Get the last offset for the given partitions
      last_offset = consumer.end_offsets([topic_partition])[topic_partition]
      print('last_offset',last_offset)

      if (last_offset != prev_last_offset):
        for consumer_record in consumer:
          # Get req_id as msg_key and converts it from byte to str for each consumer record
          msg_key = byte_to_str(consumer_record.key)
          print ('msg_key in a consumer_record:', msg_key)
          if (req_id == msg_key):
            print ('req_id is found in consumer records', req_id)
            return consumer_record
          elif (consumer_record.offset == last_offset - 1):
            break

      print('Sleeping for five seconds...')
      time.sleep(5)

      poll_retries += 1
      prev_last_offset = last_offset
      starting_offset += last_offset

    # Returns time-out response
    pjson=create_error_response(408)
    return Response(json.dumps(pjson), 408, mimetype=APPL_PROB_JSON)

  except Exception as err:
    print('Error while consume record for req_id', err)
    pjson=create_error_response(419)
    return Response(json.dumps(pjson), 419, mimetype=APPL_PROB_JSON)
  finally:
    consumer.close()


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
    elif code == 408:
      return(create_problem_json(None, "Request timeout", 408, "Request timeout", None))
    elif code == 409:
      return(create_problem_json(None, "Conflict", 409, "Request could not be processed in the current state of the resource", None))
    elif (code == 419):
      return(create_problem_json(None, "Kafka message publish failed", 419, "Publishing the event could not be processed on the Kafka cluster", None))
    elif code == 429:
      return(create_problem_json(None, "Too many requests", 429, "Too many requests have been sent in a given amount of time", None))
    elif code == 507:
      return(create_problem_json(None, "Insufficient storage", 507, "The method could not be performed on the resource because the provider is unable to store the representation needed to successfully complete the request", None))
    elif code == 503:
      return(create_problem_json(None, "Service unavailable", 503, "The provider is currently unable to handle the request due to a temporary overload", None))
    else:
      return(create_problem_json(None, "Unknown", code, "Not implemented response code", None))
