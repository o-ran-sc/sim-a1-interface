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

# Script for error testing of the Kafka message dispatcher
# The timeout value should be equal to TIME_OUT param that exist in the start script
# Run the script with the args: nonsecure|secure timeout=30

print_usage() {
    echo "Usage: ./basic_test.sh nonsecure|secure timeout=30"
    exit 1
}

if [ $# -ne 2 ]; then
    print_usage
fi
if [ "$1" != "nonsecure" ] && [ "$1" != "secure" ]; then
    print_usage
fi

timeout=$(echo "$2" | cut -d'=' -f2)
regexp_for_number='^[0-9]+$'

if ! [[ $timeout =~ $regexp_for_number ]] ; then
   echo "error:"$timeout" Not a number"
   exit 1
else
    if [ $timeout -le 0 ]; then
        echo "Timeout value must be greater than zero"
        exit 1
    fi
fi

if [ $1 == "nonsecure" ]; then
    # Default http port for the simulator
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

echo "=== Kafka message dispatcher hello world ==="
RESULT="OK"
do_curl GET / 200

echo "=== Reset force delay ==="
RESULT="Force delay has been resetted for all dispatcher responses"
do_curl POST /dispatcheradmin/forcedelay 200

# asynch error test case
echo "=== Put policy: shall publish and consume time-out ==="
req_id=$(get_random_number)
res=$(cat jsonfiles/timeout_response.json)
RESULT="json:$res"
# asynch callout
do_curl PUT  /policytypes/ANR/kafkadispatcher/alpha 408 jsonfiles/alpha_policy.json $req_id &
proc_id=$!
sleep $timeout
# after time out duration, publish the event
publish_response_event $req_id kafkatopicres
# wait until the main process to be completed
wait $proc_id

# asynch success test case after 10s
echo "=== Put policy: shall publish and consume success at least 10 secs later ==="
req_id=$(get_random_number)
RESULT=""
# asynch callout
do_curl PUT  /policytypes/STD_1/kafkadispatcher/alpha 200 jsonfiles/alpha_policy.json $req_id &
proc_id=$!
sleep 10
# after 10s, publish the event
publish_response_event $req_id kafkatopicres2
# wait until the main process to be completed
wait $proc_id

# asynch error test case
echo "=== Get policy status: shall publish and consume time-out ==="
req_id=$(get_random_number)
res=$(cat jsonfiles/timeout_response.json)
RESULT="json:$res"
# asynch callout
do_curl GET  /policytypes/STD_2/kafkadispatcher/alpha/status 408 jsonfiles/alpha_policy.json $req_id &
proc_id=$!
sleep $timeout
# after time out duration, publish the event
publish_response_event $req_id kafkatopicres3
# wait until the main process to be completed
wait $proc_id

# asynch success test case after 10s
echo "=== Get policy status: shall publish and consume success at least 15 secs later ==="
req_id=$(get_random_number)
RESULT=""
# asynch callout
do_curl GET  /policytypes/ANR/kafkadispatcher/alpha/status 200 jsonfiles/alpha_policy.json $req_id &
proc_id=$!
sleep 15
# after 15s, publish the event
publish_response_event $req_id kafkatopicres
# wait until the main process to be completed
wait $proc_id

# asynch success test case without any delay
echo "=== Delete policy: shall publish and consume success ==="
req_id=$(get_random_number)
RESULT=""
# asynch callout
do_curl DELETE  /policytypes/STD_1/kafkadispatcher/alpha 200 jsonfiles/alpha_policy.json $req_id &
proc_id=$!
publish_response_event $req_id kafkatopicres2
# wait until the main process to be completed
wait $proc_id


echo "********************"
echo "*** All tests ok ***"
echo "********************"
