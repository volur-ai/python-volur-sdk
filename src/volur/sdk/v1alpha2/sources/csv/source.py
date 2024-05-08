"""A package that contains actual implementation of various CSV sources"""

import csv
import io
import pathlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncIterator, Iterable

import anyio
from volur.pork.materials.v1alpha3 import material_pb2
from volur.pork.products.v1alpha3 import product_pb2

from .base import (
    CharacteristicColumn,
    Column,
    MaterialsSource,
    ProductsSource,
    QuantityColumn,
)


def buffered_io_base_to_str_iterable(source: io.BufferedIOBase) -> Iterable[str]:
    while data := source.readline():
        yield data.strip().decode(encoding="utf-8")


@dataclass
class MaterialsCSVFileSource(MaterialsSource):
    """A CSV source for Materials.

    This class simplifies the upload of Materials Information using CSV.

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
    has_header: bool = field(default=True)
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
    characteristics_columns: list[CharacteristicColumn] = field(
        default_factory=list,
    )

    @property
    def columns(
        self: "MaterialsCSVFileSource",
    ) -> list[str | int]:
        _: list[str | int] = []
        if self.material_id_column:
            if self.material_id_column:
                _.append(self.material_id_column.column_id)
        if self.plant_id_column:
            _.append(self.plant_id_column.column_id)
        if self.quantity_column:
            _.append(self.quantity_column.column_id)
        if self.characteristics_columns:
            for characteristic in self.characteristics_columns:
                _.append(characteristic.column_id)
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

    def _load(
        self: "MaterialsCSVFileSource",
    ) -> AsyncIterator[material_pb2.Material]:
        return (
            self._load_data_from_a_file_with_header()
            if self.has_header
            else self._load_data_from_a_file_without_header()
        )

    async def _load_data_from_a_file_with_header(
        self: "MaterialsCSVFileSource",
    ) -> AsyncIterator[material_pb2.Material]:
        if isinstance(self.path, io.BufferedIOBase):
            reader = csv.DictReader(
                buffered_io_base_to_str_iterable(self.path),
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

    async def _load_data_from_a_file_without_header(
        self: "MaterialsCSVFileSource",
    ) -> AsyncIterator[material_pb2.Material]:
        if isinstance(self.path, io.BufferedIOBase):
            dialect = csv.Sniffer().sniff(self.path.read(1024).decode("utf-8"))
            self.path.seek(0)
            reader = csv.reader(
                buffered_io_base_to_str_iterable(self.path),
                dialect=dialect,
                strict=True,
            )
            first_row = next(reader)
            number_of_columns = max(
                max(self.columns),
                len(first_row),
            )
            self.path.seek(0)
            reader = csv.reader(
                buffered_io_base_to_str_iterable(self.path),
                dialect=dialect,
                strict=True,
            )
            for _ in reader:
                data = dict(zip(range(number_of_columns), _))  # type: ignore[arg-type]
                print(data)
                yield self._create_material(data)  # type: ignore[arg-type]
        if isinstance(self.path, (str, Path)):
            with open(self.path, mode="r") as source:
                reader = csv.reader(
                    source,
                    delimiter=self.delimiter,
                    strict=True,
                )
                first_row = next(reader)
                number_of_columns = max(max(self.columns), len(first_row))
                source.seek(0)
                async for row in anyio.wrap_file(source):
                    data = dict(
                        zip(
                            range(number_of_columns),  # type: ignore[arg-type]
                            next(
                                csv.reader(
                                    [row],
                                    delimiter=self.delimiter,
                                    strict=True,
                                )
                            ),
                        ),
                    )
                    yield self._create_material(data)  # type: ignore[arg-type]

    def _create_material(
        self: "MaterialsCSVFileSource",
        data: dict[str | int, Any],
    ) -> material_pb2.Material:
        material = material_pb2.Material()
        if self.material_id_column:
            material.material_id = data.get(
                self.material_id_column.column_id,
                None,
            )
            # todo: support auto-generation of material_id
        if self.plant_id_column:
            material.plant = data.get(self.plant_id_column.column_id, None)
        if self.quantity_column:
            quantity = self.quantity_column.get_value(data)
            material.quantity.CopyFrom(quantity)
        if self.characteristics_columns:
            material.characteristics.extend(
                [column.get_value(data) for column in self.characteristics_columns]
            )
        return material


@dataclass
class ProductsCSVFileSource(ProductsSource):
    """A CSV source for Products.

    This class simplifies the upload of Product Information using CSV.
    Arguments:
        path: A path to the CSV file containing product information.
        product_id_column: A column that is used to uniquely identify a product in a dataset
        delimiter: A delimiter used in CSV file
        characteristics_columns: Specifies a list of arbitrary characteristics of a given product

    Examples:
        ### Minimal working example
        This is a **minimal** required configuration of a CSV source for
        products.
        ```python title="simple.py" linenums="1"
        source = ProductCSVFileSource(
            "products.csv",
            product_id_column=Column(
                "source_id",
            ),
        )
        ```
        ### Extended example with multiple characteristics
        When your CSV source has a more complex configuration, you can utilise
        this class to upload information using characteristic and predefined
        columns.
        ```python title="example.py" linenums="1"
        source = ProductCSVFileSource(
            "products.csv",
            product_id_column=Column(
                "product_id",
            ),
            characteristics_columns=[
                CharacteristicColumn(
                    "description",
                    "string",
                    characteristic_name="description",
                ),
                CharacteristicColumn(
                    "plant_number",
                    "integer",
                    characteristic_name="plant_number",
                ),
            ],
        )
        ```
    """  # noqa: E501

    path: str | pathlib.Path | io.BufferedIOBase
    has_header: bool = field(default=True)
    _data: AsyncIterator[product_pb2.Product] | None = field(
        default=None,
        init=False,
        repr=False,
    )
    delimiter: str = field(
        default=",",
    )
    product_id_column: Column | None = field(default=None)
    characteristics_columns: list[CharacteristicColumn] = field(
        default_factory=list,
    )

    @property
    def columns(
        self: "ProductsCSVFileSource",
    ) -> list[str | int]:
        _: list[str | int] = []
        if self.product_id_column:
            if self.product_id_column:
                _.append(self.product_id_column.column_id)
        if self.characteristics_columns:
            for characteristic in self.characteristics_columns:
                _.append(characteristic.column_id)
        return _

    def __aiter__(
        self: "ProductsCSVFileSource",
    ) -> AsyncIterator[product_pb2.Product]:
        self._data = self._load()
        return self

    async def __anext__(
        self: "ProductsCSVFileSource",
    ) -> product_pb2.Product:
        if self._data is None:
            self._data = self._load()
        data = await anext(self._data, None)
        if data is None:
            raise StopAsyncIteration()
        return data

    def _load(
        self: "ProductsCSVFileSource",
    ) -> AsyncIterator[product_pb2.Product]:
        return (
            self._load_data_from_a_file_with_header()
            if self.has_header
            else self._load_data_from_a_file_without_header()
        )

    async def _load_data_from_a_file_with_header(
        self: "ProductsCSVFileSource",
    ) -> AsyncIterator[product_pb2.Product]:
        if isinstance(self.path, io.BufferedIOBase):
            reader = csv.DictReader(
                buffered_io_base_to_str_iterable(self.path),
                delimiter=self.delimiter,
            )
            for data in reader:
                yield self._create_product(data)
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
                    yield self._create_product(data)

    async def _load_data_from_a_file_without_header(
        self: "ProductsCSVFileSource",
    ) -> AsyncIterator[product_pb2.Product]:
        if isinstance(self.path, io.BufferedIOBase):
            dialect = csv.Sniffer().sniff(self.path.read(1024).decode("utf-8"))
            self.path.seek(0)
            reader = csv.reader(
                buffered_io_base_to_str_iterable(self.path),
                dialect=dialect,
                strict=True,
            )
            first_row = next(reader)
            number_of_columns = max(
                max(self.columns),
                len(first_row),
            )
            self.path.seek(0)
            reader = csv.reader(
                buffered_io_base_to_str_iterable(self.path),
                dialect=dialect,
                strict=True,
            )
            for _ in reader:
                data = dict(zip(range(number_of_columns), _))  # type: ignore[arg-type]
                print(data)
                yield self._create_product(data)  # type: ignore[arg-type]
        if isinstance(self.path, (str, Path)):
            with open(self.path, mode="r") as source:
                reader = csv.reader(
                    source,
                    delimiter=self.delimiter,
                    strict=True,
                )
                first_row = next(reader)
                number_of_columns = max(max(self.columns), len(first_row))
                source.seek(0)
                async for row in anyio.wrap_file(source):
                    data = dict(
                        zip(
                            range(number_of_columns),  # type: ignore[arg-type]
                            next(
                                csv.reader(
                                    [row],
                                    delimiter=self.delimiter,
                                    strict=True,
                                )
                            ),
                        ),
                    )
                    yield self._create_product(data)  # type: ignore[arg-type]

    def _create_product(
        self: "ProductsCSVFileSource",
        data: dict[str | int, Any],
    ) -> product_pb2.Product:
        product = product_pb2.Product()
        if self.product_id_column:
            product.product_id = data.get(
                self.product_id_column.column_id,
                None,
            )
        if self.characteristics_columns:
            product.characteristics.extend(
                [column.get_value(data) for column in self.characteristics_columns]
            )
        return product
