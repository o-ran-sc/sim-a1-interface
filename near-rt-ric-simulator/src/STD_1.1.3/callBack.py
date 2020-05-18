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

import connexion
import json
import sys
import os
import requests


from pathlib import Path
from flask import Flask, escape, request, Response
from jsonschema import validate
from maincommon import *


check_apipath()

app = connexion.App(__name__, specification_dir=apipath)

#Check alive function
@app.route('/', methods=['GET'])
def test():

  return Response("OK", 200, mimetype='text/plain')

#Receive status (only for testing callbacks)
#/statustest
@app.route('/statustest', methods=['POST', 'PUT'])
def statustest():
  try:
    data = request.data
    data = json.loads(data)
  except:
    return Response("The status data is corrupt or missing.", 400, mimetype='text/plain')

  return Response(json.dumps(data), 200, mimetype='application/json')

port_number = 2223

app.run(port=port_number, host="127.0.0.1", threaded=False)