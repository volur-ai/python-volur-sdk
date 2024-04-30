"""Various classes and methods used accross sources code"""

import io
from dataclasses import dataclass, field
from typing import Iterable

from volur.pork.shared.v1alpha1 import quantity_pb2
from volur.sdk.v1alpha2.sources.csv.base import QuantityColumn


def load_quantity(
    value: str | None,
    column: QuantityColumn,
) -> quantity_pb2.QuantityValue:
    if value is None:
        return quantity_pb2.QuantityValue()
    try:
        if column.unit == "kilogram":
            return quantity_pb2.QuantityValue(kilogram=float(value))
        elif column.unit == "pound":
            return quantity_pb2.QuantityValue(pound=float(value))
        elif column.unit == "box":
            return quantity_pb2.QuantityValue(box=int(value))
        elif column.unit == "piece":
            return quantity_pb2.QuantityValue(piece=int(value))
    except ValueError as e:
        raise ValueError(
            f"unknown quantity unit {column.unit} or provided value {value} "
            f"can not be converted to {column.unit}"
        ) from e


@dataclass
class Value:
    value_string: str | None = field(default=None)
    value_integer: int | None = field(default=None)
    value_float: float | None = field(default=None)
    value_bool: bool | None = field(default=None)


def buffered_io_base_to_str_iterable(source: io.BufferedIOBase) -> Iterable[str]:
    while data := source.readline():
        yield data.strip().decode(encoding="utf-8")
