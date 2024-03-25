from pathlib import Path

import pytest
from volur.pork.materials.v1alpha3 import material_pb2
from volur.pork.shared.v1alpha1.characteristic_pb2 import (
    Characteristic,
    CharacteristicValue,
)
from volur.pork.shared.v1alpha1.quantity_pb2 import Quantity, QuantityValue
from volur.sdk.sources.csv import (
    CharacteristicColumn,
    Column,
    MaterialsCSVFileAsyncSource,
    QuantityColumn,
)


@pytest.fixture()
def csv_file(tmpdir: Path) -> str:
    data = """id,plant,quantity,char_value
 1,Plant1,100,1
 2,Plant2,200,2"""
    # See https://stackoverflow.com/questions/40784950/pathlib-path-and-py-test-localpath
    path = Path(tmpdir / "test.csv")
    with open(path, "wb") as f:
        f.write(data.encode("utf-8"))
    return str(path)


@pytest.fixture()
def asynchronous_csv_source(
    csv_file: str,
) -> MaterialsCSVFileAsyncSource:
    return MaterialsCSVFileAsyncSource(
        path=csv_file,
        material_id_column=Column(column_name="id"),
        plant_id_column=Column(column_name="plant"),
        quantity_column=QuantityColumn(column_name="quantity", unit="kilogram"),
        characteristics_columns=[
            CharacteristicColumn(
                column_name="char_value",
                characteristic_name="char_value",
                data_type="integer",
            )
        ],
    )


@pytest.fixture()
def expected_materials() -> list[material_pb2.Material]:
    return [
        material_pb2.Material(
            material_id=" 1",
            plant="Plant1",
            quantity=Quantity(value=QuantityValue(kilogram=100)),
            characteristics=[
                Characteristic(
                    name="char_value",
                    value=CharacteristicValue(value_integer=1),
                )
            ],
        ),
        material_pb2.Material(
            material_id=" 2",
            plant="Plant2",
            quantity=Quantity(value=QuantityValue(kilogram=200)),
            characteristics=[
                Characteristic(
                    name="char_value",
                    value=CharacteristicValue(value_integer=2),
                )
            ],
        ),
    ]


@pytest.mark.asyncio()
async def test_load_file(
    asynchronous_csv_source: MaterialsCSVFileAsyncSource,
    expected_materials: list[material_pb2.Material],
) -> None:
    actual_materials = [_ async for _ in asynchronous_csv_source]
    assert actual_materials == expected_materials