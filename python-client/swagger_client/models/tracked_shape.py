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


class TrackedShape(object):
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
        "type": "str",
        "occluded": "bool",
        "z_order": "int",
        "points": "list[float]",
        "id": "int",
        "frame": "int",
        "outside": "bool",
        "attributes": "list[AttributeVal]",
    }

    attribute_map = {
        "type": "type",
        "occluded": "occluded",
        "z_order": "z_order",
        "points": "points",
        "id": "id",
        "frame": "frame",
        "outside": "outside",
        "attributes": "attributes",
    }

    def __init__(
        self,
        type=None,
        occluded=None,
        z_order=None,
        points=None,
        id=None,
        frame=None,
        outside=None,
        attributes=None,
        _configuration=None,
    ):  # noqa: E501
        """TrackedShape - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._type = None
        self._occluded = None
        self._z_order = None
        self._points = None
        self._id = None
        self._frame = None
        self._outside = None
        self._attributes = None
        self.discriminator = None

        self.type = type
        self.occluded = occluded
        if z_order is not None:
            self.z_order = z_order
        self.points = points
        if id is not None:
            self.id = id
        self.frame = frame
        self.outside = outside
        self.attributes = attributes

    @property
    def type(self):
        """Gets the type of this TrackedShape.  # noqa: E501


        :return: The type of this TrackedShape.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this TrackedShape.


        :param type: The type of this TrackedShape.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and type is None:
            raise ValueError(
                "Invalid value for `type`, must not be `None`"
            )  # noqa: E501
        allowed_values = [
            "rectangle",
            "polygon",
            "polyline",
            "points",
            "cuboid",
        ]  # noqa: E501
        if (
            self._configuration.client_side_validation
            and type not in allowed_values
        ):
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}".format(  # noqa: E501
                    type, allowed_values
                )
            )

        self._type = type

    @property
    def occluded(self):
        """Gets the occluded of this TrackedShape.  # noqa: E501


        :return: The occluded of this TrackedShape.  # noqa: E501
        :rtype: bool
        """
        return self._occluded

    @occluded.setter
    def occluded(self, occluded):
        """Sets the occluded of this TrackedShape.


        :param occluded: The occluded of this TrackedShape.  # noqa: E501
        :type: bool
        """
        if self._configuration.client_side_validation and occluded is None:
            raise ValueError(
                "Invalid value for `occluded`, must not be `None`"
            )  # noqa: E501

        self._occluded = occluded

    @property
    def z_order(self):
        """Gets the z_order of this TrackedShape.  # noqa: E501


        :return: The z_order of this TrackedShape.  # noqa: E501
        :rtype: int
        """
        return self._z_order

    @z_order.setter
    def z_order(self, z_order):
        """Sets the z_order of this TrackedShape.


        :param z_order: The z_order of this TrackedShape.  # noqa: E501
        :type: int
        """

        self._z_order = z_order

    @property
    def points(self):
        """Gets the points of this TrackedShape.  # noqa: E501


        :return: The points of this TrackedShape.  # noqa: E501
        :rtype: list[float]
        """
        return self._points

    @points.setter
    def points(self, points):
        """Sets the points of this TrackedShape.


        :param points: The points of this TrackedShape.  # noqa: E501
        :type: list[float]
        """
        if self._configuration.client_side_validation and points is None:
            raise ValueError(
                "Invalid value for `points`, must not be `None`"
            )  # noqa: E501

        self._points = points

    @property
    def id(self):
        """Gets the id of this TrackedShape.  # noqa: E501


        :return: The id of this TrackedShape.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TrackedShape.


        :param id: The id of this TrackedShape.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def frame(self):
        """Gets the frame of this TrackedShape.  # noqa: E501


        :return: The frame of this TrackedShape.  # noqa: E501
        :rtype: int
        """
        return self._frame

    @frame.setter
    def frame(self, frame):
        """Sets the frame of this TrackedShape.


        :param frame: The frame of this TrackedShape.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and frame is None:
            raise ValueError(
                "Invalid value for `frame`, must not be `None`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and frame is not None
            and frame < 0
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `frame`, must be a value greater than or equal to `0`"
            )  # noqa: E501

        self._frame = frame

    @property
    def outside(self):
        """Gets the outside of this TrackedShape.  # noqa: E501


        :return: The outside of this TrackedShape.  # noqa: E501
        :rtype: bool
        """
        return self._outside

    @outside.setter
    def outside(self, outside):
        """Sets the outside of this TrackedShape.


        :param outside: The outside of this TrackedShape.  # noqa: E501
        :type: bool
        """
        if self._configuration.client_side_validation and outside is None:
            raise ValueError(
                "Invalid value for `outside`, must not be `None`"
            )  # noqa: E501

        self._outside = outside

    @property
    def attributes(self):
        """Gets the attributes of this TrackedShape.  # noqa: E501


        :return: The attributes of this TrackedShape.  # noqa: E501
        :rtype: list[AttributeVal]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this TrackedShape.


        :param attributes: The attributes of this TrackedShape.  # noqa: E501
        :type: list[AttributeVal]
        """
        if self._configuration.client_side_validation and attributes is None:
            raise ValueError(
                "Invalid value for `attributes`, must not be `None`"
            )  # noqa: E501

        self._attributes = attributes

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
        if issubclass(TrackedShape, dict):
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
        if not isinstance(other, TrackedShape):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TrackedShape):
            return True

        return self.to_dict() != other.to_dict()
