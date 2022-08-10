#  ============LICENSE_START===============================================
#  Copyright (C) 2021 Nordix Foundation. All rights reserved.
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

#Calculate a fingerprint from sorted items of a dict, appending an optional id
def calcFingerprint(p, pid=None):
  m=''
  ext=''
  if (pid is not None):
    ext=pid
  if (p is dict):
    for i in sorted (p.keys()):
      m = m+str(i)+calcFingerprint(p[i])
  else:
    return str(p)+ext
  return m+ext