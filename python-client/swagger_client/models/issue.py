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

class Issue(object):
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
        'id': 'int',
        'owner': 'BasicUser',
        'owner_id': 'int',
        'resolver': 'BasicUser',
        'resolver_id': 'int',
        'position': 'list[float]',
        'frame': 'int',
        'created_date': 'datetime',
        'resolved_date': 'datetime',
        'job': 'int',
        'review': 'int'
    }

    attribute_map = {
        'id': 'id',
        'owner': 'owner',
        'owner_id': 'owner_id',
        'resolver': 'resolver',
        'resolver_id': 'resolver_id',
        'position': 'position',
        'frame': 'frame',
        'created_date': 'created_date',
        'resolved_date': 'resolved_date',
        'job': 'job',
        'review': 'review'
    }

    def __init__(self, id=None, owner=None, owner_id=None, resolver=None, resolver_id=None, position=None, frame=None, created_date=None, resolved_date=None, job=None, review=None):  # noqa: E501
        """Issue - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._owner = None
        self._owner_id = None
        self._resolver = None
        self._resolver_id = None
        self._position = None
        self._frame = None
        self._created_date = None
        self._resolved_date = None
        self._job = None
        self._review = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if owner is not None:
            self.owner = owner
        if owner_id is not None:
            self.owner_id = owner_id
        if resolver is not None:
            self.resolver = resolver
        if resolver_id is not None:
            self.resolver_id = resolver_id
        self.position = position
        self.frame = frame
        if created_date is not None:
            self.created_date = created_date
        if resolved_date is not None:
            self.resolved_date = resolved_date
        self.job = job
        if review is not None:
            self.review = review

    @property
    def id(self):
        """Gets the id of this Issue.  # noqa: E501


        :return: The id of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Issue.


        :param id: The id of this Issue.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def owner(self):
        """Gets the owner of this Issue.  # noqa: E501


        :return: The owner of this Issue.  # noqa: E501
        :rtype: BasicUser
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this Issue.


        :param owner: The owner of this Issue.  # noqa: E501
        :type: BasicUser
        """

        self._owner = owner

    @property
    def owner_id(self):
        """Gets the owner_id of this Issue.  # noqa: E501


        :return: The owner_id of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """Sets the owner_id of this Issue.


        :param owner_id: The owner_id of this Issue.  # noqa: E501
        :type: int
        """

        self._owner_id = owner_id

    @property
    def resolver(self):
        """Gets the resolver of this Issue.  # noqa: E501


        :return: The resolver of this Issue.  # noqa: E501
        :rtype: BasicUser
        """
        return self._resolver

    @resolver.setter
    def resolver(self, resolver):
        """Sets the resolver of this Issue.


        :param resolver: The resolver of this Issue.  # noqa: E501
        :type: BasicUser
        """

        self._resolver = resolver

    @property
    def resolver_id(self):
        """Gets the resolver_id of this Issue.  # noqa: E501


        :return: The resolver_id of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._resolver_id

    @resolver_id.setter
    def resolver_id(self, resolver_id):
        """Sets the resolver_id of this Issue.


        :param resolver_id: The resolver_id of this Issue.  # noqa: E501
        :type: int
        """

        self._resolver_id = resolver_id

    @property
    def position(self):
        """Gets the position of this Issue.  # noqa: E501


        :return: The position of this Issue.  # noqa: E501
        :rtype: list[float]
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this Issue.


        :param position: The position of this Issue.  # noqa: E501
        :type: list[float]
        """
        if position is None:
            raise ValueError("Invalid value for `position`, must not be `None`")  # noqa: E501

        self._position = position

    @property
    def frame(self):
        """Gets the frame of this Issue.  # noqa: E501


        :return: The frame of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._frame

    @frame.setter
    def frame(self, frame):
        """Sets the frame of this Issue.


        :param frame: The frame of this Issue.  # noqa: E501
        :type: int
        """
        if frame is None:
            raise ValueError("Invalid value for `frame`, must not be `None`")  # noqa: E501

        self._frame = frame

    @property
    def created_date(self):
        """Gets the created_date of this Issue.  # noqa: E501


        :return: The created_date of this Issue.  # noqa: E501
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this Issue.


        :param created_date: The created_date of this Issue.  # noqa: E501
        :type: datetime
        """

        self._created_date = created_date

    @property
    def resolved_date(self):
        """Gets the resolved_date of this Issue.  # noqa: E501


        :return: The resolved_date of this Issue.  # noqa: E501
        :rtype: datetime
        """
        return self._resolved_date

    @resolved_date.setter
    def resolved_date(self, resolved_date):
        """Sets the resolved_date of this Issue.


        :param resolved_date: The resolved_date of this Issue.  # noqa: E501
        :type: datetime
        """

        self._resolved_date = resolved_date

    @property
    def job(self):
        """Gets the job of this Issue.  # noqa: E501


        :return: The job of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._job

    @job.setter
    def job(self, job):
        """Sets the job of this Issue.


        :param job: The job of this Issue.  # noqa: E501
        :type: int
        """
        if job is None:
            raise ValueError("Invalid value for `job`, must not be `None`")  # noqa: E501

        self._job = job

    @property
    def review(self):
        """Gets the review of this Issue.  # noqa: E501


        :return: The review of this Issue.  # noqa: E501
        :rtype: int
        """
        return self._review

    @review.setter
    def review(self, review):
        """Sets the review of this Issue.


        :param review: The review of this Issue.  # noqa: E501
        :type: int
        """

        self._review = review

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Issue, dict):
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
        if not isinstance(other, Issue):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
