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


class BasicUser(object):
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
        "url": "str",
        "id": "int",
        "username": "str",
        "first_name": "str",
        "last_name": "str",
    }

    attribute_map = {
        "url": "url",
        "id": "id",
        "username": "username",
        "first_name": "first_name",
        "last_name": "last_name",
    }

    def __init__(
        self,
        url=None,
        id=None,
        username=None,
        first_name=None,
        last_name=None,
        _configuration=None,
    ):  # noqa: E501
        """BasicUser - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._url = None
        self._id = None
        self._username = None
        self._first_name = None
        self._last_name = None
        self.discriminator = None

        if url is not None:
            self.url = url
        if id is not None:
            self.id = id
        self.username = username
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name

    @property
    def url(self):
        """Gets the url of this BasicUser.  # noqa: E501


        :return: The url of this BasicUser.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this BasicUser.


        :param url: The url of this BasicUser.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def id(self):
        """Gets the id of this BasicUser.  # noqa: E501


        :return: The id of this BasicUser.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BasicUser.


        :param id: The id of this BasicUser.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def username(self):
        """Gets the username of this BasicUser.  # noqa: E501

        Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.  # noqa: E501

        :return: The username of this BasicUser.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this BasicUser.

        Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.  # noqa: E501

        :param username: The username of this BasicUser.  # noqa: E501
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
        if (
            self._configuration.client_side_validation
            and username is not None
            and not re.search(r"^[\\w.@+-]+$", username)
        ):  # noqa: E501
            raise ValueError(
                r"Invalid value for `username`, must be a follow pattern or equal to `/^[\\w.@+-]+$/`"
            )  # noqa: E501

        self._username = username

    @property
    def first_name(self):
        """Gets the first_name of this BasicUser.  # noqa: E501


        :return: The first_name of this BasicUser.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this BasicUser.


        :param first_name: The first_name of this BasicUser.  # noqa: E501
        :type: str
        """
        if (
            self._configuration.client_side_validation
            and first_name is not None
            and len(first_name) > 150
        ):
            raise ValueError(
                "Invalid value for `first_name`, length must be less than or equal to `150`"
            )  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this BasicUser.  # noqa: E501


        :return: The last_name of this BasicUser.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this BasicUser.


        :param last_name: The last_name of this BasicUser.  # noqa: E501
        :type: str
        """
        if (
            self._configuration.client_side_validation
            and last_name is not None
            and len(last_name) > 150
        ):
            raise ValueError(
                "Invalid value for `last_name`, length must be less than or equal to `150`"
            )  # noqa: E501

        self._last_name = last_name

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
        if issubclass(BasicUser, dict):
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
        if not isinstance(other, BasicUser):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BasicUser):
            return True

        return self.to_dict() != other.to_dict()
