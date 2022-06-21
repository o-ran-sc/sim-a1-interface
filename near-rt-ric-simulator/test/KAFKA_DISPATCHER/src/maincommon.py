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
import sys
import json
from pathlib import Path
from flask import Response
import socket
import ssl
import random
import string

from kafka import KafkaProducer, KafkaConsumer

#Must exist
apipath=os.environ['APIPATH']

MSG_BROKER_URL=os.getenv('MSG_BROKER_URL')

# Make sure the api path for the interface yaml file is set, otherwise exit
def check_apipath():
    if (apipath is None):
        print("Env APIPATH not set. Exiting....")
        sys.exit(1)

# Instantiate KafkaProducer with keyword arguments
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
def create_kafka_producer():

  producer = KafkaProducer(
    bootstrap_servers = [MSG_BROKER_URL],
    key_serializer = str.encode,
    value_serializer = lambda m: json.dumps(m).encode('ascii'),
  )
  return producer


# Instantiate KafkaConsumer with keyword arguments
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
def create_kafka_consumer():
  consumer = KafkaConsumer(
    #KAFKA_TOPIC_RES,
    bootstrap_servers = MSG_BROKER_URL,
    auto_offset_reset = 'earliest',
    value_deserializer = lambda m: json.loads(m.decode('ascii')),
    #enable_auto_commit=False
  )
  return consumer


# Helper: Builds a Kafka event
def create_kafka_event(policy_type_id, policy_id, payload, operation):

  kafka_event_format = {'action': operation_to_action(operation), 'payload': payload, 'policy_type_id': policy_type_id, 'policy_id': policy_id}
  kafka_event_json = json.dumps(kafka_event_format)
  return kafka_event_json


# Helper: Converts a HTTP operation to an explanation
def operation_to_action(argument):

  switcher = {
    'PUT': "CreatePolicy",
    'DELETE': "DeletePolicy",
    'GET': "GetPolicyStatus",
  }
  return switcher.get(argument, None)


# Helper: Converts a byte array to a str
def byte_to_str(byte_arr):

  if (byte_arr is not None):
    return byte_arr.decode('utf-8')
  else:
    return None


# Helper: Creates random string
def get_random_string(length):

  characters = string.ascii_letters + string.digits + string.punctuation
  password = ''.join(random.choice(characters) for i in range(length))
  return password
