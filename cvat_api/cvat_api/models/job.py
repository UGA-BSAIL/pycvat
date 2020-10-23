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


class Job(object):
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
        "assignee": "int",
        "status": "str",
        "start_frame": "str",
        "stop_frame": "str",
        "task_id": "str",
    }

    attribute_map = {
        "url": "url",
        "id": "id",
        "assignee": "assignee",
        "status": "status",
        "start_frame": "start_frame",
        "stop_frame": "stop_frame",
        "task_id": "task_id",
    }

    def __init__(
        self,
        url=None,
        id=None,
        assignee=None,
        status=None,
        start_frame=None,
        stop_frame=None,
        task_id=None,
    ):  # noqa: E501
        """Job - a model defined in Swagger"""  # noqa: E501
        self._url = None
        self._id = None
        self._assignee = None
        self._status = None
        self._start_frame = None
        self._stop_frame = None
        self._task_id = None
        self.discriminator = None
        if url is not None:
            self.url = url
        if id is not None:
            self.id = id
        if assignee is not None:
            self.assignee = assignee
        if status is not None:
            self.status = status
        if start_frame is not None:
            self.start_frame = start_frame
        if stop_frame is not None:
            self.stop_frame = stop_frame
        if task_id is not None:
            self.task_id = task_id

    @property
    def url(self):
        """Gets the url of this Job.  # noqa: E501


        :return: The url of this Job.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this Job.


        :param url: The url of this Job.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def id(self):
        """Gets the id of this Job.  # noqa: E501


        :return: The id of this Job.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Job.


        :param id: The id of this Job.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def assignee(self):
        """Gets the assignee of this Job.  # noqa: E501


        :return: The assignee of this Job.  # noqa: E501
        :rtype: int
        """
        return self._assignee

    @assignee.setter
    def assignee(self, assignee):
        """Sets the assignee of this Job.


        :param assignee: The assignee of this Job.  # noqa: E501
        :type: int
        """

        self._assignee = assignee

    @property
    def status(self):
        """Gets the status of this Job.  # noqa: E501


        :return: The status of this Job.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Job.


        :param status: The status of this Job.  # noqa: E501
        :type: str
        """
        allowed_values = [
            "annotation",
            "validation",
            "completed",
        ]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}".format(  # noqa: E501
                    status, allowed_values
                )
            )

        self._status = status

    @property
    def start_frame(self):
        """Gets the start_frame of this Job.  # noqa: E501


        :return: The start_frame of this Job.  # noqa: E501
        :rtype: str
        """
        return self._start_frame

    @start_frame.setter
    def start_frame(self, start_frame):
        """Sets the start_frame of this Job.


        :param start_frame: The start_frame of this Job.  # noqa: E501
        :type: str
        """

        self._start_frame = start_frame

    @property
    def stop_frame(self):
        """Gets the stop_frame of this Job.  # noqa: E501


        :return: The stop_frame of this Job.  # noqa: E501
        :rtype: str
        """
        return self._stop_frame

    @stop_frame.setter
    def stop_frame(self, stop_frame):
        """Sets the stop_frame of this Job.


        :param stop_frame: The stop_frame of this Job.  # noqa: E501
        :type: str
        """

        self._stop_frame = stop_frame

    @property
    def task_id(self):
        """Gets the task_id of this Job.  # noqa: E501


        :return: The task_id of this Job.  # noqa: E501
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this Job.


        :param task_id: The task_id of this Job.  # noqa: E501
        :type: str
        """

        self._task_id = task_id

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
        if issubclass(Job, dict):
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
        if not isinstance(other, Job):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
