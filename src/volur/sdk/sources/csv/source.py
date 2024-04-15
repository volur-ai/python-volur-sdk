"""A package that contains actual implementation of various CSV sources"""

from dataclasses import dataclass, field
from typing import AsyncIterator

from loguru import logger
from volur.pork.materials.v1alpha3 import material_pb2
from volur.pork.shared.v1alpha1.characteristic_pb2 import (
    Characteristic,
)
from volur.pork.shared.v1alpha1.quantity_pb2 import Quantity
from volur.sdk.sources.csv.base import MaterialsSource
from volur.sdk.sources.csv.shared import (
    CharacteristicColumn,
    Column,
    QuantityColumn,
    fetch_value,
    load_characteristic_value,
    load_quantity,
    read,
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
                CharacteristicColumn(
                    "frozen",
                    "boolean",
                    characteristic_name="is_frozen",
                ),
                CharacteristicColumn(
                    "quality_category",
                    "string",
                    characteristic_name="quality_category",
                ),
                CharacteristicColumn(
                    "lean_percentage",
                    "float",
                    characteristic_name="lean_percentage",
                ),
            ],
        )
        ```
    """

    path: str
    material_id_column: Column
    _data: AsyncIterator[material_pb2.Material] | None = field(
        default=None,
        init=False,
        repr=False,
    )
    delimiter: str = field(
        default=",",
    )
    plant_id_column: Column | None = field(default=None)
    quantity_column: QuantityColumn | None = field(default=None)
    characteristics_columns: list[CharacteristicColumn] = field(default_factory=list)

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
        data = await anext(self._data)
        if data is None:
            raise StopAsyncIteration()
        return data

    async def _load(
        self: "MaterialsCSVFileSource",
    ) -> AsyncIterator[material_pb2.Material]:
        logger.info("reading data from a CSV file")
        reader = await read(
            self.path,
            [
                self.material_id_column,
                self.plant_id_column,
                self.quantity_column,
                *self.characteristics_columns,
            ],
            self.delimiter,
        )
        for _, row in enumerate(reader):
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
        logger.info("finished reading data from a CSV file")
