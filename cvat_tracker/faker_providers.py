"""
Custom `Faker` providers that we use for testing.
"""


import unittest.mock as mock
from typing import Any, List, Tuple

from datumaro.components.extractor import Points
from faker import Faker
from faker.providers import BaseProvider


class CvatProvider(BaseProvider):
    """
    Specialized provider for creating fake CVAT data.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.__faker = Faker()

    def point(
        self, frame_shape: Tuple[int, ...] = (1080, 1920)
    ) -> Tuple[float, float]:
        """
        Creates a single point annotation.

        Args:
            frame_shape: The shape of the frame that the annotations should
                fall within, as a tuple of (h, w, ...).

        Returns:
            The point that it created.

        """
        # Choose the x and y coordinates.
        max_height, max_width = frame_shape[:2]
        x = self.__faker.pyfloat(min_value=0, max_value=max_width)
        y = self.__faker.pyfloat(min_value=0, max_value=max_height)

        return x, y

    def points_annotation(
        self,
        max_num_points: int = 5,
        frame_shape: Tuple[int, ...] = (1080, 1920),
    ) -> Points:
        """
        Creates a single fake `Points` instance.

        Args:
            max_num_points: The maximum number of points to allow.
            frame_shape: The shape of the frame that the annotations should
                fall within, as a tuple of (h, w, ...).

        Returns:
            The `Points` instance, which will be a mock with the correct spec.

        """
        points = mock.create_autospec(Points, instance=True)

        # Generate some reasonable point data.
        num_points = self.random_int(min=1, max=max_num_points)
        point_list = []
        for _ in range(num_points):
            point_list.extend(self.point(frame_shape=frame_shape))
        points.points = point_list

        # Add no attributes for now.
        points.attributes = {}
        # Set other members randomly.
        points.visibility = [self.__faker.pybool() for _ in range(num_points)]
        points.group = self.random_int()
        points.label = self.random_int()
        points.z_order = self.random_int()
        points.id = self.random_int()

        return points

    def points_annotations(
        self,
        *args: Any,
        min_num_annotations: int = 0,
        max_num_annotations: int = 50,
        **kwargs: Any
    ) -> List[Points]:
        """
        Generates an entire list of `Points` annotations.

        Args:
            *args: Will be forwarded to `points_annotation`.
            min_num_annotations: The minimum number of annotations that will
                be produced.
            max_num_annotations: The maximum number of annotations that will
                be produced.
            **kwargs: Will be forwarded to `points_annotation`.

        Returns:
            The list of annotations that it produced.

        """
        num_annotations = self.random_int(
            min=min_num_annotations, max=max_num_annotations
        )

        annotations = []
        for _ in range(num_annotations):
            annotations.append(self.points_annotation(*args, **kwargs))

        return annotations
