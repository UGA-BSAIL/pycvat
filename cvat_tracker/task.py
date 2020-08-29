"""
Manages downloading and opening annotations from a CVAT task.
"""


import tempfile
from contextlib import ExitStack, contextmanager
from functools import cached_property
from pathlib import Path
from zipfile import ZipFile

import requests
from datumaro.components.project import Project, ProjectDataset
from loguru import logger

from cvat.utils.cli.core.core import CLI, CVAT_API_V1


class Task:
    """
    Manages downloading and opening annotations from a CVAT task.
    """

    _DATUMARO_FORMAT = "Datumaro 1.0"
    """
    Format string to use for CVAT data dumps.
    """

    @classmethod
    def __load_zip(cls, *, zip_file: Path, extract_to: Path) -> "Task":
        """
        Loads task data from a downloaded Datumaro zip file.

        Args:
            zip_file: The zip file to load from.
            extract_to: The directory to extract the zip file to.

        Returns:
            The `Task` that it created.

        """
        # Datumaro zips pollute the current directory, so we create a
        # sub-directory to contain the extracted data.
        extracted_dir = extract_to / f"{zip_file.stem}_extracted"
        extracted_dir.mkdir(exist_ok=True)

        # Open the zip file.
        logger.debug("Extracting {} to {}...", zip_file, extracted_dir)
        with ZipFile(zip_file) as opened_zip:
            opened_zip.extractall(path=extracted_dir)

        return Task(project_dir=extracted_dir)

    @classmethod
    @contextmanager
    def download(
        cls,
        *,
        task_id: int,
        user: str,
        password: str,
        server: str = "localhost:8080",
    ) -> "Task":
        """
        Automatically downloads a task from a CVAT server. It is meant to be used as a context manager.

        Args:
            task_id: The ID of the task to download.
            user: The user to log into CVAT as.
            password: The user's password.
            server: The address of the server to download the task from.

        Returns:
            The `Task` that it downloaded.

        """
        logger.info("Downloading data for task {}.", task_id)

        with ExitStack() as exit_stack:
            session = exit_stack.enter_context(requests.Session())
            # Data will be downloaded to a temporary directory.
            output_dir = Path(
                exit_stack.enter_context(tempfile.TemporaryDirectory())
            )
            logger.debug(
                "Using {} as temporary project directory.", output_dir
            )

            # Download the annotation data from the server.
            api = CVAT_API_V1(server)
            cli = CLI(session, api, (user, password))
            output_zip_file = output_dir / f"dataset_{task_id}.zip"
            cli.tasks_dump(task_id, cls._DATUMARO_FORMAT, output_zip_file)

            yield cls.__load_zip(
                zip_file=output_zip_file, extract_to=output_dir
            )

    def __init__(self, *, project_dir: Path):
        """
        Args:
            project_dir: The path to the task directory on the disk.
        """
        # Open the project.
        logger.debug("Opening project under {}.", project_dir)
        self.__project = Project.load(project_dir.as_posix())

    @cached_property
    def dataset(self) -> ProjectDataset:
        """
        Returns:
            The `Dataset` for the loaded task.
        """
        return self.__project.make_dataset()
