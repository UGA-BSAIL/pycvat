"""
Parses metadata for a task.
"""


from pathlib import Path
from typing import Any, Dict, List, Tuple

from backports.cached_property import cached_property
from loguru import logger

from .api import Authenticator


class TaskMetadata:
    """
    Parses metadata for a task.
    """

    def __init__(self, *, auth: Authenticator, task_id: int):
        """
        Args:
            task_id: The numerical ID of the task to load metadata for.
            auth: Object that we use for authenticating with the API.
        """
        self.__auth = auth
        self.__task_id = task_id

    @cached_property
    def __metadata(self) -> List[Dict]:
        """
        Returns:
            The parsed metadata from the CVAT server.
        """
        # Download the JSON data.
        logger.debug("Downloading metadata for task {}.", self.__task_id)
        metadata_url = self.__auth.api.tasks_id_data_meta(self.__task_id)
        metadata_response = self.__auth.session.get(metadata_url)
        metadata_response.raise_for_status()
        metadata_json = metadata_response.json()

        # Get the frame data.
        assert "frames" in metadata_json, (
            f"Got response {metadata_json} " f"without 'frames' key."
        )
        return metadata_json["frames"]

    def __frame_meta(self, frame_num: int) -> Dict[str, Any]:
        """
        Gets the associated metadata structure for a particular frame.

        Args:
            frame_num: The frame number to get metadata for.

        Returns:
            The metadata dictionary that it retrieved.

        """
        frame_data = self.__metadata
        assert frame_num < self.num_frames, (
            f"Requested frame number {frame_num}, but only have "
            f"{self.num_frames} frames."
        )

        return frame_data[frame_num]

    def frame_path(self, frame_num: int) -> Path:
        """
        Gets the path to a particular frame.

        Args:
            frame_num: The number of the frame to get the path to.

        Returns:
            The path to the frame.

        """
        return Path(self.__frame_meta(frame_num)["name"])

    def frame_size(self, frame_num: int) -> Tuple[int, int]:
        """
        Gets the size of a frame.

        Args:
            frame_num: The frame number to get the size of.

        Returns:
            The size in pixels as (width, height).

        """
        frame_meta = self.__frame_meta(frame_num)
        return frame_meta["width"], frame_meta["height"]

    @property
    def num_frames(self) -> int:
        """
        Returns:
            The total number of frames that we have.
        """
        return len(self.__metadata)
