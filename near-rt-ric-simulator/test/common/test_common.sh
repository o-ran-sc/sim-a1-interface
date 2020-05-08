#!/bin/bash

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

# Function to execute curl and compare + print result

# Note: Env var PORT must be set to the intended port number
# Notre Env var HTTPX must be set to either 'http' or 'https'

#args: <http-operation> <url> <response-code> [file]
#Expects the env $RESULT to contain the expected RESULT.
#If json, the RESULT shall begin with 'json:'.
#Any json parameter with unknown value shall be given as "????" to skip checking the value.
do_curl() {
     echo "(${BASH_LINENO[0]}): ${FUNCNAME[0]}" $@
    if [ $# -lt 3 ]; then
        echo "Need 3 or more parameters, <http-operation> <url> <response-code> [file]: "$@
        echo "Exiting test script....."
        exit 1
    fi
    curlstr="curl -X "$1" -skw %{http_code} $HTTPX://localhost:"${PORT}${2}" -H accept:*/*"
    if [ $# -gt 3 ]; then
        curlstr=$curlstr" -H Content-Type:application/json --data-binary @"$4
    fi
    echo "  CMD:"$curlstr
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
            echo $res
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