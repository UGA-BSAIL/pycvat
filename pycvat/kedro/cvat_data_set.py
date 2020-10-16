"""
A Kedro `DataSet` for data from CVAT.
"""


from contextlib import ExitStack
from typing import Any, Dict, Tuple

from backports.cached_property import cached_property
from kedro.io import AbstractDataSet
from loguru import logger

from ..dataset import Authenticator, CvatHandle


class CvatDataSet(AbstractDataSet):
    """
    A Kedro `DataSet` for data from CVAT.
    """

    def __init__(
        self,
        *,
        task_id: int,
        credentials: Dict[str, str],
        host: str = "localhost:8080"
    ):
        """
        Args:
            task_id: The numerical ID of the task to load data from.
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

        self.__task_id = task_id
        self.__user = credentials["username"]
        self.__password = credentials["password"]
        self.__host = host

        # CVAT data is lazy-loaded, so this specifies whether the connection
        # was ever opened.
        self.__connected_to_cvat = False

    @cached_property
    def __init_cvat_handle(self) -> Tuple[CvatHandle, ExitStack]:
        """
        Initializes the CVAT handle that will be used to access this data.

        Returns:
            A handle object that can be used to access CVAT.

            Also, an `ExitStack` object that encapsulates callbacks for
            cleaning up the CVAT handle context. The `close()` method should
            be invoked manually on this object when the CVAT handle is no
            longer needed.

        """
        logger.info(
            "Initializing connection to task {} at {}.",
            self.__task_id,
            self.__host,
        )

        self.__connected_to_cvat = True

        with ExitStack() as exit_stack:
            auth = exit_stack.enter_context(
                Authenticator.from_new_session(
                    user=self.__user,
                    password=self.__password,
                    host=self.__host,
                )
            )
            handle = exit_stack.enter_context(
                CvatHandle.for_task(task_id=self.__task_id, auth=auth)
            )

            context = exit_stack.pop_all()
            return handle, context

    @property
    def __cvat(self) -> CvatHandle:
        """
        Returns:
            The CVAT handle to use. Will be created if it doesn't already exist.
        """
        cvat, _ = self.__init_cvat_handle
        return cvat

    @property
    def __cvat_context(self) -> ExitStack:
        """
        Returns:
            The `ExitStack` object that encapsulates callbacks for safely
            cleaning up the CVAT handle.
        """
        _, context = self.__init_cvat_handle
        return context

    def __del__(self) -> None:
        # Clean up the context for the CVAT handle.
        if self.__connected_to_cvat:
            logger.debug("Cleaning up CVAT handle.")
            self.__cvat_context.close()
            self.__connected_to_cvat = False

    def _load(self) -> CvatHandle:
        return self.__cvat

    def _save(self, data: CvatHandle) -> None:
        # Force the data to be uploaded now.
        data.upload_now()

    def _exists(self) -> bool:
        # This is always true, because this class only works with data that
        # already exists on CVAT.
        return True

    # Not tested, because Kedro doesn't provide a public API for this.
    def _describe(self) -> Dict[str, Any]:  # pragma: no cover
        return dict(task_id=self.__task_id, user=self.__user, host=self.__host)
