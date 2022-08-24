#!/bin/bash

#  ============LICENSE_START===============================================
#  Copyright (C) 2020-2022 Nordix Foundation. All rights reserved.
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

# Function to execute curl and compare + print result

# Note: Env var PORT must be set to the intended port number
# Notre Env var HTTPX must be set to either 'http' or 'https'

#args: <http-operation> <url> <response-code> [file]
#Expects the env $RESULT to contain the expected RESULT.
#If json, the RESULT shall begin with 'json:'.
#Any json parameter with unknown value shall be given as "????" to skip checking the value.
#The requestid parameter is being introduced in the fifth order.
do_curl() {
    if [ $# -lt 3 ]; then
        echo "Need 3 or more parameters, <http-operation> <url> <response-code> [file]: "$@
        echo "Exiting test script....."
        exit 1
    fi
    curlstr="curl -X "$1" -skw %{http_code} $HTTPX://localhost:"${PORT}${2}" -H accept:*/*"
    if [ $# -eq 4 ]; then
        curlstr=$curlstr" -H Content-Type:application/json --data-binary @"$4
    fi
    if [ $# -ge 5 ]; then
        curlstr=$curlstr" -H Content-Type:application/json --data-binary @"$4" -H requestid:"$5
    fi
    echo "  CMD (${BASH_LINENO[0]}):"$curlstr
    res=$($curlstr)
    status=${res:${#res}-3}
    body=${res:0:${#res}-3}
    if [ $status -ne $3 ]; then
        echo "  Error status :"$status" Expected status: "$3
        echo "  Body         :"$body
        echo "Exiting test script....."
        exit 1
    else
        echo "  OK, code           :"$status"     (Expected)"
        echo "  Body               :"$body
        if [ "$RESULT" == "*" ]; then
            echo "  Body contents not checked"
        elif [[ "$RESULT" == "json:"* ]]; then
            result=${RESULT:5:${#RESULT}} #Remove 'json:' from the result string
            res=$(python ../common/compare_json.py "$result" "$body")
            if [ $res -eq 0 ]; then
                echo "  Expected json body :"$result
                echo "  Body as expected"
            else
                echo "  Expected json body :"$result
                echo "Exiting....."
                exit 1
            fi
        else
            body="$(echo $body | tr -d '\n' )"
            if [ "$RESULT" == "$body" ]; then
                echo "  Expected body      :"$RESULT
                echo "  Body as expected"
            else
                echo "  Expected body      :"$RESULT
                echo "Exiting....."
                exit 1
            fi
        fi
    fi
}

# Triggers publish_event_to_kafka_bus.py script to send msg to Kafka broker
# The aim of this function is to realize error related test cases only
# The request_id for the Kafka msg, should be passed here as a function parameter
publish_response_event() {
    if [ $# -ne 2 ]; then
        echo "Need 2 parameter, <request_id> <target_topic>"
        echo "Exiting test script....."
        exit 1
    fi
    res=$(python ../common/publish_response_event_to_kafka_bus.py "$1" "$2")
    if [ $res -eq 0 ]; then
        echo "  Result as expected  "
    else
        echo "  Result not expected  "
        echo "  Exiting.....  "
        exit 1
    fi
}

# Creates 16 digits random number using letters and numbers only
get_random_number() {
    r_num=$(tr -dc A-Za-z0-9 < /dev/urandom | head -c 16)
    echo $r_num
}

# It is being used to cross-test-cases in between A1 sim and external server
# The parameter it holds all with regards to External Server relates e.g. HTTPX_EXT_SRV and PORT_EXT_SRV
do_curl_ext_srv() {
    if [ $# -lt 3 ]; then
        echo "Need 3 or more parameters, <http-operation> <url> <response-code> [file]: "$@
        echo "Exiting test script....."
        exit 1
    fi
    curlstr="curl -X "$1" -skw %{http_code} $HTTPX_EXT_SRV://localhost:"${PORT_EXT_SRV}${2}" -H accept:*/*"
    if [ $# -gt 3 ]; then
        curlstr=$curlstr" -H Content-Type:application/json --data-binary @"$4
    fi
    echo "  CMD (${BASH_LINENO[0]}):"$curlstr
    res=$($curlstr)
    status=${res:${#res}-3}
    body=${res:0:${#res}-3}
    if [ $status -ne $3 ]; then
        echo "  Error status :"$status" Expected status: "$3
        echo "  Body         :"$body
        echo "Exiting test script....."
        exit 1
    else
        echo "  OK, code           :"$status"     (Expected)"
        echo "  Body               :"$body
        if [ "$RESULT" == "*" ]; then
            echo "  Body contents not checked"
        elif [[ "$RESULT" == "json:"* ]]; then
            result=${RESULT:5:${#RESULT}} #Remove 'json:' from the result string
            res=$(python ../common/compare_json.py "$result" "$body")
            if [ $res -eq 0 ]; then
                echo "  Expected json body :"$result
                echo "  Body as expected"
            else
                echo "  Expected json body :"$result
                echo "Exiting....."
                exit 1
            fi
        else
            body="$(echo $body | tr -d '\n' )"
            if [ "$RESULT" == "$body" ]; then
                echo "  Expected body      :"$RESULT
                echo "  Body as expected"
            else
                echo "  Expected body      :"$RESULT
                echo "Exiting....."
                exit 1
            fi
        fi
    fi
}
