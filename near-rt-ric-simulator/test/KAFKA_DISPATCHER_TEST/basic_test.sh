#!/bin/bash

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

# Script for basic test of the Kafka message dispatcher.
# Run the build_and_start with the same arg, except arg 'nonsecure|secure', as this script

print_usage() {
    echo "Usage: ./basic_test.sh nonsecure|secure "
    exit 1
}

if [ $# -ne 1 ]; then
    print_usage
fi
if [ "$1" != "nonsecure" ] && [ "$1" != "secure" ]; then
    print_usage
fi

if [ $1 == "nonsecure" ]; then
    #Default http port for the simulator
    PORT=7075
    # Set http protocol
    HTTPX="http"
else
    #Default https port for the simulator
    PORT=7175
    # Set https protocol
    HTTPX="https"
fi

. ../common/test_common.sh
. ../common/elapse_time_curl.sh

echo "=== Kafka message dispatcher hello world ==="
RESULT="OK"
do_curl GET / 200

echo "=== Reset force delay ==="
RESULT="Force delay has been resetted for all dispatcher responses"
do_curl POST /dispatcheradmin/forcedelay 200

echo "=== Put an a1 policy: alpha ==="
RESULT=""
do_curl PUT  /policytypes/ANR/kafkadispatcher/alpha 200 jsonfiles/alpha_policy.json

echo "=== Put an a1 policy alpha to update ==="
RESULT=""
do_curl PUT  /policytypes/type2/kafkadispatcher/alpha 200 jsonfiles/alpha_policy.json

echo "=== Delete an a1 policy: alpha ==="
RESULT=""
do_curl DELETE  /policytypes/type2/kafkadispatcher/alpha 200

echo "=== Set force delay 5 sec ==="
RESULT="Force delay: 5 sec set for all dispatcher responses until it is resetted"
do_curl POST '/dispatcheradmin/forcedelay?delay=5' 200

echo "=== Put an a1 policy alpha to update ==="
RESULT=""
do_elapsetime_curl PUT  /policytypes/ANR/kafkadispatcher/alpha 200 jsonfiles/alpha_policy.json 5

echo "=== Reset force delay ==="
RESULT="Force delay has been resetted for all dispatcher responses"
do_curl POST /dispatcheradmin/forcedelay 200

echo "=== Put an a1 policy: beta ==="
RESULT=""
do_curl PUT  /policytypes/type2/kafkadispatcher/beta 200 jsonfiles/beta_policy.json

echo "=== Put an a1 policy: alpha ==="
RESULT=""
do_curl PUT  /policytypes/type3/kafkadispatcher/alpha 200 jsonfiles/alpha_policy.json

echo "=== Set force response code: 500 ==="
RESULT="Force response code: 500 set for all dispatcher response until it is resetted"
do_curl POST  '/dispatcheradmin/forceresponse?code=500' 200

echo "=== Put an a1 policy: alpha ==="
res=$(cat jsonfiles/forced_response.json)
RESULT="json:$res"
do_curl PUT  /policytypes/ANR/kafkadispatcher/alpha 500 jsonfiles/alpha_policy.json

echo "=== Reset force response code ==="
RESULT="Force response code has been resetted for dispatcher responses"
do_curl POST  /dispatcheradmin/forceresponse 200

echo "=== Delete an a1policy: alpha ==="
RESULT=""
do_curl DELETE  /policytypes/type2/kafkadispatcher/alpha 200

echo "********************"
echo "*** All tests ok ***"
echo "********************"
