import csv
from pathlib import Path
from typing import Any, AsyncIterator, Coroutine, Iterator

from pydantic import ConfigDict, Field
from volur.pork.materials.v1alpha3 import material_pb2
from volur.pork.shared.v1alpha1 import characteristic_pb2, quantity_pb2
from volur.sdk.sources.csv.base import MaterialSource
from volur.sdk.sources.csv.shared import (
    CharacteristicColumn,
    Column,
    QuantityColumn,
    fetch_value,
    load_characteristic_value,
    load_quantity,
)


class MaterialsCSVFileSource(MaterialSource):
    def __aiter__(self: "MaterialSource") -> AsyncIterator[material_pb2.Material]:
        raise NotImplementedError

    def __anext__(
        self: "MaterialSource",
    ) -> Coroutine[None, None, material_pb2.Material]:
        raise NotImplementedError

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    path: str
    data: list[material_pb2.Material] = Field(default_factory=list, init=False)
    material_id_column: Column = Field(
        ...,
        description="""
            The column name used for getting the material identifier
            in the Material entity.
            """,
        examples=[
            Column(column_name="PRODUCTID"),
        ],
    )
    plant_id_column: Column | None = Field(
        default=None,
        description="""
            The column name used for getting the plant
            identifier in the Material entity
            """,
        examples=[
            Column(column_name="PLANTID"),
            Column(column_name="FACILITYID"),
        ],
    )
    quantity_column: QuantityColumn | None = Field(
        default=None,
        description="""
            The column name used for getting the quantity
            in the Material entity
            """,
        examples=[
            QuantityColumn(column_name="QUANTITY_KGS", unit="kilogram"),
            QuantityColumn(column_name="QUANTITY_LBS", unit="pound"),
        ],
    )
    characteristics_columns: list[CharacteristicColumn] | None = Field(
        default=None,
        description="""
                The column names used for getting the material
                characteristics in the Material entity
            """,
        examples=[
            CharacteristicColumn(
                column_name="leanPercentage",
                characteristic_name="lean_percentage",
                data_type="float",
            ),
            CharacteristicColumn(
                column_name="isFrozen",
                characteristic_name="is_frozen",
                data_type="bool",
            ),
            CharacteristicColumn(
                column_name="expirationDate",
                characteristic_name="expiration_date",
                data_type="date",
            ),
        ],
    )

    def __iter__(self: "MaterialsCSVFileSource") -> Iterator[material_pb2.Material]:  # type: ignore[override]
        self._load()
        return self

    def __next__(self: "MaterialsCSVFileSource") -> material_pb2.Material:
        if self.data:
            return self.data.pop(0)
        else:
            raise StopIteration

    def _load(self: "MaterialsCSVFileSource") -> None:
        _ = Path(self.path)
        if not _.exists():
            raise ValueError("file does not exist")
        if not _.is_file():
            raise ValueError("path is not a file")
        with _.open(mode="r") as source:
            reader: Iterator[dict[str, Any]] = csv.DictReader(source)
            for row in reader:
                material = material_pb2.Material()
                if (
                    value := fetch_value(
                        row,
                        self.material_id_column,
                    ).value_string
                ) is not None:
                    material.material_id = value
                if self.plant_id_column:
                    if (
                        value := fetch_value(
                            row,
                            self.plant_id_column,
                        ).value_string
                    ) is not None:
                        material.plant = value
                if self.quantity_column:
                    quantity_value = load_quantity(
                        row.get(self.quantity_column.column_name),
                        self.quantity_column,
                    )
                    quantity = quantity_pb2.Quantity()
                    quantity.value.CopyFrom(quantity_value)
                    material.quantity.CopyFrom(quantity)
                if self.characteristics_columns:
                    material.characteristics.extend(
                        [
                            characteristic_pb2.Characteristic(
                                name=column.characteristic_name,
                                value=load_characteristic_value(
                                    row.get(column.column_name),
                                    column,
                                ),
                            )
                            for column in self.characteristics_columns
                        ]
                    )
                self.data.append(material)
