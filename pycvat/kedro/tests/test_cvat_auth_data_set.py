import unittest.mock as mock

import pytest
from faker import Faker
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture

from pycvat.kedro import cvat_auth_data_set
from pycvat.type_helpers import ArbitraryTypesConfig


class TestCvatAuthDataSet:
    """
    Tests for the `CvatAuthDataSet` class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            data_set: The `CvatAuthDataSet` under test.
            mock_auth_class: The mocked `Authenticator` class to use.
            user: The username to use for logging in.
            password: The password to use for logging in.
            host: The CVAT host to connect to.
        """

        data_set: cvat_auth_data_set.CvatAuthDataSet
        mock_auth_class: mock.Mock

        user: str
        password: str
        host: str

    @classmethod
    @pytest.fixture
    def config(cls, faker: Faker, mocker: MockFixture) -> ConfigForTests:
        """
        Generates standard configuration for most tests.

        Args:
            faker: The fixture to use for generating fake data.
            mocker: The fixture to use for mocking.

        Returns:
            The configuration that it generated.

        """
        # Mock the dependencies.
        mock_auth_class = mocker.patch(
            cvat_auth_data_set.__name__ + ".Authenticator"
        )

        user = faker.profile(["username"])["username"]
        password = faker.pystr()
        host = faker.hostname()
        credentials = dict(username=user, password=password)

        data_set = cvat_auth_data_set.CvatAuthDataSet(
            credentials=credentials, host=host
        )

        yield cls.ConfigForTests(
            data_set=data_set,
            mock_auth_class=mock_auth_class,
            user=user,
            password=password,
            host=host,
        )

        # Manually call the destructor before the mocks exit scope, since it
        # needs the mocks to be active to work.
        data_set.__del__()

    def test_init(self, config: ConfigForTests) -> None:
        """
        Tests that we can initialize a `CvatAuthDataSet` correctly.

        Args:
            config: The configuration to use for testing.

        """
        # Arrange and act done in fixtures.
        # Assert.
        # It should have created the underlying Authenticator object.
        config.mock_auth_class.from_new_session.assert_called_once_with(
            user=config.user, password=config.password, host=config.host
        )

    def test_del(self, config: ConfigForTests) -> None:
        """
        Tests that everything gets cleaned up properly.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        config.data_set.__del__()

        # Assert.
        # It should have exited the context that it created.
        config.mock_auth_class.from_new_session.return_value.__exit__.assert_called_once()

    def test_load(self, config: ConfigForTests) -> None:
        """
        Tests that `load` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        got_auth = config.data_set.load()

        # Assert.
        mock_auth = config.mock_auth_class.from_new_session.return_value
        assert got_auth == mock_auth.__enter__.return_value

    def test_exists(self, config: ConfigForTests) -> None:
        """
        Tests that `exists` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act and assert.
        assert config.data_set.exists()
