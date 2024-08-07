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

# Function to execute curl and compare + print result

# Note: Env var PORT must be set to the intended port number
# Notre Env var HTTPX must be set to either 'http' or 'https'

#args: <http-operation> <url> <response-code> [file]
#Expects the env $RESULT to contain the expected RESULT.
#If json, the RESULT shall begin with 'json:'.
#Any json parameter with unknown value shall be given as "????" to skip checking the value.
do_elapsetime_curl() {
    if [ $# -lt 4 ]; then
        echo "Need 4 or more parameters, <http-operation> <url> <response-code> <delay-time> [file]: "$@
        echo "Exiting test script....."
        exit 1
    fi

    #capture total elapsetime via ~%{time_total}
    curlstr="curl -X "$1" -skw %{http_code}~%{time_total} $HTTPX://localhost:"${PORT}${2}" -H accept:*/*"
    if [ $# -gt 4 ]; then
        curlstr=$curlstr" -H Content-Type:application/json --data-binary @"$4
    fi
    echo "  CMD (${BASH_LINENO[0]}):"$curlstr
    res=$($curlstr)

    #target delay time for a single request
    delay_time=$4

    #extract time_total and get rid of its decimals points
    left=$(echo $res | cut -d'~' -f1)
    right=$(echo $res | cut -d'~' -f2)
    elapsedtime=$(echo $right | cut -d'.' -f1)

    res=$left
    status=${res:${#res}-3}
    body=${res:0:${#res}-3}

    if [ $status -ne $3 ]; then
        echo "  Error status :"$status" Expected status: "$3
        echo "  Body         :"$body
        echo "Exiting test script....."
        exit 1
    elif [ $elapsedtime -lt $delay_time ]; then
        echo "  Elapsed time :"$elapsedtime" Expected delay time:"$delay_time "seconds"
        echo "Exiting test script....."
        exit 1
    else
        echo "  Delay OK           :"$elapsedtime"     (Expected)"
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
