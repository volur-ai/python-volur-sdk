"""A package that contains interfaces for sources."""

import abc
from dataclasses import dataclass, field
from typing import Any, Literal

from volur.pork.shared.v1alpha1 import characteristic_pb2


@dataclass
class Column:
    column_name: str


@dataclass
class QuantityColumn(Column):
    unit: Literal[
        "kilogram",
        "pound",
        "box",
        "piece",
    ]


@dataclass
class CharacteristicColumn(Column):
    characteristic_name: str

    @abc.abstractmethod
    def get_value(
        self: "CharacteristicColumn", data: dict[str, Any]
    ) -> characteristic_pb2.Characteristic: ...


@dataclass
class CharacteristicColumnFloat(CharacteristicColumn):
    def get_value(
        self: "CharacteristicColumn",
        data: dict[str, str | None],
    ) -> characteristic_pb2.Characteristic:
        _ = data.get(self.column_name, None)
        if _ is None:
            raise ValueError(
                f"can not fetch the float characteristic column with name {self.column_name}"  # noqa: E501
            )
        if _ == "":
            return characteristic_pb2.Characteristic(
                name=self.characteristic_name,
                value=characteristic_pb2.CharacteristicValue(),
            )
        else:
            try:
                value = float(_)
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_name,
                    value=characteristic_pb2.CharacteristicValue(
                        value_float=value,
                    ),
                )
            except ValueError as error:
                raise ValueError(
                    f"can not parse value {_} in column {self.column_name} as float value"  # noqa: E501
                ) from error


class CharacteristicColumnInteger(CharacteristicColumn):
    def get_value(
        self: "CharacteristicColumnInteger", data: dict[str, str | None]
    ) -> characteristic_pb2.Characteristic:
        _ = data.get(self.column_name, None)
        if _ is None:
            raise ValueError(
                f"can not fetch the integer characteristic column with name {self.column_name}"  # noqa: E501
            )
        if _ == "":
            return characteristic_pb2.Characteristic(
                name=self.characteristic_name,
                value=characteristic_pb2.CharacteristicValue(),
            )
        else:
            try:
                value = int(_)
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_name,
                    value=characteristic_pb2.CharacteristicValue(
                        value_integer=value,
                    ),
                )
            except ValueError as error:
                raise ValueError(
                    f"can not parse value {_} in column {self.column_name} as integer value"  # noqa: E501
                    ""
                ) from error


class CharacteristicColumnString(CharacteristicColumn):
    def get_value(
        self: "CharacteristicColumnString",
        data: dict[str, str | None],
    ) -> characteristic_pb2.Characteristic:
        _ = data.get(self.column_name, None)
        if _ is None:
            raise ValueError(
                f"can not fetch the string characteristic column with name {self.column_name}"  # noqa: E501
            )
        if _ == "":
            return characteristic_pb2.Characteristic(
                name=self.characteristic_name,
                value=characteristic_pb2.CharacteristicValue(),
            )
        else:
            value = str(_)
            return characteristic_pb2.Characteristic(
                name=self.characteristic_name,
                value=characteristic_pb2.CharacteristicValue(
                    value_string=value,
                ),
            )


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

    def __post_init__(self: "CharacteristicColumnBool") -> None:
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
        data: dict[str, str | None],
    ) -> characteristic_pb2.Characteristic:
        _ = data.get(self.column_name, None)
        if _ is None:
            raise ValueError(
                f"can not fetch the bool characteristic column with name {self.column_name}"  # noqa: E501
            )
        if _ == "":
            return characteristic_pb2.Characteristic(
                name=self.characteristic_name,
                value=characteristic_pb2.CharacteristicValue(),
            )
        else:
            if _.lower() in set(self.true_values):
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_name,
                    value=characteristic_pb2.CharacteristicValue(
                        value_bool=True,
                    ),
                )
            elif _.lower() in set(self.false_values):
                return characteristic_pb2.Characteristic(
                    name=self.characteristic_name,
                    value=characteristic_pb2.CharacteristicValue(
                        value_bool=False,
                    ),
                )
            else:
                raise ValueError(
                    f"can not parse value {_} in column {self.column_name} as bool value"  # noqa: E501
                )
