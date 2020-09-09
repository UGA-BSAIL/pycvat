"""
Tests for the `cvat_dataset` module.
"""


import unittest.mock as mock
from pathlib import Path

import pytest
from faker import Faker
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture

from pycvat.dataset import cvat_dataset
from pycvat.dataset.api import Authenticator
from pycvat.dataset.task import Task
from pycvat.dataset.task_metadata import TaskMetadata
from pycvat.type_helpers import ArbitraryTypesConfig


class TestCvatDataset:
    """
    Tests for the CvatDataset class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            dataset: The `CvatDataset` object under test.
            mock_task: The mocked `Task` object.
            mock_task_meta: The mocked `TaskMetadata` object.
            mock_dataset_item_class: The mocked `DatasetItem` class.
        """

        dataset: cvat_dataset.CvatDataset
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
            cvat_dataset.__name__ + ".DatasetItem"
        )

        dataset = cvat_dataset.CvatDataset(
            task=mock_task, task_meta=mock_task_metadata
        )

        return cls.ConfigForTests(
            dataset=dataset,
            mock_task=mock_task,
            mock_task_metadata=mock_task_metadata,
            mock_dataset_item_class=mock_dataset_item_class,
        )

    @pytest.mark.parametrize(
        "frame_num", [0, 5], ids=["frame_num_0", "frame_num_5"]
    )
    def test_iter_frames_and_annotations(
        self, config: ConfigForTests, faker: Faker, frame_num: int
    ) -> None:
        """
        Tests that `iter_frames_and_annotations` works.

        Args:
            config: The configuration to use for testing.
            faker: The fixture to use for generating fake data.
            frame_num: The frame number to test iterating from.

        """
        # Arrange.
        # Make it look like we have enough frames.
        config.mock_task_metadata.num_frames = frame_num + 1

        # Make it look like the underlying CVAT dataset contains some data.
        item1 = faker.dataset_item(allow_no_images=False)
        item2 = faker.dataset_item(allow_no_images=False)
        config.mock_task.dataset.__iter__.return_value = [item1, item2]

        # Set the correct paths for our frames so that it reads the first item.
        config.mock_task_metadata.frame_path.return_value = Path(
            item1.image.path
        )

        # Act.
        pairs_iter = config.dataset.iter_frames_and_annotations(
            start_at=frame_num
        )
        frame, annotations = next(iter(pairs_iter))

        # Assert.
        assert frame == config.mock_task.get_image.return_value
        # It should have gotten the first item.
        assert annotations == item1.annotations

        # It should have gotten the right frame.
        config.mock_task.get_image.assert_called_once_with(frame_num)
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

        # Make it look like the underlying CVAT dataset contains some data.
        item = faker.dataset_item(allow_no_images=False)
        config.mock_task.dataset.__iter__.return_value = [item]

        # Set the correct paths for our frames so that it reads the item.
        config.mock_task_metadata.frame_path.return_value = Path(
            item.image.path
        )

        annotations = faker.points_annotations()

        # Act.
        config.dataset.update_annotations(frame_num, annotations)

        # Assert.
        # It should have updated the item in the dataset.
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
            cvat_dataset.__name__ + ".TaskMetadata"
        )
        mock_task_class = mocker.patch(cvat_dataset.__name__ + ".Task")

        # Act.
        with cvat_dataset.CvatDataset.for_task(
            task_id=task_id, auth=mock_auth
        ):
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
