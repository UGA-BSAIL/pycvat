"""
Miscellaneous type aliases.
"""


from typing import Union

from cvat_api import LabeledImage, LabeledShape, LabeledTrack


class ArbitraryTypesConfig:
    """
    Pydantic configuration class that allows for arbitrary types.
    """

    arbitrary_types_allowed = True


LabeledObject = Union[LabeledImage, LabeledShape, LabeledTrack]
"""
Type alias for any type of annotation.
"""
