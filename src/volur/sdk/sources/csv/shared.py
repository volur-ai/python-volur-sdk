from typing import Literal

from pydantic import BaseModel, Field
from volur.pork.shared.v1alpha1 import characteristic_pb2, quantity_pb2


class Column(BaseModel):
    column_name: str


class CharacteristicColumn(Column):
    characteristic_name: str
    data_type: Literal[
        "string",
        "bool",
        "integer",
        "float",
        "datetime",
        "date",
    ]


def load_characteristic_value(
    value: str | None,
    column: CharacteristicColumn,
) -> characteristic_pb2.CharacteristicValue:
    if value is None:
        raise ValueError("value is missing")
    if column.data_type == "string":
        return characteristic_pb2.CharacteristicValue(value_string=value)
    elif column.data_type == "integer":
        return characteristic_pb2.CharacteristicValue(value_integer=int(value))
    elif column.data_type == "float":
        return characteristic_pb2.CharacteristicValue(value_float=float(value))
    elif column.data_type == "bool":
        return characteristic_pb2.CharacteristicValue(value_bool=bool(value))
    raise ValueError(
        f"unknown characteristic type or provided value {value} "
        f"can not be converted to {column.data_type}"
    )


class QuantityColumn(Column):
    unit: Literal[
        "kilogram",
        "pound",
        "box",
        "piece",
    ]


def load_quantity(
    value: str | None,
    column: QuantityColumn,
) -> quantity_pb2.QuantityValue:
    if value is None:
        raise ValueError("value is missing")
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


class Value(BaseModel):
    value_string: str | None = Field(
        default=None,
        description="The string value of the characteristic",
    )
    value_integer: int | None = Field(
        default=None,
        description="The int value of the characteristic",
    )
    value_float: float | None = Field(
        default=None,
        description="The float value of the characteristic",
    )
    value_bool: bool | None = Field(
        default=None,
        description="The bool value of the characteristic",
    )


def fetch_value(row: dict[str, str], column: Column) -> Value:
    value = row.get(column.column_name)
    if value is None:
        raise ValueError(f"column {column.column_name} does not exist")
    if value.isdigit():
        return Value(value_integer=int(value))
    elif value.replace(".", "", 1).isdigit():
        return Value(value_float=float(value))
    elif value.lower() in ["true", "false"]:
        return Value(value_bool=bool(value))
    else:
        return Value(value_string=value)
