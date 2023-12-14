#  ============LICENSE_START===============================================
#  Copyright (C) 2021 Nordix Foundation. All rights reserved.
#  Copyright (C) 2023 OpenInfra Foundation Europe. All rights reserved.
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
from maincommon import apipath

app = connexion.App(__name__, specification_dir=apipath)

policy_types={}
policy_instances = {}
policy_status = {}
callbacks = {}
forced_settings = {}
forced_settings['code']=None
forced_settings['delay']=None
policy_fingerprint={}
hosts_set=set()
data_delivery_counter=0
