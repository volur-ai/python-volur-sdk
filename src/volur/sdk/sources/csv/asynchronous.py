import csv
from pathlib import Path
from typing import Any, AsyncIterator, Iterator

import aiofiles
from pydantic import Field
from volur.pork.materials.v1alpha3 import material_pb2
from volur.pork.materials.v1alpha3.material_pb2 import Material
from volur.pork.shared.v1alpha1.characteristic_pb2 import (
    Characteristic,
)
from volur.pork.shared.v1alpha1.quantity_pb2 import Quantity
from volur.sdk.sources import MaterialSource
from volur.sdk.sources.csv.shared import (
    CharacteristicColumn,
    Column,
    QuantityColumn,
    fetch_value,
    load_characteristic_value,
    load_quantity,
)


class MaterialsCSVFileAsyncSource(MaterialSource):
    def __iter__(self: "MaterialSource") -> Iterator[material_pb2.Material]:  # type: ignore[override]
        raise NotImplementedError

    def __next__(self: "MaterialSource") -> material_pb2.Material:
        raise NotImplementedError

    _data: AsyncIterator[Material] | None = None
    path: str
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

    def __aiter__(self: "MaterialsCSVFileAsyncSource") -> "MaterialsCSVFileAsyncSource":
        self._data = self._load()
        return self

    async def __anext__(self: "MaterialsCSVFileAsyncSource") -> Material:
        if self._data is None:
            self._data = self._load()
        data = await self._data.__anext__()
        if data is None:
            raise StopAsyncIteration()
        return data

    async def _load(
        self: "MaterialsCSVFileAsyncSource",
    ) -> AsyncIterator[Material]:
        _ = Path(self.path)
        if not _.exists():
            raise ValueError("file does not exist")
        if not _.is_file():
            raise ValueError("path is not a file")
        async with aiofiles.open(_, mode="r") as source:
            content = await source.read()
            reader: Iterator[dict[str, Any]] = csv.DictReader(content.splitlines())
            for row in reader:
                material = Material()
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
                    quantity = Quantity()
                    quantity.value.CopyFrom(quantity_value)
                    material.quantity.CopyFrom(quantity)
                if self.characteristics_columns:
                    material.characteristics.extend(
                        [
                            Characteristic(
                                name=column.characteristic_name,
                                value=load_characteristic_value(
                                    row.get(column.column_name),
                                    column,
                                ),
                            )
                            for column in self.characteristics_columns
                        ]
                    )
                yield material
