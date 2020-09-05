"""
Tests for the `api` module.
"""


import unittest.mock as mock

import pytest
import requests
from faker import Faker
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture

from cvat_tracker.backend import api
from cvat_tracker.type_helpers import ArbitraryTypesConfig


class TestExtendedApi:
    """
    Tests for the `ExtendedApi` class.
    """

    def test_task_id_and_meta(self) -> None:
        """
        Tests that `task_id_and_meta` works.

        """
        # Arrange.
        # Create an API to test with.
        host_name = "test_host:8080"
        test_api = api.ExtendedApi(host_name)

        task_id = 2

        # Act.
        got_url = test_api.tasks_id_data_meta(task_id)

        # Assert.
        assert host_name in got_url
        assert got_url.endswith(f"{task_id}/data/meta")


class TestAuthenticator:
    """
    Tests for the `Authenticator` class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            authenticator: The `Authenticator` object under test.
            mock_session: The mocked `requests.Session` instance.
            mock_api_class: The mocked `ExtendedApi` class.
            user: The username that was used.
            password: The password that was used.
            host: The host URL that was used.
        """

        authenticator: api.Authenticator
        mock_session: requests.Session
        mock_api_class: mock.Mock

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
        mock_api_class = mocker.patch(api.__name__ + ".ExtendedApi")
        mock_session = mocker.create_autospec(requests.Session, instance=True)

        # Create fake user and server information.
        user = faker.profile(["username"])["username"]
        password = faker.pystr()
        host = faker.hostname()

        auth = api.Authenticator(
            user=user, password=password, host=host, session=mock_session
        )

        return cls.ConfigForTests(
            authenticator=auth,
            mock_api_class=mock_api_class,
            mock_session=mock_session,
            user=user,
            password=password,
            host=host,
        )

    @pytest.mark.parametrize(
        "has_token", [False, True], ids=["no_token", "token"]
    )
    def test_session(
        self, config: ConfigForTests, faker: Faker, has_token: bool
    ) -> None:
        """
        Tests that the `session` property works.

        Args:
            config: The configuration to use for testing.
            faker: The fixture to use for generating fake data.
            has_token: If true, it will simulate an authentication token in the
                response from CVAT.

        """
        # Arrange.
        # Start with no headers.
        config.mock_session.headers = {}

        # Simulate the authentication token if necessary.
        mock_response = config.mock_session.post.return_value
        fake_token = faker.pystr()
        if has_token:
            mock_response.cookies = {
                api.Authenticator.AUTH_TOKEN_NAME: fake_token
            }
        else:
            mock_response.cookies = {}

        # Act.
        session = config.authenticator.session

        # Assert.
        assert session == config.mock_session

        # It should have logged in with the provided credentials.
        mock_api = config.mock_api_class.return_value
        config.mock_session.post.assert_called_once_with(
            mock_api.login,
            {"username": config.user, "password": config.password},
        )

        # It should have grabbed the token if provided.
        if has_token:
            assert (
                config.mock_session.headers[
                    api.Authenticator.AUTH_TOKEN_HEADER_NAME
                ]
                == fake_token
            )
        else:
            # There should be no headers.
            assert config.mock_session.headers == {}

    def test_api(self, config: ConfigForTests) -> None:
        """
        Tests that the `api` property works.

        Args:
            config: The configuration to use for testing.

        """
        # Act and and assert.
        assert config.authenticator.api == config.mock_api_class.return_value

    def test_credentials(self, config: ConfigForTests) -> None:
        """
        Tests that the `credentials` property works.

        Args:
            config: The configuration to use for testing.

        """
        # Act and assert.
        assert config.authenticator.credentials == (
            config.user,
            config.password,
        )

    def test_from_new_session(self, mocker: MockFixture, faker: Faker) -> None:
        """
        Tests that `from_new_session` works.

        Args:
            mocker: The fixture to use for mocking.
            faker: The fixture to use for generating fake data.

        """
        # Arrange.
        # Mock out the `Session` class.
        mock_session_class = mocker.patch("requests.Session")

        # Act.
        with api.Authenticator.from_new_session(
            user=faker.pystr(), password=faker.pystr()
        ):
            # Assert.
            # It should have created a new session.
            mock_session_class.return_value.__enter__.assert_called_once()

        # Upon exit, it should have deleted the session.
        mock_session_class.return_value.__exit__.assert_called_once()
