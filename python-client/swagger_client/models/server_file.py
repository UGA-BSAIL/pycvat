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


class ServerFile(object):
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
    swagger_types = {"file": "str"}

    attribute_map = {"file": "file"}

    def __init__(self, file=None, _configuration=None):  # noqa: E501
        """ServerFile - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._file = None
        self.discriminator = None

        self.file = file

    @property
    def file(self):
        """Gets the file of this ServerFile.  # noqa: E501


        :return: The file of this ServerFile.  # noqa: E501
        :rtype: str
        """
        return self._file

    @file.setter
    def file(self, file):
        """Sets the file of this ServerFile.


        :param file: The file of this ServerFile.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and file is None:
            raise ValueError(
                "Invalid value for `file`, must not be `None`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and file is not None
            and len(file) > 1024
        ):
            raise ValueError(
                "Invalid value for `file`, length must be less than or equal to `1024`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and file is not None
            and len(file) < 1
        ):
            raise ValueError(
                "Invalid value for `file`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._file = file

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
        if issubclass(ServerFile, dict):
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
        if not isinstance(other, ServerFile):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ServerFile):
            return True

        return self.to_dict() != other.to_dict()
