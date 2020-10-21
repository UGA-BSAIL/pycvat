"""
Tests for the `labels` module.
"""


import unittest.mock as mock

import pytest
from faker import Faker
from pycvat.dataset import labels
from pycvat.type_helpers import ArbitraryTypesConfig
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture


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
            mock_label_annotation_class: The mocked `LabelAnnotation` class.
        """

        label: labels.Label
        mock_label_annotation_class: mock.Mock

    @classmethod
    @pytest.fixture
    def config(cls, faker: Faker, mocker: MockFixture) -> ConfigForTests:
        """
        Generates standard configuration for tests.

        Args:
            faker: Fixture to use for generating fake data.
            mocker: The fixture to use for mocking.

        Returns:
            The configuration that it generated.

        """
        # Mock the dependencies.
        mock_label_annotation_class = mocker.patch(
            labels.__name__ + ".LabelAnnotation"
        )

        label = labels.Label(name=faker.word(), id=faker.random_int())

        return cls.ConfigForTests(
            label=label,
            mock_label_annotation_class=mock_label_annotation_class,
        )

    def test_to_dict(self, config: ConfigForTests) -> None:
        """
        Tests that `to_dict` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        got_dict = config.label.to_dict()

        # Assert.
        assert "name" in got_dict
        assert "attributes" in got_dict
        assert "id" in got_dict
        # The name and ID should be correct.
        assert got_dict["name"] == config.label.name
        assert got_dict["id"] == config.label.id

    def test_to_annotation(self, config: ConfigForTests) -> None:
        """
        Tests that `to_annotation` works.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        got_annotation = config.label.to_annotation()

        # Assert.
        config.mock_label_annotation_class.assert_called_once_with(
            label=config.label.id, id=config.label.id
        )
        assert (
            got_annotation == config.mock_label_annotation_class.return_value
        )


class TestLabelSet:
    """
    Tests for the `LabelSet` class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            label_set: The `LabelSet` object under test.
        """

        label_set: labels.LabelSet

    @classmethod
    @pytest.fixture
    def config(cls) -> ConfigForTests:
        """
        Generates standard configuration for most tests.

        Returns:
            The configuration that it generated.

        """
        return cls.ConfigForTests(label_set=labels.LabelSet())

    def test_new_label(self, config: ConfigForTests) -> None:
        """
        Tests that we can create new labels.

        Args:
            config: The configuration to use for testing.

        """
        # Act.
        label1 = config.label_set.new_label("label_1")
        label2 = config.label_set.new_label("label_2")

        # Assert.
        # It should have named the labels right.
        assert label1.name == "label_1"
        assert label2.name == "label_2"

        # It should have used sequential IDs for the labels.
        assert label1.id == 0
        assert label2.id == 1

    def test_labels_to_cvat_spec(
        self, config: ConfigForTests, mocker: MockFixture
    ) -> None:
        """
        Tests that `labels_to_cvat_spec` works.

        Args:
            config: The configuration to use for testing.
            mocker: The fixture to use for mocking.

        """
        # Arrange.
        # Mock out the Label class for this test.
        mock_label_class = mocker.patch(labels.__name__ + ".Label")
        mock_label = mock_label_class.return_value

        # Add the fake labels.
        config.label_set.new_label("label_1")
        config.label_set.new_label("label_2")

        # Act.
        got_labels = config.label_set.to_cvat_spec()

        # Assert.
        assert got_labels == [mock_label.to_dict.return_value] * 2
