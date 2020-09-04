"""
Tests for the `tracker` module.
"""


import json
import unittest.mock as mock

import cv2
import numpy as np
import pytest
from faker import Faker
from pydantic.dataclasses import dataclass
from pytest_mock import MockFixture
from pytest_snapshot.plugin import Snapshot

from cvat_tracker import tracker
from cvat_tracker.backend.cvat_dataset import CvatDataset
from cvat_tracker.type_helpers import ArbitraryTypesConfig

from .test_images import FRAME_1_PATH, FRAME_2_PATH


class TestTracker:
    """
    Tests for the `Tracker` class.
    """

    @dataclass(frozen=True, config=ArbitraryTypesConfig)
    class ConfigForTests:
        """
        Encapsulates standard configuration for most tests.

        Attributes:
            tracker: The `Tracker` instance under test.
            mock_dataset: The mocked `CvatDataset` to use with the tracker.
            mock_sift: The mocked OpenCV SIFT object.
            mock_matcher: The mocked OpenCV feature matcher.
            mock_points_class: The mocked CVAT `Points` class.
            mock_pyr_down: The mocked `cv2.pyrDown` function.
            mock_perspective_transform: The mocked `cv2.perspectiveTransform`
                function.
            mock_find_homography: The mocked `cv2.findHomography` function.
        """

        tracker: tracker.Tracker
        mock_dataset: CvatDataset
        mock_sift: mock.Mock
        mock_matcher: mock.Mock
        mock_points_class: mock.Mock
        mock_pyr_down: mock.Mock
        mock_perspective_transform: mock.Mock
        mock_find_homography: mock.Mock

    @classmethod
    @pytest.fixture
    def config(cls, mocker: MockFixture) -> ConfigForTests:
        """
        Generates standard configuration for tests.

        Args:
            mocker: The fixture to use for mocking.

        Returns:
            The configuration that it generated.

        """
        # Mock the dependencies.
        mock_dataset = mocker.create_autospec(CvatDataset, instance=True)
        mock_sift_create = mocker.patch("cv2.SIFT_create")
        mock_sift = mock_sift_create.return_value
        mock_matcher_create = mocker.patch("cv2.FlannBasedMatcher_create")
        mock_matcher = mock_matcher_create.return_value
        mock_points_class = mocker.patch(tracker.__name__ + ".Points")
        mock_pyr_down = mocker.patch("cv2.pyrDown")
        mock_perspective_transform = mocker.patch("cv2.perspectiveTransform")
        mock_find_homography = mocker.patch("cv2.findHomography")

        # Create the Tracker under test.
        _tracker = tracker.Tracker(mock_dataset)

        return cls.ConfigForTests(
            tracker=_tracker,
            mock_dataset=mock_dataset,
            mock_sift=mock_sift,
            mock_matcher=mock_matcher,
            mock_points_class=mock_points_class,
            mock_pyr_down=mock_pyr_down,
            mock_perspective_transform=mock_perspective_transform,
            mock_find_homography=mock_find_homography,
        )

    @pytest.mark.parametrize(
        "start_frame", [0, 5], ids=["start_frame_0", "start_frame_5"]
    )
    def test_track_forward(
        self,
        config: ConfigForTests,
        mocker: MockFixture,
        faker: Faker,
        start_frame: int,
    ) -> None:
        """
        Tests that `track_forward()` works.

        Args:
            config: The configuration to use for testing.
            mocker: The fixture to use for mocking.
            faker: The fixture to use for generating fake data.
            start_frame: The frame to start tracking from during the test.

        """
        # Arrange.
        # Create some fake annotations.
        first_annotations = faker.points_annotations()
        next_annotations = faker.points_annotations()

        # Make it look like we have some frame data.
        mock_first_frame = mocker.create_autospec(np.ndarray, instance=True)
        mock_next_frame = mocker.create_autospec(np.ndarray, instance=True)
        config.mock_dataset.iter_frames_and_annotations.return_value = [
            (mock_first_frame, first_annotations),
            (mock_next_frame, next_annotations),
        ]

        # Make it look like SIFT feature extraction produces valid results.
        config.mock_sift.detectAndCompute.return_value = (
            mocker.Mock(),
            mocker.Mock(),
        )
        config.mock_matcher.return_value = [mocker.Mock(), mocker.Mock()]
        config.mock_find_homography.return_value = (
            mocker.Mock(),
            mocker.Mock(),
        )

        # Make sure that our fake perspective transformation produces valid
        # points. In this case, we're just going to have it add 1 to the
        # input points.
        config.mock_perspective_transform.side_effect = lambda p, _: p + 1

        # Act.
        updated_annotations = config.tracker.track_forward(
            start_frame=start_frame
        )

        # Assert.
        # It should have added the new annotations to the original ones.
        assert len(updated_annotations) == len(first_annotations) + len(
            next_annotations
        )
        for annotation in next_annotations:
            # The original annotations on the second frame should have not
            # been touched.
            assert annotation in updated_annotations
        for annotation in first_annotations:
            # The original annotations on the first frame should have been
            # changed.
            assert annotation not in updated_annotations

        # It should have saved the updated annotations.
        config.mock_dataset.update_annotations.assert_called_once_with(
            start_frame + 1, updated_annotations
        )

    @pytest.mark.slow
    @pytest.mark.integration
    def test_track_forward_integration(
        self, snapshot: Snapshot, mocker: MockFixture, faker: Faker
    ) -> None:
        """
        Full integration test of the `track_forward()` method that uses a
        snapshot of the tracked annotations from real data.

        Args:
            snapshot: The fixture to use for snapshot testing.
            mocker: The fixture to use for mocking.
            faker: The fixture to use for generating fake data.

        """
        # Arrange.
        # Load some real frame data.
        frame_1 = cv2.imread(FRAME_1_PATH.as_posix())
        frame_2 = cv2.imread(FRAME_2_PATH.as_posix())

        # Create some fake annotations for those frames also.
        annotations_1 = faker.points_annotations(frame_shape=frame_1.shape)
        annotations_2 = faker.points_annotations(frame_shape=frame_2.shape)

        # Mock the dataset so that it reads real frames.
        mock_dataset = mocker.create_autospec(CvatDataset, instance=True)
        mock_dataset.iter_frames_and_annotations.return_value = [
            (frame_1, annotations_1),
            (frame_2, annotations_2),
        ]

        # Create the tracker.
        _tracker = tracker.Tracker(mock_dataset)

        # Act.
        updated_annotations = _tracker.track_forward()

        # Assert.
        # Serialize the new annotation points.
        annotation_points = [a.points for a in updated_annotations]
        serial_points = json.dumps(annotation_points)

        snapshot.assert_match(serial_points, "annotation_points.json")
