"""
Manages downloading and opening annotations from a CVAT task.
"""


from pathlib import Path
from typing import Any, Iterable, List

import cv2
import numpy as np
from loguru import logger
from methodtools import lru_cache

from cvat_api import ApiClient, ClientFile, Data, Label
from cvat_api import Task as TaskModel
from cvat_api import TasksApi

from .clearable_cached_property import ClearableCachedProperty
from .cvat_connector import CvatConnector
from .job import Job
from .swagger_extensions import ExtendedTasksApi


class Task(CvatConnector):
    """
    Manages downloading and opening annotations from a CVAT task.
    """

    _MAX_IMAGES_TO_CACHE = 256
    """
    Maximum number of downloaded images to cache in memory.
    """

    @classmethod
    def create_new(
        cls,
        *,
        api_client: ApiClient,
        name: str,
        labels: Iterable[Label],
        bug_tracker: str = "",
        images: List[Path] = [],
    ) -> "Task":
        """
        Creates a brand new task and uploads it to the server.

        Args:
            api_client: The client to use for accessing the CVAT API.
            name: The name of the new task.
            labels: The annotation labels that should be used for the new task.
            bug_tracker: Specify the URL of a bug tracker for the new task.
            images: A list of the paths to the images to annotate for this task.

        Returns:
            The task that it created.

        """
        # Create the task on the server.
        api = ExtendedTasksApi(api_client)
        task_model = TaskModel(
            name=name, labels=labels, bug_tracker=bug_tracker
        )
        task_model = api.tasks_create(task_model)
        logger.info("Created new task with ID {}.", task_model.id)

        # Add the images to the task.
        logger.debug("Uploading task images...")
        client_files = [ClientFile(file=i) for i in images]
        task_data = Data(image_quality=70, client_files=client_files)
        api.tasks_data_create(task_data, task_model.id)

        return cls(task_id=task_model.id, api_client=api_client)

    def __init__(self, *, task_id: int, **kwargs: Any):
        """
        Args:
            task_id: The numerical ID of the task.
            **kwargs: Will be forwarded to the superclass.
        """
        super().__init__(**kwargs)

        self.__task_api = TasksApi(self.api)
        self.__task_id = task_id

    @ClearableCachedProperty
    def __task_data(self) -> TaskModel:
        """
        Gets the general task data from the API.

        Returns:
            The task data that it got.

        """
        logger.debug("Downloading data for task {}.", self.__task_id)
        return self.__task_api.tasks_read(self.__task_id)

    def __download_image(self, frame_num: int) -> np.ndarray:
        """
        Downloads an image from the CVAT server.

        Args:
            frame_num: The number of the frame to load.

        Returns:
            The raw image data that it downloaded.

        """
        # Download the image.
        logger.debug("Downloading image for frame {}.", frame_num)
        task = self.__task_api.tasks_data_read(
            self.__task_id,
            "frame",
            "original",
            frame_num,
            # This is necessary, because otherwise Swagger tries to decode
            # the image data as UTF-8.
            _preload_content=False,
        )

        return np.fromstring(task.data, dtype=np.uint8)

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
        image = self.__download_image(frame_num)

        if not compressed:
            # Load the image data.
            return cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
        else:
            return image

    def get_jobs(self) -> List[Job]:
        """
        Gets all the jobs associated with this task.

        Returns:
            The jobs for the task.

        """
        # Get the job numbers.
        segments = self.__task_data.segments
        all_jobs = []
        for segment in segments:
            all_jobs.extend([j.id for j in segment.jobs])
        logger.debug("Got job IDs {} for task {}.", all_jobs, self.__task_id)

        # Create the Job objects.
        return [Job(job_id=i, api_client=self.__jobs_api) for i in all_jobs]

    def get_labels(self) -> List[Label]:
        """
        Returns:
            The labels associated with this task.

        """
        return self.__task_data.labels[:]

    def find_label(self, name: str) -> Label:
        """
        Gets a label with a specific name.

        Args:
            name: The name of the desired label.

        Returns:
            The label it found.

        Raises:
            NameError if there is no label with that name.

        """
        for label in self.get_labels():
            if label.name == name:
                return label

        raise NameError(f"There is no label with name '{name}'.")

    @property
    def id(self) -> int:
        """
        Returns:
            The ID for the task.
        """
        return self.__task_id

    def reload(self) -> None:
        logger.debug("Forcing data reload.")

        Task.__task_data.flush_cache(self)
        # Clear all cached images.
        self.get_image.cache_clear()

    def upload(self) -> None:
        logger.debug("Uploading task data to CVAT.")

        # Make sure all the job data is up-to-date.
        for job in self.get_jobs():
            job.upload()
