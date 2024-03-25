from pathlib import Path
from typing import List

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
    MaterialsCSVFileSource,
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
def expected_materials() -> List[material_pb2.Material]:
    return [
        material_pb2.Material(
            material_id=" 1",
            plant="Plant1",
            quantity=Quantity(value=QuantityValue(kilogram=100)),
            characteristics=[
                Characteristic(
                    name="char_value", value=CharacteristicValue(value_integer=1)
                )
            ],
        ),
        material_pb2.Material(
            material_id=" 2",
            plant="Plant2",
            quantity=Quantity(value=QuantityValue(kilogram=200)),
            characteristics=[
                Characteristic(
                    name="char_value", value=CharacteristicValue(value_integer=2)
                )
            ],
        ),
    ]


def test_load_from_csv(
    csv_file: str, expected_materials: List[material_pb2.Material]
) -> None:
    source = MaterialsCSVFileSource(
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

    for actual, expected in zip(source, expected_materials):
        assert actual == expected


def test_file_does_not_exist() -> None:
    source = MaterialsCSVFileSource(
        path="non_existent_file.csv",
        material_id_column=Column(column_name="id"),
        plant_id_column=Column(column_name="plant"),
    )
    with pytest.raises(ValueError, match="file does not exist"):
        list(source)


def test_path_is_not_a_file(tmpdir: Path) -> None:
    source = MaterialsCSVFileSource(
        path=str(Path(tmpdir)), material_id_column=Column(column_name="id")
    )
    with pytest.raises(ValueError, match="path is not a file"):
        list(source)
