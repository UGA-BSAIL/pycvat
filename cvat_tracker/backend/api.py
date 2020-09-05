"""
Tools for communicating with the CVAT API.
"""


from contextlib import contextmanager
from functools import cached_property
from typing import Any, Tuple

import requests
from loguru import logger

from cvat.utils.cli.core.core import CVAT_API_V1


class ExtendedApi(CVAT_API_V1):
    """
    Extends the `CVAT_API_V1` class with additional endpoints.
    """

    def tasks_id_data_meta(self, task_id: int) -> str:
        """
        Args:
            task_id: The ID of the task we want metadata for.

        Returns:
            The URL to `GET` in order to obtain JSON metadata for a task.

        """
        return f"{self.tasks_id_data(task_id)}/meta"


class Authenticator:
    """
    Encapsulates the login procedure for the CVAT API server.
    """

    AUTH_TOKEN_NAME = "csrftoken"
    """
    The name of the token field used in the login response.
    """
    AUTH_TOKEN_HEADER_NAME = "X-CSRFToken"
    """
    The name of the header used to store the login token.
    """

    @classmethod
    @contextmanager
    def from_new_session(cls, **kwargs: Any) -> "Authenticator":
        """
        Creates an `Authenticator` object with a new session. Meant to be used
        as a context manager.

        Args:
            **kwargs: Will be forwarded to `__init__`. All arguments except for
                `session` must still be specified.

        Returns:
            The new `Authenticator` that it created.

        """
        with requests.Session() as session:
            yield cls(session=session, **kwargs)

    def __init__(
        self,
        *,
        user: str,
        password: str,
        host: str = "localhost:8080",
        session: requests.Session,
    ):
        """
        Args:
            user: The username to authenticate with.
            password: The password to authenticated with.
            host: The server to connect to.
            session: Session to use internally for requests.
        """
        self.__user = user
        self.__password = password
        self.__session = session

        self.__api = ExtendedApi(host)

    @cached_property
    def session(self) -> requests.Session:
        """
        Returns:
            A session for the CVAT API where authentication has been
            performed for the specified user.
        """
        logger.debug("Logging into CVAT as user {}.", self.__user)

        login_url = self.__api.login
        credentials = {"username": self.__user, "password": self.__password}
        response = self.__session.post(login_url, credentials)
        response.raise_for_status()

        if self.AUTH_TOKEN_NAME in response.cookies:
            self.__session.headers[
                self.AUTH_TOKEN_HEADER_NAME
            ] = response.cookies[self.AUTH_TOKEN_NAME]

        return self.__session

    @property
    def api(self) -> ExtendedApi:
        """
        Returns:
            The object that we use to generate API URLs.
        """
        return self.__api

    @property
    def credentials(self) -> Tuple[str, str]:
        """
        Returns:
            The username and password as a tuple.
        """
        return self.__user, self.__password
