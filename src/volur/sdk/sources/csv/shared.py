"""Various classes and methods used accross sources code"""

import csv
from pathlib import Path
from typing import Iterator, Literal

import aiofiles
from pydantic import BaseModel, Field
from volur.pork.shared.v1alpha1 import characteristic_pb2, quantity_pb2


class Column(BaseModel):
    column_name: str
    data_type: Literal[
        "string",
        "bool",
        "integer",
        "float",
        "datetime",
        "date",
    ] = Field("string", description="The data type of the column")


class CharacteristicColumn(Column):
    characteristic_name: str


def load_characteristic_value(
    value: str | None,
    column: CharacteristicColumn,
) -> characteristic_pb2.CharacteristicValue:
    if value is None:
        return characteristic_pb2.CharacteristicValue()
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
        return Value()
    if column.data_type == "string":
        return Value(value_string=value)
    elif column.data_type == "integer":
        try:
            _ = int(value)
            return Value(value_integer=_)
        except ValueError as error:
            raise ValueError(
                f"column {column.column_name} is not an integer"
            ) from error
    elif column.data_type == "float":
        try:
            _ = float(value)
            return Value(value_float=_)
        except ValueError as error:
            raise ValueError(f"column {column.column_name} is not an float") from error
    elif column.data_type == "bool":
        if value.lower() in ["true", "false"]:
            return Value(value_bool=bool(value))
        else:
            raise ValueError(f"column {column.column_name} is not an bool")
    else:
        raise ValueError(f"unknown data type {column.data_type}")


async def read(
    path: str,
    columns: list[Column | None],
    delimeter: str,
) -> Iterator[dict[str, str]]:
    _ = Path(path)
    if not _.exists():
        raise ValueError("file does not exist")
    if not _.is_file():
        raise ValueError("path is not a file")
    async with aiofiles.open(_, mode="r") as source:
        content = await source.read()
        reader = csv.DictReader(
            content.splitlines(),
            delimiter=delimeter,
        )
        required_columns = set([_.column_name for _ in columns if _ is not None])
        columns_present_in_file = set(reader.fieldnames)  # type: ignore[arg-type]
        missing_columns = required_columns.difference(
            columns_present_in_file,
        )
        if missing_columns:
            raise ValueError(
                f"missing columns in " f"the csv file: {','.join(missing_columns)}"
            )
        return reader
