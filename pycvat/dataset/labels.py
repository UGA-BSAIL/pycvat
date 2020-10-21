"""
Wrapper around the CVAT labels JSON description format.
"""


from typing import Any, Dict, List

from loguru import logger
from pydantic.dataclasses import dataclass

from datumaro.components.extractor import Label as LabelAnnotation


@dataclass(frozen=True)
class Label:
    """
    Represents a CVAT label for a task.

    Mostly, this is not meant to be instantiated directly. Use `LabelSet`
    instead to manage labels.

    Attributes:
        name: The label name.
        id: A unique numerical ID for the label.
    """

    name: str
    id: int

    def to_dict(self) -> Dict[str, Any]:
        """
        Represents this label as a dict in the format that the CVAT API
        understands.

        Returns:
            A dictionary representing this label specification.

        """
        # For now, we don't support attributes.
        return dict(name=self.name, id=self.id, attributes=[])

    def to_annotation(self) -> LabelAnnotation:
        """
        Converts this label to the corresponding CVAT annotation subclass.

        Returns:
            The converted label.

        """
        return LabelAnnotation(label=self.id, id=self.id)


class LabelSet:
    """
    Manages a set of labels for a particular task.
    """

    def __init__(self):
        # The underlying labels, in order by their IDs.
        self.__labels = []

    def new_label(self, name: str) -> Label:
        """
        Adds a new label to the set.

        Args:
            name: The name of the label.

        Returns:
            The `Label` that it created.

        """
        label_id = len(self.__labels)
        logger.debug("Creating new label '{}' with ID {}.", name, label_id)

        label = Label(name=name, id=label_id)
        self.__labels.append(label)
        return label

    def to_cvat_spec(self) -> List[Dict[str, Any]]:
        """
        Converts the set of labels to a list of label specifications that CVAT
        can understand.

        Returns:
            The combined label specification.

        """
        return [label.to_dict() for label in self.__labels]
