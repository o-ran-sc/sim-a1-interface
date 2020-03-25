
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

# Deep compare of two json obects
# If a parameter value in the target json is set to '????' then the result json value is not checked for that parameter
# Any included json array will be sorted before comparison

import sys
import json

def compare_json(jsonTarget,jsonResult):


    if isinstance(jsonTarget, dict):
        if (len(jsonTarget) != len(jsonResult)):
            return 1
        for key in jsonTarget.keys():
            if (jsonResult.get(key) is None):
                return 1
            res=compare_json(jsonTarget.get(key), jsonResult.get(key))
            if (res != 0):
                return 1
    elif isinstance(jsonTarget, list):
        if (len(jsonTarget) != len(jsonResult)):
            return 1
        jsonTarget.sort()
        jsonResult.sort()
        for i in range(len(jsonTarget)):
            res=compare_json(jsonTarget[i], jsonResult[i])
            if (res != 0):
                return 1
    else:
        if (jsonTarget != "????") and (jsonTarget != jsonResult):
            return 1
    return 0


try:
    jsonTarget = json.loads(sys.argv[1])
    jsonResult = json.loads(sys.argv[2])

    print(compare_json(jsonTarget,jsonResult))

except Exception as e:
    print (1)
sys.exit()





