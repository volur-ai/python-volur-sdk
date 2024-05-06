"""A package that contains base classes for CSV sources."""

import abc
from dataclasses import InitVar, dataclass, field
from typing import Any, Literal

from volur.pork.shared.v1alpha1 import characteristic_pb2, quantity_pb2


@dataclass
class Column:
    column_name: InitVar[str | int]
    column_id: str | int = field(init=False)

    def __post_init__(self: "Column", column_name: str | int) -> None:
        if isinstance(column_name, str):
            if not column_name:
                raise ValueError("column name can not be empty string")
        if isinstance(column_name, int):
            if column_name < 0:
                raise ValueError("column index must be equal or more than 0")
        self.column_id = column_name


@dataclass
class QuantityColumn(Column):
    unit: InitVar[
        Literal[
            "kilogram",
            "pound",
            "box",
            "piece",
        ]
    ]
    unit_id: str = field(init=False)

    def __post_init__(
        self: "QuantityColumn",
        column_name: str | int,
        unit: str,
    ) -> None:
        super().__post_init__(column_name)
        if unit == "":
            raise ValueError("unit can not be empty string")
        self.unit_id = unit

    def get_value(
        self: "QuantityColumn",
        data: dict[str | int, Any],
    ) -> quantity_pb2.Quantity:
        _ = data.get(self.column_id, None)
        value = quantity_pb2.QuantityValue()
        if _ is None:
            return quantity_pb2.Quantity(value=value)
        if _ == "":
            return quantity_pb2.Quantity(value=value)
        try:
            match self.unit_id:
                case "kilogram":
                    value.kilogram = float(_)
                case "pound":
                    value.pound = float(_)
                case "box":
                    value.box = int(_)
                case "piece":
                    value.piece = int(_)
                case _:
                    pass
        except ValueError as error:
            raise ValueError(
                f"provided value {_} in column {self.column_id} can not be interpreted as {self.unit_id}"  # noqa: E501
            ) from error
        return quantity_pb2.Quantity(value=value)


@dataclass
class CharacteristicColumn(Column):
    characteristic_name: InitVar[str]
    characteristic_id: str = field(init=False)

    def __post_init__(
        self: "CharacteristicColumn",
        column_name: str | int,
        characteristic_name: str,
    ) -> None:
        super().__post_init__(column_name)
        if characteristic_name == "":
            raise ValueError("characteristic name can not be empty")
        self.characteristic_id = characteristic_name

    @abc.abstractmethod
    def get_value(
        self: "CharacteristicColumn",
        data: dict[str | int, Any],
    ) -> characteristic_pb2.Characteristic: ...


@dataclass
class CharacteristicColumnFloat(CharacteristicColumn):
    def get_value(
        self: "CharacteristicColumn",
        data: dict[str | int, Any],
    ) -> characteristic_pb2.Characteristic:
        _ = data.get(self.column_id, None)
        if _ is None:
            return characteristic_pb2.Characteristic(
                name=self.characteristic_id,
                value=characteristic_pb2.CharacteristicValue(),
            )
        if _ == "":
            return characteristic_pb2.Characteristic(
                name=self.characteristic_id,
                value=characteristic_pb2.CharacteristicValue(),
            )
        else:
            try:
                value = float(_)
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_id,
                    value=characteristic_pb2.CharacteristicValue(
                        value_float=value,
                    ),
                )
            except ValueError as error:
                raise ValueError(
                    f"provided value {_} in column {self.column_id} can not be interpreted as float characteristic"  # noqa: E501
                ) from error


class CharacteristicColumnInteger(CharacteristicColumn):
    def get_value(
        self: "CharacteristicColumnInteger",
        data: dict[str | int, Any],
    ) -> characteristic_pb2.Characteristic:
        _ = data.get(self.column_id, None)
        if _ is None:
            return characteristic_pb2.Characteristic(
                name=self.characteristic_id,
                value=characteristic_pb2.CharacteristicValue(),
            )
        if _ == "":
            return characteristic_pb2.Characteristic(
                name=self.characteristic_id,
                value=characteristic_pb2.CharacteristicValue(),
            )
        else:
            try:
                value = int(_)
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_id,
                    value=characteristic_pb2.CharacteristicValue(
                        value_integer=value,
                    ),
                )
            except ValueError as error:
                raise ValueError(
                    f"provided value {_} in column {self.column_id} can not be interpreted as integer characteristic"  # noqa: E501
                ) from error


class CharacteristicColumnString(CharacteristicColumn):
    def get_value(
        self: "CharacteristicColumnString",
        data: dict[str | int, Any],
    ) -> characteristic_pb2.Characteristic:
        _ = data.get(self.column_id, None)
        if _ is None:
            return characteristic_pb2.Characteristic(
                name=self.characteristic_id,
                value=characteristic_pb2.CharacteristicValue(),
            )
        if _ == "":
            return characteristic_pb2.Characteristic(
                name=self.characteristic_id,
                value=characteristic_pb2.CharacteristicValue(),
            )
        else:
            try:
                value = str(_)
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_id,
                    value=characteristic_pb2.CharacteristicValue(
                        value_string=value,
                    ),
                )
            except ValueError as e:
                raise ValueError(
                    f"provided value {_} in column {self.column_id} can not be interpreted as string characteristic"  # noqa: E501
                ) from e


@dataclass
class CharacteristicColumnBool(CharacteristicColumn):
    extra_values_true: list[str] = field(default_factory=list)
    extra_values_false: list[str] = field(default_factory=list)
    true_values: list[str] = field(init=False)
    false_values: list[str] = field(init=False)
    default_values_true: list[str] = field(default_factory=lambda: ["true"], init=False)
    default_values_false: list[str] = field(
        default_factory=lambda: ["false"], init=False
    )

    def __post_init__(
        self: "CharacteristicColumnBool",
        column_name: str | int,
        characteristic_name: str,
    ) -> None:
        super().__post_init__(column_name, characteristic_name)
        self.true_values = [
            *self.default_values_true,
            *[_.lower() for _ in self.extra_values_true],
        ]
        self.false_values = [
            *self.default_values_false,
            *[_.lower() for _ in self.extra_values_false],
        ]

    def get_value(
        self: "CharacteristicColumnBool",
        data: dict[str | int, Any],
    ) -> characteristic_pb2.Characteristic:
        _ = data.get(self.column_id, None)
        if _ is None:
            return characteristic_pb2.Characteristic(
                name=self.characteristic_id,
                value=characteristic_pb2.CharacteristicValue(),
            )
        if _ == "":
            return characteristic_pb2.Characteristic(
                name=self.characteristic_id,
                value=characteristic_pb2.CharacteristicValue(),
            )
        else:
            if _.lower() in set(self.true_values):
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_id,
                    value=characteristic_pb2.CharacteristicValue(
                        value_bool=True,
                    ),
                )
            elif _.lower() in set(self.false_values):
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_id,
                    value=characteristic_pb2.CharacteristicValue(
                        value_bool=False,
                    ),
                )
            else:
                raise ValueError(
                    f"provided value {_} in column {self.column_id} can not be interpreted as bool characteristic"  # noqa: E501
                )
