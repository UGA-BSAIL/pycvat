"""
Tests for the `cvat_data_set` module.
"""

import unittest.mock as mock

import pytest
from faker import Faker
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture

from pycvat.dataset import CvatHandle
from pycvat.kedro import cvat_data_set
from pycvat.type_helpers import ArbitraryTypesConfig


class TestCvatDataSet:
    """
    Tests for the `CvatDataSet` class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            data_set: The `CvatDataSet` object under test.
            mock_auth_class: The mocked `Authenticator` class.
            mock_cvat_handle_class: The mocked `CvatHandle` class.
            task_id: The task ID to use for testing.
            user: The username to use for testing.
            password: The password to use for testing.
            host: The CVAT server address to use for testing.
        """

        data_set: cvat_data_set.CvatDataSet
        mock_auth_class: mock.Mock
        mock_cvat_handle_class: mock.Mock

        task_id: int
        user: str
        password: str
        host: str

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
        mock_auth_class = mocker.patch(
            cvat_data_set.__name__ + ".Authenticator"
        )
        mock_cvat_handle_class = mocker.patch(
            cvat_data_set.__name__ + ".CvatHandle"
        )

        task_id = faker.random_int()
        user = faker.profile(["username"])["username"]
        password = faker.pystr()
        host = faker.hostname()
        credentials = dict(username=user, password=password)

        data_set = cvat_data_set.CvatDataSet(
            task_id=task_id, credentials=credentials, host=host
        )

        yield cls.ConfigForTests(
            data_set=data_set,
            mock_auth_class=mock_auth_class,
            mock_cvat_handle_class=mock_cvat_handle_class,
            task_id=task_id,
            user=user,
            password=password,
            host=host,
        )

        # Manually call the destructor before the mocks exit scope, since it
        # needs the mocks to be active to work.
        data_set.__del__()

    @pytest.mark.parametrize(
        "cvat_connected",
        [False, True],
        ids=["cvat_not_connected", "cvat_connected"],
    )
    def test_del(self, config: ConfigForTests, cvat_connected: bool) -> None:
        """
        Tests that everything gets cleaned up properly.

        Args:
            config: The configuration to use for testing.
            cvat_connected: True if we should have actually connected to the
                CVAT server, false otherwise.

        """
        # Arrange.
        if cvat_connected:
            # We need to perform a load operation to force it to connect to
            # CVAT.
            config.data_set.load()

        # Act.
        config.data_set.__del__()

        if cvat_connected:
            # It should have exited the context that it created.
            config.mock_auth_class.from_new_session.return_value.__exit__.assert_called_once()
            config.mock_cvat_handle_class.for_task.return_value.__exit__.assert_called_once()
        else:
            # It should not have touched the CVAT stuff.
            config.mock_auth_class.from_new_session.return_value.__exit__.assert_not_called()
            config.mock_cvat_handle_class.for_task.return_value.__exit__.assert_not_called()

    def test_load(self, config: ConfigForTests) -> None:
        """
        Tests that `load()` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        got_data = config.data_set.load()

        # Assert.
        # It should have set up the CvatHandle.
        config.mock_auth_class.from_new_session.assert_called_once_with(
            user=config.user, password=config.password, host=config.host
        )
        mock_auth = (
            config.mock_auth_class.from_new_session.return_value.__enter__.return_value
        )

        config.mock_cvat_handle_class.for_task.assert_called_once_with(
            task_id=config.task_id, auth=mock_auth
        )

        # It should not have exited the context.
        config.mock_auth_class.from_new_session.return_value.__exit__.assert_not_called()
        config.mock_cvat_handle_class.for_task.return_value.__exit__.assert_not_called()

        # It should have just given us the CVAT handle.
        mock_handle = (
            config.mock_cvat_handle_class.for_task.return_value.__enter__.return_value
        )
        assert got_data == mock_handle

    def test_save(self, config: ConfigForTests, mocker: MockFixture) -> None:
        """
        Tests that `save()` works.

        Args:
            config: The configuration to use for testing.
            mocker: The fixture to use for mocking.

        """
        # Arrange.
        # Create fake data to try saving.
        mock_handle = mocker.create_autospec(CvatHandle, instance=True)

        # Act.
        config.data_set.save(mock_handle)

        # Assert.
        # It should have uploaded the data to the server.
        mock_handle.upload_now.assert_called_once_with()

    def test_exists(self, config: ConfigForTests) -> None:
        """
        Tests that `exists()` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act and assert.
        # Currently, this always returns True.
        assert config.data_set.exists()
