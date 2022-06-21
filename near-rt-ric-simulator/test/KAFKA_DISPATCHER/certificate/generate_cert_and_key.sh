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

# This will generate a self-signed certificate with password 'test'

SUBJECT="/C=IE/ST=WESTMEATH/L=ATHLONE/O=Ericsson/OU=EST/CN=est.tech/emailAddress=halil.cakal@est.tech"
PW=test
echo $PW > pass

openssl req -x509 -passout file:pass -newkey rsa:2048 -keyout key.crt -subj "$SUBJECT" -out cert.crt -days 9999
