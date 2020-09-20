"""
Tests for the `task_metadata` module.
"""


import unittest.mock as mock
from pathlib import Path
from typing import Any, Dict

import pytest
import requests
from faker import Faker
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture

from pycvat.dataset import Authenticator, task_metadata
from pycvat.type_helpers import ArbitraryTypesConfig


class TestTaskMetadata:
    """
    Tests for the `TaskMetadata` class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            task_meta: The `TaskMetadata` object under test.
            mock_auth: The mocked `Authenticator` to use for testing.
            server_metadata: The fake metadata that we will use to simulate the
                server response.
            task_id: The task ID number that we are using.
        """

        task_meta: task_metadata.TaskMetadata
        mock_auth: Authenticator
        server_metadata: Dict[str, Any]

        task_id: int

    @classmethod
    @pytest.fixture()
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
        mock_auth = mocker.create_autospec(Authenticator, instance=True)
        mock_auth.session = mocker.create_autospec(
            requests.Session, instance=True
        )
        task_id = faker.random_int()

        # Make it look like we got valid metadata from the server.
        server_metadata = faker.task_metadata(min_num_frames=10)
        mock_response = mock_auth.session.get.return_value
        mock_response.json.return_value = server_metadata

        task_meta = task_metadata.TaskMetadata(auth=mock_auth, task_id=task_id)

        return cls.ConfigForTests(
            task_meta=task_meta,
            mock_auth=mock_auth,
            task_id=task_id,
            server_metadata=server_metadata,
        )

    def test_frame_path(self, config: ConfigForTests) -> None:
        """
        Tests that `frame_path()` works.

        Args:
            config: The configuration to use for testing.

        """
        # Arrange.
        frame_num = 1

        # Act.
        got_path = config.task_meta.frame_path(frame_num)

        # Assert.
        # It should have produced the correct path.
        expected_path = config.server_metadata["frames"][frame_num]["name"]
        assert got_path == Path(expected_path)

    def test_frame_size(self, config: ConfigForTests) -> None:
        """
        Tests that `frame_size()` works.

        Args:
            config: The configuration to use for testing.

        """
        # Arrange.
        frame_num = 1

        # Act.
        got_size = config.task_meta.frame_size(frame_num)

        # Assert.
        # It should have produced the correct size.
        frame_dict = config.server_metadata["frames"][frame_num]
        expected_size = (frame_dict["width"], frame_dict["height"])
        assert got_size == expected_size

    def test_num_frames(self, config: ConfigForTests) -> None:
        """
        Tests that the `num_frames` property works.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        got_num_frames = config.task_meta.num_frames

        # Assert.
        assert got_num_frames == len(config.server_metadata["frames"])
