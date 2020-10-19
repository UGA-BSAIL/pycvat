"""
Wrapper around the CVAT labels JSON description format.
"""


from typing import Any, Dict, Iterable, List

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Label:
    """
    Represents a CVAT label for a task.

    Attributes:
        name: The label name.
    """

    name: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Represents this label as a dict in the format that the CVAT API
        understands.

        Returns:
            A dictionary representing this label specification.

        """
        # For now, we don't support attributes.
        return dict(name=self.name, attributes=[])


def labels_to_cvat_spec(labels: Iterable[Label]) -> List[Dict[str, Any]]:
    """
    Converts a bunch of labels to a list of label specifications that CVAT
    can understand.

    Args:
        labels: The labels to convert.

    Returns:
        The combined label specification.

    """
    return [label.to_dict() for label in labels]
