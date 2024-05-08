import io
from pathlib import Path

import pytest
from volur.pork.products.v1alpha3 import product_pb2
from volur.pork.shared.v1alpha1.characteristic_pb2 import (
    Characteristic,
    CharacteristicValue,
)
from volur.sdk.v1alpha2.sources.csv.base import (
    CharacteristicColumnString,
    Column,
)
from volur.sdk.v1alpha2.sources.csv.source import ProductsCSVFileSource


@pytest.fixture()
def products_csv_content() -> list[str]:
    return [
        "id,plant_code,description",
        "product-id-1,Plant1,Description1",
        "product-id-2,Plant1,Description2",
        "product-id-3,Plant2,Description3",
        "product-id-4,Plant2,Description4",
    ]


@pytest.fixture()
def csv_file(
    tmpdir: Path,
    products_csv_content: list[str],
) -> str:
    # See https://stackoverflow.com/questions/40784950/pathlib-path-and-py-test-localpath
    path = Path(tmpdir / "test.csv")
    with open(path, "wb") as f:
        for _ in products_csv_content:
            f.write(_.encode())
            f.write("\n".encode())
    return str(path)


@pytest.fixture()
def csv_source(
    csv_file: str,
) -> ProductsCSVFileSource:
    return ProductsCSVFileSource(
        path=csv_file,
        product_id_column=Column(column_name="id"),
        characteristics_columns=[
            CharacteristicColumnString(
                column_name="plant_code",
                characteristic_name="plant_code",
            ),
            CharacteristicColumnString(
                column_name="description",
                characteristic_name="description",
            ),
        ],
    )


@pytest.fixture()
def expected_products() -> list[product_pb2.Product]:
    return [
        product_pb2.Product(
            product_id="product-id-1",
            characteristics=[
                Characteristic(
                    name="plant_code",
                    value=CharacteristicValue(value_string="Plant1"),
                ),
                Characteristic(
                    name="description",
                    value=CharacteristicValue(value_string="Description1"),
                ),
            ],
        ),
        product_pb2.Product(
            product_id="product-id-2",
            characteristics=[
                Characteristic(
                    name="plant_code",
                    value=CharacteristicValue(value_string="Plant1"),
                ),
                Characteristic(
                    name="description",
                    value=CharacteristicValue(value_string="Description2"),
                ),
            ],
        ),
        product_pb2.Product(
            product_id="product-id-3",
            characteristics=[
                Characteristic(
                    name="plant_code",
                    value=CharacteristicValue(value_string="Plant2"),
                ),
                Characteristic(
                    name="description",
                    value=CharacteristicValue(value_string="Description3"),
                ),
            ],
        ),
        product_pb2.Product(
            product_id="product-id-4",
            characteristics=[
                Characteristic(
                    name="plant_code",
                    value=CharacteristicValue(value_string="Plant2"),
                ),
                Characteristic(
                    name="description",
                    value=CharacteristicValue(value_string="Description4"),
                ),
            ],
        ),
    ]


@pytest.mark.asyncio()
async def test_load_file(
    csv_source: ProductsCSVFileSource,
    expected_products: list[product_pb2.Product],
) -> None:
    actual_products = [_ async for _ in csv_source]
    assert actual_products == expected_products


@pytest.fixture()
def buffered_csv(products_csv_content: list[str]) -> io.BufferedIOBase:
    bio = io.BytesIO()
    for _ in products_csv_content:
        bio.write(_.encode())
        bio.write("\n".encode())
    bio.seek(0)
    return bio


@pytest.fixture()
def io_buffered_csv_source(buffered_csv: io.BufferedIOBase) -> ProductsCSVFileSource:
    return ProductsCSVFileSource(
        path=buffered_csv,
        product_id_column=Column(column_name="id"),
        characteristics_columns=[
            CharacteristicColumnString(
                column_name="plant_code",
                characteristic_name="plant_code",
            ),
            CharacteristicColumnString(
                column_name="description",
                characteristic_name="description",
            ),
        ],
    )


@pytest.mark.asyncio()
async def test_load_from_io_buffered(
    io_buffered_csv_source: ProductsCSVFileSource,
    expected_products: list[product_pb2.Product],
) -> None:
    actual_products = [_ async for _ in io_buffered_csv_source]
    actual_products.sort(key=lambda _: _.product_id)
    expected_products.sort(key=lambda _: _.product_id)
    assert actual_products == expected_products


@pytest.fixture()
def products_csv_without_header_content() -> list[str]:
    return [
        "product-id-1,Plant1,Description1",
        "product-id-2,Plant1,Description2",
        "product-id-3,Plant2,Description3",
        "product-id-4,Plant2,Description4",
    ]


@pytest.fixture()
def products_csv_without_header_file(
    tmpdir: Path,
    products_csv_without_header_content: list[str],
) -> str:
    # See https://stackoverflow.com/questions/40784950/pathlib-path-and-py-test-localpath
    path = Path(tmpdir / "test.csv")
    with open(path, "wb") as f:
        for _ in products_csv_without_header_content:
            f.write(_.encode())
            f.write("\n".encode())
    return str(path)


@pytest.fixture()
def csv_source_without_header(
    products_csv_without_header_file: str,
) -> ProductsCSVFileSource:
    return ProductsCSVFileSource(
        path=products_csv_without_header_file,
        has_header=False,
        product_id_column=Column(column_name=0),
        characteristics_columns=[
            CharacteristicColumnString(
                column_name=1,
                characteristic_name="plant_code",
            ),
            CharacteristicColumnString(
                column_name=2,
                characteristic_name="description",
            ),
        ],
    )


@pytest.mark.asyncio()
async def test_load_file_without_headers(
    csv_source_without_header: ProductsCSVFileSource,
    expected_products: list[product_pb2.Product],
) -> None:
    actual_products = [_ async for _ in csv_source_without_header]
    assert actual_products == expected_products


@pytest.fixture()
def buffered_csv_without_header(
    products_csv_without_header_content: list[str],
) -> io.BufferedIOBase:
    bio = io.BytesIO()
    for _ in products_csv_without_header_content:
        bio.write(_.encode())
        bio.write("\n".encode())
    bio.seek(0)
    return bio


@pytest.fixture()
def io_buffered_csv_without_header_source(
    buffered_csv_without_header: io.BufferedIOBase,
) -> ProductsCSVFileSource:
    return ProductsCSVFileSource(
        path=buffered_csv_without_header,
        has_header=False,
        product_id_column=Column(column_name=0),
        characteristics_columns=[
            CharacteristicColumnString(
                column_name=1,
                characteristic_name="plant_code",
            ),
            CharacteristicColumnString(
                column_name=2,
                characteristic_name="description",
            ),
        ],
    )


@pytest.mark.asyncio()
async def test_load_from_io_buffered_without_header(
    io_buffered_csv_without_header_source: ProductsCSVFileSource,
    expected_products: list[product_pb2.Product],
) -> None:
    actual_products = [_ async for _ in io_buffered_csv_without_header_source]
    actual_products.sort(key=lambda _: _.product_id)
    expected_products.sort(key=lambda _: _.product_id)
    assert actual_products == expected_products
