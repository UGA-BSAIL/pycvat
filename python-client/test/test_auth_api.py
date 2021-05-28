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
from swagger_client.api.auth_api import AuthApi  # noqa: E501
from swagger_client.rest import ApiException


class TestAuthApi(unittest.TestCase):
    """AuthApi unit test stubs"""

    def setUp(self):
        self.api = swagger_client.api.auth_api.AuthApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_auth_login_create(self):
        """Test case for auth_login_create

        """
        pass

    def test_auth_logout_create(self):
        """Test case for auth_logout_create

        Calls Django logout method and delete the Token object assigned to the current User object.  # noqa: E501
        """
        pass

    def test_auth_logout_list(self):
        """Test case for auth_logout_list

        Calls Django logout method and delete the Token object assigned to the current User object.  # noqa: E501
        """
        pass

    def test_auth_password_change_create(self):
        """Test case for auth_password_change_create

        Calls Django Auth SetPasswordForm save method.  # noqa: E501
        """
        pass

    def test_auth_password_reset_confirm_create(self):
        """Test case for auth_password_reset_confirm_create

        Password reset e-mail link is confirmed, therefore this resets the user's password.  # noqa: E501
        """
        pass

    def test_auth_password_reset_create(self):
        """Test case for auth_password_reset_create

        Calls Django Auth PasswordResetForm save method.  # noqa: E501
        """
        pass

    def test_auth_register_create(self):
        """Test case for auth_register_create

        """
        pass

    def test_auth_signing_create(self):
        """Test case for auth_signing_create

        This method signs URL for access to the server.  # noqa: E501
        """
        pass


if __name__ == "__main__":
    unittest.main()
