#  ============LICENSE_START===============================================
#  Copyright (C) 2023 Nordix Foundation. All rights reserved.
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

# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401


class EnforceStatus():

    def __init__(self, enforce_status: str=None, enforce_reason: str=None):  # noqa: E501
        """EnforceStatus

        :param enforce_status: The enforce_status of this EnforceStatus.  # noqa: E501
        :type enforce_status: str
        :param enforce_reason: The enforce_reason of this EnforceStatus.  # noqa: E501
        :type enforce_reason: str
        """
        self._enforce_status = enforce_status
        self._enforce_reason = enforce_reason

    @property
    def enforce_status(self) -> str:
        """Gets the enforce_status of this EnforceStatus.

        :return: The enforce_status of this EnforceStatus.
        :rtype: str
        """
        return self._enforce_status

    @enforce_status.setter
    def enforce_status(self, enforce_status: str):
        """Sets the enforce_status of this EnforceStatus.

        :param enforce_status: The enforce_status of this EnforceStatus.
        :type enforce_status: str
        """
        allowed_values = ["ENFORCED", "NOT_ENFORCED"]  # noqa: E501
        if enforce_status not in allowed_values:
            raise ValueError(
                "Invalid value for `enforce_status` ({0}), must be one of {1}"
                .format(enforce_status, allowed_values)
            )

        self._enforce_status = enforce_status

    @property
    def enforce_reason(self) -> str:
        """Gets the enforce_reason of this EnforceStatus.

        :return: The enforce_reason of this EnforceStatus.
        :rtype: str
        """
        return self._enforce_reason

    @enforce_reason.setter
    def enforce_reason(self, enforce_reason: str):
        """Sets the enforce_reason of this EnforceStatus.

        :param enforce_reason: The enforce_reason of this EnforceStatus.
        :type enforce_reason: str
        """
        allowed_values = ["SCOPE_NOT_APPLICABLE", "STATEMENT_NOT_APPLICABLE", "OTHER_REASON"]  # noqa: E501
        if enforce_reason not in allowed_values:
            raise ValueError(
                "Invalid value for `enforce_reason` ({0}), must be one of {1}"
                .format(enforce_reason, allowed_values)
            )

        self._enforce_reason = enforce_reason

    def to_dict(self):
        """Returns the model properties as a dict

        :rtype: dict
        """
        result = {
            'enforceStatus': self._enforce_status, 
            'enforceReason': self._enforce_reason
        }
        return result
