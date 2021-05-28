# coding: utf-8

"""
    CVAT REST API

    REST API for Computer Vision Annotation Tool (CVAT)  # noqa: E501

    OpenAPI spec version: v1
    Contact: nikita.manovich@intel.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six
from swagger_client.configuration import Configuration


class RestrictedRegister(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "username": "str",
        "email": "str",
        "password1": "str",
        "password2": "str",
        "first_name": "str",
        "last_name": "str",
        "confirmations": "list[UserAgreement]",
    }

    attribute_map = {
        "username": "username",
        "email": "email",
        "password1": "password1",
        "password2": "password2",
        "first_name": "first_name",
        "last_name": "last_name",
        "confirmations": "confirmations",
    }

    def __init__(
        self,
        username=None,
        email=None,
        password1=None,
        password2=None,
        first_name=None,
        last_name=None,
        confirmations=None,
        _configuration=None,
    ):  # noqa: E501
        """RestrictedRegister - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._username = None
        self._email = None
        self._password1 = None
        self._password2 = None
        self._first_name = None
        self._last_name = None
        self._confirmations = None
        self.discriminator = None

        self.username = username
        if email is not None:
            self.email = email
        self.password1 = password1
        self.password2 = password2
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if confirmations is not None:
            self.confirmations = confirmations

    @property
    def username(self):
        """Gets the username of this RestrictedRegister.  # noqa: E501


        :return: The username of this RestrictedRegister.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this RestrictedRegister.


        :param username: The username of this RestrictedRegister.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and username is None:
            raise ValueError(
                "Invalid value for `username`, must not be `None`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and username is not None
            and len(username) > 150
        ):
            raise ValueError(
                "Invalid value for `username`, length must be less than or equal to `150`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and username is not None
            and len(username) < 1
        ):
            raise ValueError(
                "Invalid value for `username`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._username = username

    @property
    def email(self):
        """Gets the email of this RestrictedRegister.  # noqa: E501


        :return: The email of this RestrictedRegister.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this RestrictedRegister.


        :param email: The email of this RestrictedRegister.  # noqa: E501
        :type: str
        """
        if (
            self._configuration.client_side_validation
            and email is not None
            and len(email) < 1
        ):
            raise ValueError(
                "Invalid value for `email`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._email = email

    @property
    def password1(self):
        """Gets the password1 of this RestrictedRegister.  # noqa: E501


        :return: The password1 of this RestrictedRegister.  # noqa: E501
        :rtype: str
        """
        return self._password1

    @password1.setter
    def password1(self, password1):
        """Sets the password1 of this RestrictedRegister.


        :param password1: The password1 of this RestrictedRegister.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and password1 is None:
            raise ValueError(
                "Invalid value for `password1`, must not be `None`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and password1 is not None
            and len(password1) < 1
        ):
            raise ValueError(
                "Invalid value for `password1`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._password1 = password1

    @property
    def password2(self):
        """Gets the password2 of this RestrictedRegister.  # noqa: E501


        :return: The password2 of this RestrictedRegister.  # noqa: E501
        :rtype: str
        """
        return self._password2

    @password2.setter
    def password2(self, password2):
        """Sets the password2 of this RestrictedRegister.


        :param password2: The password2 of this RestrictedRegister.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and password2 is None:
            raise ValueError(
                "Invalid value for `password2`, must not be `None`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and password2 is not None
            and len(password2) < 1
        ):
            raise ValueError(
                "Invalid value for `password2`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._password2 = password2

    @property
    def first_name(self):
        """Gets the first_name of this RestrictedRegister.  # noqa: E501


        :return: The first_name of this RestrictedRegister.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this RestrictedRegister.


        :param first_name: The first_name of this RestrictedRegister.  # noqa: E501
        :type: str
        """
        if (
            self._configuration.client_side_validation
            and first_name is not None
            and len(first_name) < 1
        ):
            raise ValueError(
                "Invalid value for `first_name`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this RestrictedRegister.  # noqa: E501


        :return: The last_name of this RestrictedRegister.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this RestrictedRegister.


        :param last_name: The last_name of this RestrictedRegister.  # noqa: E501
        :type: str
        """
        if (
            self._configuration.client_side_validation
            and last_name is not None
            and len(last_name) < 1
        ):
            raise ValueError(
                "Invalid value for `last_name`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._last_name = last_name

    @property
    def confirmations(self):
        """Gets the confirmations of this RestrictedRegister.  # noqa: E501


        :return: The confirmations of this RestrictedRegister.  # noqa: E501
        :rtype: list[UserAgreement]
        """
        return self._confirmations

    @confirmations.setter
    def confirmations(self, confirmations):
        """Sets the confirmations of this RestrictedRegister.


        :param confirmations: The confirmations of this RestrictedRegister.  # noqa: E501
        :type: list[UserAgreement]
        """

        self._confirmations = confirmations

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(
                        lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                        value,
                    )
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(RestrictedRegister, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RestrictedRegister):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RestrictedRegister):
            return True

        return self.to_dict() != other.to_dict()
