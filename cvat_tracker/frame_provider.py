"""
High-level API for obtaining frames and annotations.
"""


from contextlib import contextmanager
from functools import cached_property
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

from .api import Authenticator
from .task import Task
from .task_metadata import TaskMetadata


class FrameProvider:
    """
    High-level API for obtaining frames and annotations.
    """

    @classmethod
    @contextmanager
    def for_task(cls, *, task_id: int, auth: Authenticator) -> "FrameProvider":
        """
        Creates a new `FrameProvider` for the specified task. Meant to be
        used as a context manager.

        Args:
            task_id: The numerical ID of the task we are processing.
            auth: The object to use for authenticating with CVAT.

        Returns:
            The `FrameProvider` object that it created.
        """
        metadata = TaskMetadata(task_id=task_id, auth=auth)

        with Task.download(task_id=task_id, auth=auth) as task:
            yield cls(task=task, task_meta=metadata)

    def __init__(self, *, task: Task, task_meta: TaskMetadata):
        """
        Args:
            task: The `Task` object to get data from.
            task_meta: The `TaskMetadata` object to get data from.
        """
        self.__task = task
        self.__task_meta = task_meta

    @cached_property
    def __paths_to_annotations(self) -> Dict[Path, List]:
        """
        Returns:
            A mapping of image paths to the list of annotations for that image.
        """
        paths_to_annotations = {}
        for item in self.__task.dataset:
            item_path = Path(item.image.path)
            paths_to_annotations[item_path] = item.annotations

        return paths_to_annotations

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

            # Get the associated annotations. To do this, we will look at the
            # path in order to associate this frame with a particular
            # set of annotations.
            frame_path = self.__task_meta.frame_path(frame_num)
            assert (
                frame_path in self.__paths_to_annotations
            ), f"Could not find any dataset entry for image {frame_path}."
            annotations = self.__paths_to_annotations[frame_path]

            yield frame_data, annotations
