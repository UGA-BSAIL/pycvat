"""
Tests for the `task` module.
"""


import unittest.mock as mock
from pathlib import Path

import pytest
from faker import Faker
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture

from cvat.utils.cli.core.core import CLI
from pycvat.dataset import task
from pycvat.dataset.api import Authenticator
from pycvat.type_helpers import ArbitraryTypesConfig


class TestTask:
    """
    Tests for the `Task` class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            task: The `Task` under test.
            mock_project_class: The mocked `datumaro` `Project` class.
            mock_cli: The mocked `CLI` object to use.
            mock_load_image: The mocked `load_image()` function.
            mock_fromfile: The mocked `numpy.fromfile()` function.

            mock_make_archive: The mocked `shutil.make_archive()` function.
            project_dir: The fake project directory that we used to create
                the task.
            task_id: The fake task ID that we used to create the task.
        """

        task: task.Task
        mock_project_class: mock.Mock
        mock_cli: CLI
        mock_load_image: mock.Mock
        mock_fromfile: mock.Mock
        mock_make_archive: mock.Mock

        project_dir: Path
        task_id: int

    @classmethod
    @pytest.fixture
    def config(cls, mocker: MockFixture, faker: Faker) -> ConfigForTests:
        """
        Generates standard configuration for most tests.

        Args:
            mocker: The fixture to use for mocking.
            faker: The fixture to use for generating fake data.

        Returns:
            The configuration that it generated.

        """
        # Mock the dependencies.
        mock_project_class = mocker.patch(task.__name__ + ".Project")
        mock_cli = mocker.create_autospec(CLI, instance=True)
        mock_load_image = mocker.patch(task.__name__ + ".load_image")
        mock_fromfile = mocker.patch("numpy.fromfile")
        mock_make_archive = mocker.patch("shutil.make_archive")

        # Make it look like we have external sources.
        mock_project = mock_project_class.load.return_value
        mock_project.env.sources.items = {"external_source": mocker.Mock()}

        project_dir = Path(faker.file_path())
        task_id = faker.random_int()

        _task = task.Task(
            project_dir=project_dir, cvat_cli=mock_cli, task_id=task_id,
        )

        return cls.ConfigForTests(
            task=_task,
            mock_project_class=mock_project_class,
            mock_cli=mock_cli,
            project_dir=project_dir,
            task_id=task_id,
            mock_load_image=mock_load_image,
            mock_fromfile=mock_fromfile,
            mock_make_archive=mock_make_archive,
        )

    def test_init(self, config: ConfigForTests) -> None:
        """
        Tests that we can initialize a new `Task` object correctly.

        Args:
            config: The configuration to use for testing.

        """
        # Arrange and act done in fixtures.
        # Assert.
        # It should have created the Datumaro project.
        config.mock_project_class.load.assert_called_once_with(
            config.project_dir.as_posix()
        )

        # It should have removed external sources.
        mock_project = config.mock_project_class.load.return_value
        for source_name in mock_project.env.sources.items.keys():
            mock_project.remove_source.assert_any_call(source_name)

    def test_dataset(self, config: ConfigForTests) -> None:
        """
        Tests that the `dataset` property works.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        got_dataset = config.task.dataset

        # Assert.
        mock_project = config.mock_project_class.load.return_value
        assert got_dataset == mock_project.make_dataset.return_value

    @pytest.mark.parametrize(
        "compressed", [False, True], ids=["not_compressed", "compressed"]
    )
    def test_get_image(
        self,
        config: ConfigForTests,
        mocker: MockFixture,
        faker: Faker,
        compressed: bool,
    ) -> None:
        """
        Tests that `get_image` works.

        Args:
            config: The configuration to use for testing.
            mocker: The fixture to use for mocking.
            faker: The fixture to use for generating fake data.
            compressed: Whether to load the compressed image or the extracted
                one.

        """
        # Arrange.
        # Mock the TemporaryDirectory function.
        mock_temp_dir = mocker.patch("tempfile.TemporaryDirectory")
        # Make it return something deterministic.
        temp_dir = Path(faker.file_path())
        mock_temp_dir.return_value.__enter__.return_value = temp_dir.as_posix()

        frame_num = faker.random_int()

        # Act.
        got_image = config.task.get_image(frame_num, compressed=compressed)

        # Assert.
        # It should have retrieved the frame from CVAT.
        config.mock_cli.tasks_frame.assert_called_once_with(
            config.task_id,
            frame_ids=[frame_num],
            outdir=mocker.ANY,
            quality=mocker.ANY,
        )

        if not compressed:
            # It should have loaded the image off the disk.
            config.mock_load_image.assert_called_once()
            loader_function = config.mock_load_image

            assert (
                got_image
                == config.mock_load_image.return_value.astype.return_value
            )
        else:
            # It should have read the raw image data.
            config.mock_fromfile.assert_called_once()
            loader_function = config.mock_fromfile

            assert got_image == config.mock_fromfile.return_value

        # Check that the image path is reasonable.
        args, _ = loader_function.call_args
        got_image_path = args[0]
        assert temp_dir.as_posix() in got_image_path

    def test_upload(self, config: ConfigForTests) -> None:
        """
        Tests that we can upload modified annotations.

        Args:
            config: The configuration to use for testing.

        """
        # Arrange.
        # Make it look like make_archive() produces a valid archive name.
        config.mock_make_archive.return_value = "archive_name"

        # Act.
        config.task.upload()

        # Assert.
        mock_dataset = (
            config.mock_project_class.load.return_value.make_dataset.return_value
        )
        mock_dataset.export_project.assert_called_once()

        # It should have archived the project.
        config.mock_make_archive.assert_called_once()

        # It should have uploaded the project.
        config.mock_cli.tasks_upload.assert_called_once_with(
            config.task_id, mock.ANY, mock.ANY
        )

    def test_download(
        self, config: ConfigForTests, mocker: MockFixture
    ) -> None:
        """
        Tests that `download` works.

        Args:
            config: The configuration to use for testing.
            mocker: The fixture to use for mocking.

        """
        # Arrange.
        # Mock the dependencies.
        mock_cli_class = mocker.patch(task.__name__ + ".CLI")
        mock_zipfile_class = mocker.patch(task.__name__ + ".ZipFile")
        mock_auth = mocker.create_autospec(Authenticator, instance=True)

        # Act.
        with task.Task.download(task_id=config.task_id, auth=mock_auth):
            pass

        # Assert.
        # It should have downloaded the task data.
        mock_cli_class.assert_called_once_with(
            mock_auth.session, mock_auth.api, mock_auth.credentials
        )
        mock_cli = mock_cli_class.return_value
        mock_cli.tasks_dump.assert_called_once_with(
            config.task_id, mocker.ANY, mocker.ANY
        )

        # It should have extracted the zip file.
        mock_zipfile_class.assert_called_once()
        mock_zipfile = mock_zipfile_class.return_value.__enter__.return_value
        mock_zipfile.extractall.assert_called_once()
