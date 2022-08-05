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

# This is a script for test-purposes only
# It consumes a response-event from a kafka bus with different apporaches
# In order to use this script, you must have an venv for Python and kafka-python libs has to be installed
# To instal kafka-python please use: pip install kafka-python
# Example of an response-event json
#{
  #"response-code": "400",
  #"error-info": "Bad format"
#}


import os
import json
import sys
import math
import time

from kafka import KafkaConsumer, TopicPartition
from threading import RLock

# Response string with JSON format
response_data_JSON =  """
{
  "response-code": 200,
  "error-info": ""
}
"""

# in seconds
TIME_OUT=30
target_topic_res='kafkatopicres'
MSG_BROKER_URL='localhost:9092'

# Instantiate KafkaConsumer with keyword arguments
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html
def create_kafka_consumer():
  consumer = KafkaConsumer(
    # kafka cluster endpoint
    bootstrap_servers = MSG_BROKER_URL,
    # move to the earliest or latest available message
    auto_offset_reset = 'earliest',
    # number of milliseconds to block during message iteration
    # if no new message available during this period of time, iteration through a for-loop will stop automatically
    consumer_timeout_ms = 100,
    value_deserializer = lambda m: json.loads(m.decode('ascii')),
    #enable_auto_commit=False
  )
  return consumer

# Helper: Searches for req_id by seeking every five seconds up to thirty seconds
# Helper: If the req_id is found, then ConsumerRecord will be returned
# Helper: If the req_id is not found, then Response Request Timeout will be returned
def consume(req_id):

  try:
    print ('req_id looking for in consumer:', req_id)
    consumer = create_kafka_consumer()
    # Latch to target topic and partition
    topic_partition = TopicPartition(target_topic_res, 0)
    consumer.assign([topic_partition])

    sleep_period_in_sec = 5
    poll_cycle_threshold = calc_pollcycle_threshold(sleep_period_in_sec)
    poll_retries = 0

    while (poll_retries < poll_cycle_threshold):
      for consumer_record in consumer:
        # Get req_id as msg_key and converts it from byte to str for each consumer record
        msg_key = byte_to_str(consumer_record.key)
        print ('msg_key in a consumer_record:', msg_key)
        if (req_id == msg_key):
          print ('req_id is found in consumer records', req_id)
          return consumer_record

      print('Sleeping for ' + str(sleep_period_in_sec) + ' seconds...')
      time.sleep(sleep_period_in_sec)
      poll_retries += 1

    return 1
  except Exception as err:
    print('Error while consume record for req_id', err)
    return 1
  finally:
    consumer.close()

# Helper: calculates poll cycle threshold
def calc_pollcycle_threshold(sleep_period_in_sec):

    poll_cycle_threshold = int(TIME_OUT) / sleep_period_in_sec
    poll_cycle_threshold = math.floor(poll_cycle_threshold)
    return poll_cycle_threshold

# Helper: Converts a byte array to a str
def byte_to_str(byte_arr):

  if (byte_arr is not None):
    return byte_arr.decode('utf-8')
  else:
    return None

if __name__ == '__main__':
    try:
      requestid = sys.argv[1]
      future = consume(requestid)
    except Exception as err:
      print('Error in __main__', err)
      print (1)
    sys.exit()
