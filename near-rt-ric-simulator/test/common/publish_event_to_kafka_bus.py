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

# This script publishes event to a kafka bus
# In order to use this script, you must have an venv for Python and kafka-python libs has to be installed
# To instal kafka-python please use: pip install kafka-python
# Example of an event json
#{

          #"title": "A1 policy external server",
          #"description": "A1 policies notifying external server",
          #"type": "object",
          #"properties": {
            #"a1PolicyType": "alpha test policy",
            #"url" : "http://www.com"
          #}

#}


import os
import json
import sys

from kafka import KafkaProducer

# String with JSON format
data_JSON =  """
{

          "title": "A1 policy external server",
          "description": "A1 policies notifying external server",
          "type": "object",
          "properties": {
            "a1PolicyType": "alpha test policy",
            "url" : "http://www.com"
          }

}
"""

# Instantiate KafkaProducer with keyword arguments
# https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
def create_kafka_producer():

  producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    key_serializer = str.encode,
    value_serializer = lambda m: json.dumps(m).encode('ascii'),
  )
  return producer

# Helper: Publishes (to) the target broker and the topic in synch
def publish(kafka_evet, req_id):

  # Instantiate KafkaProducer with keyword arguments
  producer = create_kafka_producer()
  # Assigns an id to each request that is supposed to get a result
  # req_id  = 'Hll1EsycKLNRric7'

  try:

    # synch-publish
    # KafkaProducer.send(topicname, value=broker_message, key=req_id, headers=None, partition=None, timestamp_ms=None)
    fut_rec_metadata = producer.send('kafkatopicres', kafka_evet, req_id)
    return fut_rec_metadata.get()

  except Exception as err:
    print('Error while publish', err)
  finally:
    producer.close()

if __name__ == '__main__':
    try:

        requestid = sys.argv[1]
        target_event_in_dict = json.loads(data_JSON)
        future = publish(target_event_in_dict, requestid)

        if (future is not None):
            print (0)
        else:
            print (1)

    except Exception:
        print (1)
    sys.exit()
