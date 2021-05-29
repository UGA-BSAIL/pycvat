# coding: utf-8

"""
    CVAT REST API

    REST API for Computer Vision Annotation Tool (CVAT)  # noqa: E501

    OpenAPI spec version: v1
    Contact: nikita.manovich@intel.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.issues_api import IssuesApi  # noqa: E501
from swagger_client.rest import ApiException


class TestIssuesApi(unittest.TestCase):
    """IssuesApi unit test stubs"""

    def setUp(self):
        self.api = IssuesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_issues_comments(self):
        """Test case for issues_comments

        The action returns all comments of a specific issue  # noqa: E501
        """
        pass

    def test_issues_delete(self):
        """Test case for issues_delete

        Method removes an issue from a job  # noqa: E501
        """
        pass

    def test_issues_partial_update(self):
        """Test case for issues_partial_update

        Method updates an issue. It is used to resolve/reopen an issue  # noqa: E501
        """
        pass


if __name__ == "__main__":
    unittest.main()
