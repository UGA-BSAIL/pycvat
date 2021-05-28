# coding: utf-8

# flake8: noqa

"""
    CVAT REST API

    REST API for Computer Vision Annotation Tool (CVAT)  # noqa: E501

    OpenAPI spec version: v1
    Contact: nikita.manovich@intel.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

# import apis into sdk package
from swagger_client.api.auth_api import AuthApi
from swagger_client.api.comments_api import CommentsApi
from swagger_client.api.issues_api import IssuesApi
from swagger_client.api.jobs_api import JobsApi
from swagger_client.api.lambda_api import LambdaApi
from swagger_client.api.projects_api import ProjectsApi
from swagger_client.api.restrictions_api import RestrictionsApi
from swagger_client.api.reviews_api import ReviewsApi
from swagger_client.api.server_api import ServerApi
from swagger_client.api.tasks_api import TasksApi
from swagger_client.api.users_api import UsersApi

# import ApiClient
from swagger_client.api_client import ApiClient
from swagger_client.configuration import Configuration

# import models into sdk package
from swagger_client.models.about import About
from swagger_client.models.attribute import Attribute
from swagger_client.models.attribute_val import AttributeVal
from swagger_client.models.basic_user import BasicUser
from swagger_client.models.client_file import ClientFile
from swagger_client.models.combined_issue import CombinedIssue
from swagger_client.models.combined_review import CombinedReview
from swagger_client.models.comment import Comment
from swagger_client.models.data import Data
from swagger_client.models.data_meta import DataMeta
from swagger_client.models.dataset_format import DatasetFormat
from swagger_client.models.dataset_formats import DatasetFormats
from swagger_client.models.exception import Exception
from swagger_client.models.file_info import FileInfo
from swagger_client.models.frame_meta import FrameMeta
from swagger_client.models.issue import Issue
from swagger_client.models.job import Job
from swagger_client.models.label import Label
from swagger_client.models.labeled_data import LabeledData
from swagger_client.models.labeled_image import LabeledImage
from swagger_client.models.labeled_shape import LabeledShape
from swagger_client.models.labeled_track import LabeledTrack
from swagger_client.models.log_event import LogEvent
from swagger_client.models.login import Login
from swagger_client.models.password_change import PasswordChange
from swagger_client.models.password_reset_confirm import PasswordResetConfirm
from swagger_client.models.password_reset_serializer_ex import (
    PasswordResetSerializerEx,
)
from swagger_client.models.plugins import Plugins
from swagger_client.models.project import Project
from swagger_client.models.remote_file import RemoteFile
from swagger_client.models.restricted_register import RestrictedRegister
from swagger_client.models.review import Review
from swagger_client.models.rq_status import RqStatus
from swagger_client.models.segment import Segment
from swagger_client.models.server_file import ServerFile
from swagger_client.models.simple_job import SimpleJob
from swagger_client.models.task import Task
from swagger_client.models.tracked_shape import TrackedShape
from swagger_client.models.user import User
from swagger_client.models.user_agreement import UserAgreement
