"""
High-level API for obtaining and updating frames and annotations.
"""


from contextlib import contextmanager
from functools import cached_property
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
from datumaro.components.extractor import DatasetItem
from loguru import logger

from .api import Authenticator
from .task import Task
from .task_metadata import TaskMetadata


class CvatHandle:
    """
    High-level API for obtaining and updating frames and annotations.
    """

    @classmethod
    @contextmanager
    def for_task(cls, *, task_id: int, auth: Authenticator) -> "CvatHandle":
        """
        Creates a new `CvatHandle` instance for the specified task. Meant to be
        used as a context manager. It will automatically re-upload the
        project to the server upon exit.

        Args:
            task_id: The numerical ID of the task we are processing.
            auth: The object to use for authenticating with CVAT.

        Returns:
            The `CvatHandle` object that it created.
        """
        metadata = TaskMetadata(task_id=task_id, auth=auth)

        with Task.download(task_id=task_id, auth=auth) as task:
            yield cls(task=task, task_meta=metadata)

            # Upload the modified project.
            task.upload()

    def __init__(self, *, task: Task, task_meta: TaskMetadata):
        """
        Args:
            task: The `Task` object to get data from.
            task_meta: The `TaskMetadata` object to get data from.
        """
        self.__task = task
        self.__task_meta = task_meta

    @cached_property
    def __paths_to_items(self) -> Dict[Path, DatasetItem]:
        """
        Returns:
            A mapping of image paths to the corresponding `DatasetItem`s.
        """
        paths_to_items = {}
        for item in self.__task.dataset:
            item_path = Path(item.image.path)
            paths_to_items[item_path] = item

        return paths_to_items

    def __get_item_for_frame(self, frame_num: int) -> DatasetItem:
        """
        Gets the corresponding `DatasetItem` for a particular frame number.

        Args:
            frame_num: The frame number to get the `DatasetItem` for.

        Returns:
            The `DatasetItem` corresponding to this frame number.

        """
        # Use the path to associate the frame with a particular set of
        # annotations.
        frame_path = self.__task_meta.frame_path(frame_num)

        assert (
            frame_path in self.__paths_to_items
        ), f"Could not find any dataset entry for image {frame_path}."
        return self.__paths_to_items[frame_path]

    def iter_frames_and_annotations(
        self, start_at: int = 0
    ) -> Iterable[Tuple[np.ndarray, List]]:
        """
        Args:
            start_at: The frame number to start iterating at.

        Yields:
            Each frame, and the corresponding list of annotation objects for
            that frame. Frames will be iterated in order.
        """
        for frame_num in range(start_at, self.__task_meta.num_frames):
            frame_data = self.__task.get_image(frame_num)
            # Get the associated annotations.
            item = self.__get_item_for_frame(frame_num)

            yield frame_data, item.annotations

    def update_annotations(self, frame_num: int, annotations: List) -> None:
        """
        Updates the annotations for a particular frame.

        Args:
            frame_num: The frame number to update the annotations for.
            annotations: The new list of annotations to set.

        """
        logger.debug("Updating annotations for frame {}.", frame_num)
        item = self.__get_item_for_frame(frame_num)

        # Update the DatasetItem with the correct annotations.
        updated_item = DatasetItem(
            id=item.id,
            annotations=annotations,
            subset=item.subset,
            path=item.path,
            image=item.image,
        )
        self.__task.dataset.put(updated_item)

    def upload_now(self) -> None:
        """
        Forces an immediate update of this data on the CVAT server. (If the
        instance was created with `for_task()`, this will be done
        automatically when exiting the context manager, and there is
        therefore no need to do it manually.)

        """
        self.__task.upload()
