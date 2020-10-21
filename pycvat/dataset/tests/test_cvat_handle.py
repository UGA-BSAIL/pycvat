"""
Tests for the `cvat_handle` module.
"""


import unittest.mock as mock
from pathlib import Path

import pytest
from faker import Faker
from pycvat.dataset import cvat_handle
from pycvat.dataset.api import Authenticator
from pycvat.dataset.task import Task
from pycvat.dataset.task_metadata import TaskMetadata
from pycvat.type_helpers import ArbitraryTypesConfig
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture


class TestCvatHandle:
    """
    Tests for the CvatHandle class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            cvat: The `CvatHandle` object under test.
            mock_task: The mocked `Task` object.
            mock_task_meta: The mocked `TaskMetadata` object.
            mock_dataset_item_class: The mocked `DatasetItem` class.
        """

        cvat: cvat_handle.CvatHandle
        mock_task: mock.Mock
        mock_task_metadata: TaskMetadata
        mock_dataset_item_class: mock.Mock

    @classmethod
    @pytest.fixture
    def config(cls, mocker: MockFixture) -> ConfigForTests:
        """
        Generates standard configuration for most tests.

        Args:
            mocker: The fixture to use for mocking.

        Returns:
            The configuration that it generated.

        """
        # Mock the dependencies.
        mock_task = mocker.MagicMock(spec=Task)
        mock_task_metadata = mocker.create_autospec(
            TaskMetadata, instance=True
        )
        mock_dataset_item_class = mocker.patch(
            cvat_handle.__name__ + ".DatasetItem"
        )

        cvat = cvat_handle.CvatHandle(
            task=mock_task, task_meta=mock_task_metadata
        )

        return cls.ConfigForTests(
            cvat=cvat,
            mock_task=mock_task,
            mock_task_metadata=mock_task_metadata,
            mock_dataset_item_class=mock_dataset_item_class,
        )

    def test_get_frame_size(self, config: ConfigForTests) -> None:
        """
        Tests that `get_frame_size()` works.

        Args:
            config: The configuration to use for testing.

        """
        # Arrange.
        frame_num = 4

        # Act.
        got_size = config.cvat.get_frame_size(frame_num)

        # Assert.
        config.mock_task_metadata.frame_size.assert_called_once_with(frame_num)
        assert got_size == config.mock_task_metadata.frame_size.return_value

    @pytest.mark.parametrize(
        "frame_num", [0, 5], ids=["frame_num_0", "frame_num_5"]
    )
    @pytest.mark.parametrize(
        "compressed", [False, True], ids=["not_compressed", "compressed"]
    )
    def test_iter_frames_and_annotations(
        self,
        config: ConfigForTests,
        faker: Faker,
        frame_num: int,
        compressed: bool,
    ) -> None:
        """
        Tests that `iter_frames_and_annotations` works.

        Args:
            config: The configuration to use for testing.
            faker: The fixture to use for generating fake data.
            frame_num: The frame number to test iterating from.
            compressed: Whether to get a compressed image.

        """
        # Arrange.
        # Make it look like we have enough frames.
        config.mock_task_metadata.num_frames = frame_num + 1

        # Make it look like the underlying CVAT cvat contains some data.
        item1 = faker.dataset_item(allow_no_images=False)
        item2 = faker.dataset_item(allow_no_images=False)
        config.mock_task.dataset.__iter__.return_value = [item1, item2]

        # Set the correct paths for our frames so that it reads the first item.
        config.mock_task_metadata.frame_path.return_value = Path(
            item1.image.path
        )

        # Act.
        pairs_iter = config.cvat.iter_frames_and_annotations(
            start_at=frame_num, compressed=compressed
        )
        frame, annotations = next(iter(pairs_iter))

        # Assert.
        assert frame == config.mock_task.get_image.return_value
        # It should have gotten the first item.
        assert annotations == item1.annotations

        # It should have gotten the right frame.
        config.mock_task.get_image.assert_called_once_with(
            frame_num, compressed=compressed
        )
        # It should have gotten the right frame metadata.
        config.mock_task_metadata.frame_path.assert_called_once_with(frame_num)

    def test_update_annotations(
        self, config: ConfigForTests, faker: Faker
    ) -> None:
        """
        Tests that `update_annotations` works.

        Args:
            config: The configuration to use for testing.
            faker: The fixture to use for generating fake data.

        """
        # Arrange.
        frame_num = 3

        # Make it look like the underlying CVAT cvat contains some data.
        item = faker.dataset_item(allow_no_images=False)
        config.mock_task.dataset.__iter__.return_value = [item]

        # Set the correct paths for our frames so that it reads the item.
        config.mock_task_metadata.frame_path.return_value = Path(
            item.image.path
        )

        annotations = faker.points_annotations()

        # Act.
        config.cvat.update_annotations(frame_num, annotations)

        # Assert.
        # It should have updated the item in the cvat.
        put_item = config.mock_dataset_item_class.return_value
        config.mock_task.dataset.put.assert_called_once_with(put_item)

        config.mock_dataset_item_class.assert_called_once_with(
            id=item.id,
            annotations=annotations,
            subset=item.subset,
            path=item.path,
            image=item.image,
        )

    def test_for_task(self, mocker: MockFixture) -> None:
        """
        Tests that `for_task` works.

        Args:
            mocker: The fixture to use for mocking.

        """
        # Arrange.
        task_id = 1

        # Mock the dependencies.
        mock_auth = mocker.create_autospec(Authenticator, instance=True)
        mock_metadata_class = mocker.patch(
            cvat_handle.__name__ + ".TaskMetadata"
        )
        mock_task_class = mocker.patch(cvat_handle.__name__ + ".Task")

        # Act.
        with cvat_handle.CvatHandle.for_task(task_id=task_id, auth=mock_auth):
            # Assert.
            mock_metadata_class.asert_called_once_with(
                task_id=task_id, auth=mock_auth
            )
            mock_task_class.download.assert_called_once_with(
                task_id=task_id, auth=mock_auth
            )

        # Upon exit, it should have uploaded the task.
        mock_task = (
            mock_task_class.download.return_value.__enter__.return_value
        )
        mock_task.upload.assert_called_once_with()

    def test_for_new_task(self, mocker: MockFixture) -> None:
        """
        Tests that `for_new_task` works.

        Args:
            mocker: The fixture to use for mocking.

        """
        # Arrange.
        task_kwargs = {"foo": 42, "bar": None}

        # Mock the dependencies.
        mock_auth = mocker.create_autospec(Authenticator, instance=True)
        mock_metadata_class = mocker.patch(
            cvat_handle.__name__ + ".TaskMetadata"
        )
        mock_task_class = mocker.patch(cvat_handle.__name__ + ".Task")

        # Act.
        with cvat_handle.CvatHandle.for_new_task(
            auth=mock_auth, **task_kwargs
        ):
            # Assert.
            # It should have created the task.
            mock_task_class.create_new.assert_called_once_with(
                auth=mock_auth, **task_kwargs
            )
            mock_task = (
                mock_task_class.create_new.return_value.__enter__.return_value
            )

            mock_metadata_class.asert_called_once_with(
                task_id=mock_task.id, auth=mock_auth
            )

        # Upon exit, it should have uploaded the task.
        mock_task.upload.assert_called_once_with()

    def test_upload_now(self, config: ConfigForTests) -> None:
        """
        Tests that `upload_now` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        config.cvat.upload_now()

        # Assert.
        config.mock_task.upload.assert_called_once_with()

    def test_num_frames(self, config: ConfigForTests) -> None:
        """
        Tests that `num_frames` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act and assert.
        assert config.cvat.num_frames == config.mock_task_metadata.num_frames
