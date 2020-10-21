from contextlib import ExitStack
from typing import Any, Dict

from kedro.io import AbstractDataSet
from loguru import logger

from ..dataset.api import Authenticator


class CvatAuthDataSet(AbstractDataSet):
    """
    A Kedro `DataSet` that encapsulates CVAT authentication information.
    """

    def __init__(
        self, *, credentials: Dict[str, str], host: str = "localhost:8080"
    ):
        """
        Args:
            credentials: Credentials to use for logging into CVAT. Should
                contain two keys: "username", which is the name of the user
                to log in as, and "password", which is the password for that
                user.
            host: The address of the CVAT server to connect to.
        """
        assert (
            "username" in credentials
        ), "'username' must be specified in CVAT credentials."
        assert (
            "password" in credentials
        ), "'password' must be specified in CVAT credentials."

        self.__username = credentials["username"]
        self.__host = host

        with ExitStack() as exit_stack:
            self.__auth = exit_stack.enter_context(
                Authenticator.from_new_session(
                    user=self.__username,
                    password=credentials["password"],
                    host=host,
                )
            )
            self.__context = exit_stack.pop_all()

    def __del__(self) -> None:
        # Clean up the context for the Authenticator.
        logger.debug("Cleaning up authenticator.")
        self.__context.close()

    def _load(self) -> Authenticator:
        return self.__auth

    def _save(self, *args: Any, **kwargs: Any) -> None:
        """
        The authenticator is immutable, so this method does nothing.

        """

    def _exists(self) -> bool:
        # Is is always true, because the Authenticator object will be made
        # on-demand.
        return True

    # Not tested, because Kedro doesn't provide a public API for this.
    def _describe(self) -> Dict[str, Any]:  # pragma: no cover
        return dict(user=self.__username, host=self.__host)
