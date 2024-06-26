"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Quantity(google.protobuf.message.Message):
    """This could maybe be abstratcted outside pork? Will leave it here for now

    Quantity represents a measurable amount of an item, encapsulated in a
    value that specifies the unit of measure. For example, it can describe
    a certain number of pieces or a weight in kilograms. It's essential for
    contexts where an explicit declaration of the measurement unit is crucial.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUE_FIELD_NUMBER: builtins.int
    @property
    def value(self) -> global___QuantityValue:
        """QuantityValue holds the actual value of the quantity in a specified unit."""

    def __init__(
        self,
        *,
        value: global___QuantityValue | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["value", b"value"]) -> None: ...

global___Quantity = Quantity

@typing.final
class QuantityValue(google.protobuf.message.Message):
    """QuantityValue acts as a union type for various representations of quantity.
    A client should set the appropriate field based on the unit of measure being
    used. Typically, a quantity would be expressed in either a count of items
    (piece, box) or a weight (kilogram, pound), or both.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PIECE_FIELD_NUMBER: builtins.int
    BOX_FIELD_NUMBER: builtins.int
    KILOGRAM_FIELD_NUMBER: builtins.int
    POUND_FIELD_NUMBER: builtins.int
    piece: builtins.int
    """The quantity in individual countable units or pieces."""
    box: builtins.int
    """The quantity in pre-defined box units (e.g., boxes of a fixed item count)."""
    kilogram: builtins.float
    """The weight of the quantity in kilograms."""
    pound: builtins.float
    """The weight of the quantity in pounds."""
    def __init__(
        self,
        *,
        piece: builtins.int = ...,
        box: builtins.int = ...,
        kilogram: builtins.float = ...,
        pound: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["box", b"box", "kilogram", b"kilogram", "piece", b"piece", "pound", b"pound"]) -> None: ...

global___QuantityValue = QuantityValue
