"""A package that contains actual implementation of various CSV sources"""

import csv
import io
import pathlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import AsyncIterator

import anyio
from loguru import logger
from volur.pork.materials.v1alpha3 import material_pb2
from volur.pork.shared.v1alpha1 import quantity_pb2
from volur.sdk.v1alpha1.sources.csv.base import MaterialsSource
from volur.sdk.v1alpha2.sources.csv import shared
from volur.sdk.v1alpha2.sources.csv.base import (
    CharacteristicColumn,
    Column,
    QuantityColumn,
)


@dataclass
class MaterialsCSVFileSource(MaterialsSource):
    """A CSV source for Materials.

    This class simplfies the upload of Materials Information using CSV.

    Arguments:
        path: A path to the CSV file containing materials information.
        material_id_column: A column that is used to uniquely identify a material in a dataset
        delimiter: A delimiter used in CSV file
        plant_id_column: A column that is used to reference a production plant where material is used
        quantity_column: A column that represent the quantity of material
        characteristics_columns: Specifies a list of arbitrary characteristics of a given material

    Examples:
        ### Minimal working example
        This is a **minimal** required configuration of a CSV source for
        materials.

        ```python title="simple.py" linenums="1"
        source = MaterialsCSVFileSource(
            "materials.csv",
            material_id_column=Column(
                "source_id",
            ),
        )
        ```
        ### Extended example with multiple characteristics
        When your CSV source has a more complex configuration, you can utilise
        this class to upload information using characteristic and predefined
        columns.

        ```python title="example.py" linenums="1"
        source = MaterialsCSVFileSource(
            "materials.csv",
            material_id_column=Column(
                "material_id",
            ),
            plant_id_column=Column(
                "plant_id_column",
            ),
            quanity_column=Column(
                "weight",
                unit="kilogram",
            ),
            characteristics_columns=[
                CharacteristicColumnBool(
                    column_name="frozen",
                    characteristic_name="is_frozen",
                ),
                CharacteristicColumnString(
                    column_name="quality_category",
                    characteristic_name="quality_category",
                ),
                CharacteristicColumnFloat(
                    column_name="lean_percentage",
                    characteristic_name="lean_percentage",
                ),
            ],
        )
        ```
    """  # noqa: E501

    path: str | pathlib.Path | io.BufferedIOBase
    _data: AsyncIterator[material_pb2.Material] | None = field(
        default=None,
        init=False,
        repr=False,
    )
    delimiter: str = field(
        default=",",
    )
    material_id_column: Column | None = field(default=None)
    plant_id_column: Column | None = field(default=None)
    quantity_column: QuantityColumn | None = field(default=None)
    characteristics_columns: list[CharacteristicColumn] = field(default_factory=list)

    @property
    def columns(
        self: "MaterialsCSVFileSource",
    ) -> list[str]:
        _: list[str] = []
        if self.material_id_column:
            if self.material_id_column.column_name:
                _.append(self.material_id_column.column_name)
        if self.plant_id_column:
            if self.plant_id_column.column_name:
                _.append(self.plant_id_column.column_name)
        if self.quantity_column:
            if self.quantity_column.column_name:
                _.append(self.quantity_column.column_name)
        if self.characteristics_columns:
            for characteristic in self.characteristics_columns:
                if characteristic.column_name:
                    _.append(characteristic.column_name)
        return _

    def __aiter__(
        self: "MaterialsCSVFileSource",
    ) -> AsyncIterator[material_pb2.Material]:
        self._data = self._load()
        return self

    async def __anext__(
        self: "MaterialsCSVFileSource",
    ) -> material_pb2.Material:
        if self._data is None:
            self._data = self._load()
        data = await anext(self._data, None)
        if data is None:
            raise StopAsyncIteration()
        return data

    async def _load(
        self: "MaterialsCSVFileSource",
    ) -> AsyncIterator[material_pb2.Material]:
        logger.info("reading data from a CSV file")
        if isinstance(self.path, io.BufferedIOBase):
            reader = csv.DictReader(
                shared.buffered_io_base_to_str_iterable(self.path),
                delimiter=self.delimiter,
            )
            for data in reader:
                yield self._create_material(data)
        if isinstance(self.path, (str, Path)):
            with open(self.path, mode="r") as source:
                reader = csv.reader(  # type: ignore[assignment]
                    source,
                    delimiter=self.delimiter,
                    strict=True,
                )
                header = next(reader)
                async for row in anyio.wrap_file(source):
                    data = dict(
                        zip(
                            header,
                            next(
                                csv.reader(
                                    [row],
                                    delimiter=self.delimiter,
                                    strict=True,
                                )
                            ),
                        ),
                    )
                    yield self._create_material(data)
        logger.info("finished reading data from a CSV file")

    def _create_material(
        self: "MaterialsCSVFileSource",
        data: dict[str, str],
    ) -> material_pb2.Material:
        material = material_pb2.Material()
        if self.material_id_column:
            _ = data.get(self.material_id_column.column_name, None)
            if _ is not None and _ != "":
                material.material_id = _
            else:
                raise ValueError(
                    f"""material id is required, found empty value
                    in material id column {self.material_id_column.column_name}"""
                )
        if self.plant_id_column:
            _ = data.get(self.plant_id_column.column_name, None)
            if _ is not None and _ != "":
                material.plant = _
            else:
                raise ValueError(
                    f"""plant id is required, found empty value
                    in plant id column {self.plant_id_column.column_name}"""
                )
        if self.quantity_column:
            quantity_value = shared.load_quantity(
                data.get(self.quantity_column.column_name),
                self.quantity_column,
            )
            quantity = quantity_pb2.Quantity()
            quantity.value.CopyFrom(quantity_value)
            material.quantity.CopyFrom(quantity)
        if self.characteristics_columns:
            material.characteristics.extend(
                [column.get_value(data) for column in self.characteristics_columns]
            )
        return material
