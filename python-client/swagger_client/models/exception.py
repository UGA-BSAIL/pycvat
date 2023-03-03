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

class Exception(object):
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
        'system': 'str',
        'client': 'str',
        'time': 'datetime',
        'job_id': 'int',
        'task_id': 'int',
        'proj_id': 'int',
        'client_id': 'int',
        'message': 'str',
        'filename': 'str',
        'line': 'int',
        'column': 'int',
        'stack': 'str'
    }

    attribute_map = {
        'system': 'system',
        'client': 'client',
        'time': 'time',
        'job_id': 'job_id',
        'task_id': 'task_id',
        'proj_id': 'proj_id',
        'client_id': 'client_id',
        'message': 'message',
        'filename': 'filename',
        'line': 'line',
        'column': 'column',
        'stack': 'stack'
    }

    def __init__(self, system=None, client=None, time=None, job_id=None, task_id=None, proj_id=None, client_id=None, message=None, filename=None, line=None, column=None, stack=None):  # noqa: E501
        """Exception - a model defined in Swagger"""  # noqa: E501
        self._system = None
        self._client = None
        self._time = None
        self._job_id = None
        self._task_id = None
        self._proj_id = None
        self._client_id = None
        self._message = None
        self._filename = None
        self._line = None
        self._column = None
        self._stack = None
        self.discriminator = None
        self.system = system
        self.client = client
        self.time = time
        if job_id is not None:
            self.job_id = job_id
        if task_id is not None:
            self.task_id = task_id
        if proj_id is not None:
            self.proj_id = proj_id
        self.client_id = client_id
        self.message = message
        self.filename = filename
        self.line = line
        self.column = column
        self.stack = stack

    @property
    def system(self):
        """Gets the system of this Exception.  # noqa: E501


        :return: The system of this Exception.  # noqa: E501
        :rtype: str
        """
        return self._system

    @system.setter
    def system(self, system):
        """Sets the system of this Exception.


        :param system: The system of this Exception.  # noqa: E501
        :type: str
        """
        if system is None:
            raise ValueError("Invalid value for `system`, must not be `None`")  # noqa: E501

        self._system = system

    @property
    def client(self):
        """Gets the client of this Exception.  # noqa: E501


        :return: The client of this Exception.  # noqa: E501
        :rtype: str
        """
        return self._client

    @client.setter
    def client(self, client):
        """Sets the client of this Exception.


        :param client: The client of this Exception.  # noqa: E501
        :type: str
        """
        if client is None:
            raise ValueError("Invalid value for `client`, must not be `None`")  # noqa: E501

        self._client = client

    @property
    def time(self):
        """Gets the time of this Exception.  # noqa: E501


        :return: The time of this Exception.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this Exception.


        :param time: The time of this Exception.  # noqa: E501
        :type: datetime
        """
        if time is None:
            raise ValueError("Invalid value for `time`, must not be `None`")  # noqa: E501

        self._time = time

    @property
    def job_id(self):
        """Gets the job_id of this Exception.  # noqa: E501


        :return: The job_id of this Exception.  # noqa: E501
        :rtype: int
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id):
        """Sets the job_id of this Exception.


        :param job_id: The job_id of this Exception.  # noqa: E501
        :type: int
        """

        self._job_id = job_id

    @property
    def task_id(self):
        """Gets the task_id of this Exception.  # noqa: E501


        :return: The task_id of this Exception.  # noqa: E501
        :rtype: int
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this Exception.


        :param task_id: The task_id of this Exception.  # noqa: E501
        :type: int
        """

        self._task_id = task_id

    @property
    def proj_id(self):
        """Gets the proj_id of this Exception.  # noqa: E501


        :return: The proj_id of this Exception.  # noqa: E501
        :rtype: int
        """
        return self._proj_id

    @proj_id.setter
    def proj_id(self, proj_id):
        """Sets the proj_id of this Exception.


        :param proj_id: The proj_id of this Exception.  # noqa: E501
        :type: int
        """

        self._proj_id = proj_id

    @property
    def client_id(self):
        """Gets the client_id of this Exception.  # noqa: E501


        :return: The client_id of this Exception.  # noqa: E501
        :rtype: int
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """Sets the client_id of this Exception.


        :param client_id: The client_id of this Exception.  # noqa: E501
        :type: int
        """
        if client_id is None:
            raise ValueError("Invalid value for `client_id`, must not be `None`")  # noqa: E501

        self._client_id = client_id

    @property
    def message(self):
        """Gets the message of this Exception.  # noqa: E501


        :return: The message of this Exception.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this Exception.


        :param message: The message of this Exception.  # noqa: E501
        :type: str
        """
        if message is None:
            raise ValueError("Invalid value for `message`, must not be `None`")  # noqa: E501

        self._message = message

    @property
    def filename(self):
        """Gets the filename of this Exception.  # noqa: E501


        :return: The filename of this Exception.  # noqa: E501
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this Exception.


        :param filename: The filename of this Exception.  # noqa: E501
        :type: str
        """
        if filename is None:
            raise ValueError("Invalid value for `filename`, must not be `None`")  # noqa: E501

        self._filename = filename

    @property
    def line(self):
        """Gets the line of this Exception.  # noqa: E501


        :return: The line of this Exception.  # noqa: E501
        :rtype: int
        """
        return self._line

    @line.setter
    def line(self, line):
        """Sets the line of this Exception.


        :param line: The line of this Exception.  # noqa: E501
        :type: int
        """
        if line is None:
            raise ValueError("Invalid value for `line`, must not be `None`")  # noqa: E501

        self._line = line

    @property
    def column(self):
        """Gets the column of this Exception.  # noqa: E501


        :return: The column of this Exception.  # noqa: E501
        :rtype: int
        """
        return self._column

    @column.setter
    def column(self, column):
        """Sets the column of this Exception.


        :param column: The column of this Exception.  # noqa: E501
        :type: int
        """
        if column is None:
            raise ValueError("Invalid value for `column`, must not be `None`")  # noqa: E501

        self._column = column

    @property
    def stack(self):
        """Gets the stack of this Exception.  # noqa: E501


        :return: The stack of this Exception.  # noqa: E501
        :rtype: str
        """
        return self._stack

    @stack.setter
    def stack(self, stack):
        """Sets the stack of this Exception.


        :param stack: The stack of this Exception.  # noqa: E501
        :type: str
        """
        if stack is None:
            raise ValueError("Invalid value for `stack`, must not be `None`")  # noqa: E501

        self._stack = stack

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
        if issubclass(Exception, dict):
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
        if not isinstance(other, Exception):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
