from pathlib import Path

import pytest
from volur.pork.products.v1alpha2 import product_pb2
from volur.pork.shared.v1alpha1.characteristic_pb2 import (
    Characteristic,
    CharacteristicValue,
)
from volur.sdk.sources.csv import (
    CharacteristicColumn,
    Column,
    ProductCSVFileSource,
)


@pytest.fixture()
def csv_file(tmpdir: Path) -> str:
    data = """id,description,plant_code
 1,description1,1001
 2,description2,1002"""
    # See https://stackoverflow.com/questions/40784950/pathlib-path-and-py-test-localpath
    path = Path(tmpdir / "test.csv")
    with open(path, "wb") as f:
        f.write(data.encode("utf-8"))
    return str(path)


@pytest.fixture()
def asynchronous_csv_source(
    csv_file: str,
) -> ProductCSVFileSource:
    return ProductCSVFileSource(
        path=csv_file,
        product_id_column=Column(column_name="id"),
        characteristics_columns=[
            CharacteristicColumn(
                column_name="description",
                characteristic_name="description",
                data_type="string",
            ),
            CharacteristicColumn(
                column_name="plant_code",
                characteristic_name="plant_code",
                data_type="integer",
            ),
        ],
    )


@pytest.fixture()
def expected_product() -> list[product_pb2.Product]:
    return [
        product_pb2.Product(
            product_id=" 1",
            characteristics=[
                Characteristic(
                    name="description",
                    value=CharacteristicValue(value_string="description1"),
                ),
                Characteristic(
                    name="plant_code",
                    value=CharacteristicValue(value_integer=1001),
                ),
            ],
        ),
        product_pb2.Product(
            product_id=" 2",
            characteristics=[
                Characteristic(
                    name="description",
                    value=CharacteristicValue(value_string="description2"),
                ),
                Characteristic(
                    name="plant_code",
                    value=CharacteristicValue(value_integer=1002),
                ),
            ],
        ),
    ]


@pytest.mark.asyncio()
async def test_load_file(
    asynchronous_csv_source: ProductCSVFileSource,
    expected_product: list[product_pb2.Product],
) -> None:
    actual_product = [_ async for _ in asynchronous_csv_source]
    assert actual_product == expected_product
