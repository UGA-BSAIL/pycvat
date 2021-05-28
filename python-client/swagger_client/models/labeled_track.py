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


class LabeledTrack(object):
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
        "id": "int",
        "frame": "int",
        "label_id": "int",
        "group": "int",
        "source": "str",
        "shapes": "list[TrackedShape]",
        "attributes": "list[AttributeVal]",
    }

    attribute_map = {
        "id": "id",
        "frame": "frame",
        "label_id": "label_id",
        "group": "group",
        "source": "source",
        "shapes": "shapes",
        "attributes": "attributes",
    }

    def __init__(
        self,
        id=None,
        frame=None,
        label_id=None,
        group=None,
        source="manual",
        shapes=None,
        attributes=None,
        _configuration=None,
    ):  # noqa: E501
        """LabeledTrack - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._frame = None
        self._label_id = None
        self._group = None
        self._source = None
        self._shapes = None
        self._attributes = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.frame = frame
        self.label_id = label_id
        self.group = group
        if source is not None:
            self.source = source
        self.shapes = shapes
        self.attributes = attributes

    @property
    def id(self):
        """Gets the id of this LabeledTrack.  # noqa: E501


        :return: The id of this LabeledTrack.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this LabeledTrack.


        :param id: The id of this LabeledTrack.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def frame(self):
        """Gets the frame of this LabeledTrack.  # noqa: E501


        :return: The frame of this LabeledTrack.  # noqa: E501
        :rtype: int
        """
        return self._frame

    @frame.setter
    def frame(self, frame):
        """Sets the frame of this LabeledTrack.


        :param frame: The frame of this LabeledTrack.  # noqa: E501
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
    def label_id(self):
        """Gets the label_id of this LabeledTrack.  # noqa: E501


        :return: The label_id of this LabeledTrack.  # noqa: E501
        :rtype: int
        """
        return self._label_id

    @label_id.setter
    def label_id(self, label_id):
        """Sets the label_id of this LabeledTrack.


        :param label_id: The label_id of this LabeledTrack.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and label_id is None:
            raise ValueError(
                "Invalid value for `label_id`, must not be `None`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and label_id is not None
            and label_id < 0
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `label_id`, must be a value greater than or equal to `0`"
            )  # noqa: E501

        self._label_id = label_id

    @property
    def group(self):
        """Gets the group of this LabeledTrack.  # noqa: E501


        :return: The group of this LabeledTrack.  # noqa: E501
        :rtype: int
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this LabeledTrack.


        :param group: The group of this LabeledTrack.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and group is None:
            raise ValueError(
                "Invalid value for `group`, must not be `None`"
            )  # noqa: E501
        if (
            self._configuration.client_side_validation
            and group is not None
            and group < 0
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `group`, must be a value greater than or equal to `0`"
            )  # noqa: E501

        self._group = group

    @property
    def source(self):
        """Gets the source of this LabeledTrack.  # noqa: E501


        :return: The source of this LabeledTrack.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this LabeledTrack.


        :param source: The source of this LabeledTrack.  # noqa: E501
        :type: str
        """
        if (
            self._configuration.client_side_validation
            and source is not None
            and len(source) < 1
        ):
            raise ValueError(
                "Invalid value for `source`, length must be greater than or equal to `1`"
            )  # noqa: E501

        self._source = source

    @property
    def shapes(self):
        """Gets the shapes of this LabeledTrack.  # noqa: E501


        :return: The shapes of this LabeledTrack.  # noqa: E501
        :rtype: list[TrackedShape]
        """
        return self._shapes

    @shapes.setter
    def shapes(self, shapes):
        """Sets the shapes of this LabeledTrack.


        :param shapes: The shapes of this LabeledTrack.  # noqa: E501
        :type: list[TrackedShape]
        """
        if self._configuration.client_side_validation and shapes is None:
            raise ValueError(
                "Invalid value for `shapes`, must not be `None`"
            )  # noqa: E501

        self._shapes = shapes

    @property
    def attributes(self):
        """Gets the attributes of this LabeledTrack.  # noqa: E501


        :return: The attributes of this LabeledTrack.  # noqa: E501
        :rtype: list[AttributeVal]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this LabeledTrack.


        :param attributes: The attributes of this LabeledTrack.  # noqa: E501
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
        if issubclass(LabeledTrack, dict):
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
        if not isinstance(other, LabeledTrack):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LabeledTrack):
            return True

        return self.to_dict() != other.to_dict()
