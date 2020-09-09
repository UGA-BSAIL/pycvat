"""
Manages downloading and opening annotations from a CVAT task.
"""


import shutil
import tempfile
from contextlib import ExitStack, contextmanager
from functools import cached_property
from pathlib import Path
from typing import ContextManager
from zipfile import ZipFile

import numpy as np
from datumaro.components.project import Project, ProjectDataset
from datumaro.plugins.cvat_format.converter import CvatConverter
from datumaro.util.image import load_image
from loguru import logger
from methodtools import lru_cache

from cvat.utils.cli.core.core import CLI

from .api import Authenticator


class Task:
    """
    Manages downloading and opening annotations from a CVAT task.
    """

    _DATUMARO_FORMAT = "Datumaro 1.0"
    """
    Format string to use for CVAT data dumps.
    """
    _MAX_IMAGES_TO_CACHE = 256
    """
    Maximum number of downloaded images to cache in memory.
    """

    @classmethod
    def __load_zip(
        cls, *, zip_file: Path, extract_to: Path
    ) -> ContextManager[Path]:
        """
        Loads task data from a downloaded Datumaro zip file.

        Args:
            zip_file: The zip file to load from.
            extract_to: The directory to extract the zip file to.

        Returns:
            The path to the unzipped project directory.

        """
        # Datumaro zips pollute the current directory, so we create a
        # sub-directory to contain the extracted data.
        extracted_dir = extract_to / f"{zip_file.stem}_extracted"
        extracted_dir.mkdir(exist_ok=True)

        # Open the zip file.
        logger.debug("Extracting {} to {}...", zip_file, extracted_dir)
        with ZipFile(zip_file) as opened_zip:
            opened_zip.extractall(path=extracted_dir)

        return extracted_dir

    @classmethod
    @contextmanager
    def download(
        cls, *, task_id: int, auth: Authenticator
    ) -> ContextManager["Task"]:
        """
        Automatically downloads a task from a CVAT server. It is meant to be
        used as a context manager.

        Args:
            task_id: The ID of the task to download.
            auth: Object that we use for authenticating with the API.

        Returns:
            The `Task` that it downloaded.

        """
        logger.info("Downloading data for task {}.", task_id)

        with tempfile.TemporaryDirectory() as output_dir:
            output_dir = Path(output_dir)
            logger.debug(
                "Using {} as temporary project directory.", output_dir
            )

            # Download the annotation data from the server.
            cli = CLI(auth.session, auth.api, auth.credentials,)
            output_zip_file = output_dir / f"dataset_{task_id}.zip"
            cli.tasks_dump(task_id, cls._DATUMARO_FORMAT, output_zip_file)

            project_dir = cls.__load_zip(
                zip_file=output_zip_file, extract_to=output_dir
            )

            yield cls(project_dir=project_dir, cvat_cli=cli, task_id=task_id)

    def __init__(self, *, project_dir: Path, cvat_cli: CLI, task_id: int):
        """
        *Note: In general, this class is not meant to be instantiated directly.
        Use the factory methods instead.*

        Args:
            project_dir: The path to the task directory on the disk.
            cvat_cli: The CLI object to use for communicating with the CVAT
                server.
            task_id: The numerical ID of the task.
        """
        self.__cli = cvat_cli
        self.__task_id = task_id

        # Open the project.
        logger.debug("Opening project under {}.", project_dir)
        self.__project = Project.load(project_dir.as_posix())

        self.__remove_external_sources()

    def __remove_external_sources(self) -> None:
        """
        Removes all external sources from the project. We do this because we
        download the images manually, and only want to use *local* annotation
        data from the project.

        """
        source_names = list(self.__project.env.sources.items.keys())
        for source_name in source_names:
            logger.debug("Removing project source '{}'.", source_name)
            self.__project.remove_source(source_name)

    @contextmanager
    def __download_image(
        self, frame_num: int, output_dir: Path
    ) -> ContextManager[Path]:
        """
        Downloads an image from the CVAT server. This is meant to be used as
        a context manager; the downloaded image will be deleted upon exit.

        Args:
            frame_num: The number of the frame to load.
            output_dir: The directory to save the downloaded image in.

        Returns:
            The path to the image that it downloaded.

        """
        # Download the image.
        logger.debug("Downloading image for frame {}.", frame_num)
        self.__cli.tasks_frame(
            self.__task_id,
            frame_ids=[frame_num],
            outdir=output_dir,
            quality="original",
        )

        # The image is saved in this format.
        image_name = f"task_{self.__task_id}_frame_{frame_num:06d}.jpg"
        image_path = output_dir / image_name

        try:
            yield image_path

        finally:
            # Delete the downloaded image.
            logger.debug("Deleting downloaded frame {}.", image_path)
            image_path.unlink()

    @contextmanager
    def __make_zip(self) -> ContextManager[Path]:
        """
        Creates a zipped version of the project directory.

        Returns:
            The path to the zip file that it created. It will be deleted upon
            exit from the context.
        """
        with tempfile.TemporaryDirectory() as output_dir:
            output_dir = Path(output_dir)
            project_dir = output_dir / "project_cvat"
            project_dir.mkdir()
            zip_path = output_dir / "project_cvat_zip"

            # Save to CVAT format.
            converter = CvatConverter()
            self.dataset.export_project(
                save_dir=project_dir, converter=converter
            )

            # Create the archive.
            archive_name = shutil.make_archive(
                zip_path, "zip", root_dir=project_dir
            )
            archive_path = output_dir / archive_name
            logger.debug("Created project archive {}.", archive_path)

            yield archive_path

    @cached_property
    def dataset(self) -> ProjectDataset:
        """
        Returns:
            The `Dataset` for the loaded task.
        """
        return self.__project.make_dataset()

    @lru_cache(maxsize=_MAX_IMAGES_TO_CACHE)
    def get_image(
        self, frame_num: int, compressed: bool = False
    ) -> np.ndarray:
        """
        Loads a particular image from the CVAT server.

        Args:
            frame_num: The number of the frame to load.
            compressed: If true, it will return the raw JPEG data instead of
                loading it.

        Returns:
            The image that it loaded.

        """
        with ExitStack() as exit_stack:
            # Download the image to a temporary directory.
            image_dir = Path(
                exit_stack.enter_context(tempfile.TemporaryDirectory())
            )
            image_path = exit_stack.enter_context(
                self.__download_image(frame_num, image_dir)
            )

            if not compressed:
                # Load the image data.
                return load_image(image_path.as_posix()).astype(np.uint8)
            else:
                return np.fromfile(image_path.as_posix(), dtype=np.uint8)

    def upload(self) -> None:
        """
        Uploads the current version of the project to CVAT.
        """
        logger.info("Uploading project...")

        # Make sure the project is updated on the disk.
        self.__project.save()
        # Create a zip of the project.
        with self.__make_zip() as zip_path:
            self.__cli.tasks_upload(
                self.__task_id, "CVAT 1.1", zip_path.as_posix()
            )

        logger.info("Project uploaded.")
