"""
Tests for the `labels` module.
"""


import pytest
from faker import Faker
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture

from pycvat.dataset import labels
from pycvat.type_helpers import ArbitraryTypesConfig


class TestLabel:
    """
    Tests for the `Label` class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            label: The `Label` instance to use for testing.
        """

        label: labels.Label

    @classmethod
    @pytest.fixture
    def config(cls, faker: Faker) -> ConfigForTests:
        """
        Generates standard configuration for tests.

        Args:
            faker: Fixture to use for generating fake data.

        Returns:
            The configuration that it generated.

        """
        label = labels.Label(name=faker.word())
        return cls.ConfigForTests(label=label)

    def test_to_dict(self, config: ConfigForTests) -> None:
        """
        Tests that `to_dict` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        got_dict = config.label.to_dict()

        # Assert.
        # Required keys for CVAT.
        assert "name" in got_dict
        assert "attributes" in got_dict
        # The name should be correct.
        assert got_dict["name"] == config.label.name


def test_labels_to_cvat_spec(mocker: MockFixture) -> None:
    """
    Tests that `labels_to_cvat_spec` works.

    Args:
        mocker: The fixture to use for mocking.

    """
    # Arrange.
    # Create some fake labels to test with.
    mock_label1 = mocker.create_autospec(labels.Label, instance=True)
    mock_label2 = mocker.create_autospec(labels.Label, instance=True)

    # Act.
    got_labels = labels.labels_to_cvat_spec([mock_label1, mock_label2])

    # Assert.
    assert got_labels == [
        mock_label1.to_dict.return_value,
        mock_label2.to_dict.return_value,
    ]
