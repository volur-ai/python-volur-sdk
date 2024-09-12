import io
from pathlib import Path

import pytest

from volur.pork.demand.v1alpha2 import demand_pb2
from volur.pork.products.v1alpha3.product_pb2 import Product
from volur.pork.shared.v1alpha1.characteristic_pb2 import (
    Characteristic,
    CharacteristicValue,
)
from volur.pork.shared.v1alpha1.quantity_pb2 import Quantity, QuantityValue
from volur.sdk.v1alpha2.sources.csv import (
    CharacteristicColumnBool,
    CharacteristicColumnFloat,
    CharacteristicColumnInteger,
    CharacteristicColumnString,
    Column,
    DemandCSVFileSource,
    QuantityColumn,
)


@pytest.fixture
def demand_csv_content() -> list[str]:
    return [
        "product,customer,plant,quantity,float_column,integer_column,string_column,bool_column",
        "product-id-1,Customer1,Plant1,100,1.0,1,string-value,true",
        "product-id-2,Customer2,Plant1,100,,1,string-value,true",
        "product-id-3,Customer3,Plant1,100,1.0,,string-value,true",
        "product-id-4,Customer4,Plant1,100,1.0,1,,false",
        "product-id-5,Customer5,Plant1,100,1.0,1,string-value,",
    ]


@pytest.fixture
def csv_file(
    tmpdir: Path,
    demand_csv_content: list[str],
) -> str:
    # See https://stackoverflow.com/questions/40784950/pathlib-path-and-py-test-localpath
    path = Path(tmpdir / "test.csv")
    with open(path, "wb") as f:
        for _ in demand_csv_content:
            f.write(_.encode())
            f.write("\n".encode())
    return str(path)


@pytest.fixture
def csv_source(
    csv_file: str,
) -> DemandCSVFileSource:
    return DemandCSVFileSource(
        path=csv_file,
        product_id_column=Column(column_name="product"),
        customer_id_column=Column(column_name="customer"),
        plant_id_column=Column(column_name="plant"),
        quantity_column=QuantityColumn(column_name="quantity", unit="kilogram"),
        characteristics_columns=[
            CharacteristicColumnFloat(
                column_name="float_column",
                characteristic_name="float-characteristic",
            ),
            CharacteristicColumnInteger(
                column_name="integer_column",
                characteristic_name="integer-characteristic",
            ),
            CharacteristicColumnString(
                column_name="string_column",
                characteristic_name="string-characteristic",
            ),
            CharacteristicColumnBool(
                column_name="bool_column",
                characteristic_name="bool-characteristic",
            ),
        ],
    )


@pytest.fixture
def expected_demand() -> list[demand_pb2.Demand]:
    return [
        demand_pb2.Demand(
            product=Product(product_id="product-id-1"),
            customer_id="Customer1",
            plant="Plant1",
            quantity=Quantity(value=QuantityValue(kilogram=100)),
            characteristics=[
                Characteristic(
                    name="float-characteristic",
                    value=CharacteristicValue(value_float=1.0),
                ),
                Characteristic(
                    name="integer-characteristic",
                    value=CharacteristicValue(value_integer=1),
                ),
                Characteristic(
                    name="string-characteristic",
                    value=CharacteristicValue(value_string="string-value"),
                ),
                Characteristic(
                    name="bool-characteristic",
                    value=CharacteristicValue(value_bool=True),
                ),
            ],
        ),
        demand_pb2.Demand(
            product=Product(product_id="product-id-2"),
            customer_id="Customer2",
            plant="Plant1",
            quantity=Quantity(value=QuantityValue(kilogram=100)),
            characteristics=[
                Characteristic(
                    name="float-characteristic",
                    value=CharacteristicValue(),
                ),
                Characteristic(
                    name="integer-characteristic",
                    value=CharacteristicValue(value_integer=1),
                ),
                Characteristic(
                    name="string-characteristic",
                    value=CharacteristicValue(value_string="string-value"),
                ),
                Characteristic(
                    name="bool-characteristic",
                    value=CharacteristicValue(value_bool=True),
                ),
            ],
        ),
        demand_pb2.Demand(
            product=Product(product_id="product-id-3"),
            customer_id="Customer3",
            plant="Plant1",
            quantity=Quantity(value=QuantityValue(kilogram=100)),
            characteristics=[
                Characteristic(
                    name="float-characteristic",
                    value=CharacteristicValue(value_float=1.0),
                ),
                Characteristic(
                    name="integer-characteristic",
                    value=CharacteristicValue(),
                ),
                Characteristic(
                    name="string-characteristic",
                    value=CharacteristicValue(value_string="string-value"),
                ),
                Characteristic(
                    name="bool-characteristic",
                    value=CharacteristicValue(value_bool=True),
                ),
            ],
        ),
        demand_pb2.Demand(
            product=Product(product_id="product-id-4"),
            customer_id="Customer4",
            plant="Plant1",
            quantity=Quantity(value=QuantityValue(kilogram=100)),
            characteristics=[
                Characteristic(
                    name="float-characteristic",
                    value=CharacteristicValue(value_float=1.0),
                ),
                Characteristic(
                    name="integer-characteristic",
                    value=CharacteristicValue(value_integer=1),
                ),
                Characteristic(
                    name="string-characteristic",
                    value=CharacteristicValue(),
                ),
                Characteristic(
                    name="bool-characteristic",
                    value=CharacteristicValue(value_bool=False),
                ),
            ],
        ),
        demand_pb2.Demand(
            product=Product(product_id="product-id-5"),
            customer_id="Customer5",
            plant="Plant1",
            quantity=Quantity(value=QuantityValue(kilogram=100)),
            characteristics=[
                Characteristic(
                    name="float-characteristic",
                    value=CharacteristicValue(value_float=1.0),
                ),
                Characteristic(
                    name="integer-characteristic",
                    value=CharacteristicValue(value_integer=1),
                ),
                Characteristic(
                    name="string-characteristic",
                    value=CharacteristicValue(value_string="string-value"),
                ),
                Characteristic(
                    name="bool-characteristic",
                    value=CharacteristicValue(),
                ),
            ],
        ),
    ]


@pytest.mark.asyncio
async def test_load_file(
    csv_source: DemandCSVFileSource,
    expected_demand: list[demand_pb2.Demand],
) -> None:
    actual_demand = [_ async for _ in csv_source]
    assert actual_demand == expected_demand


@pytest.fixture
def buffered_csv(demand_csv_content: list[str]) -> io.BufferedIOBase:
    bio = io.BytesIO()
    for _ in demand_csv_content:
        bio.write(_.encode())
        bio.write("\n".encode())
    bio.seek(0)
    return bio


@pytest.fixture
def io_buffered_csv_source(buffered_csv: io.BufferedIOBase) -> DemandCSVFileSource:
    return DemandCSVFileSource(
        path=buffered_csv,
        product_id_column=Column(column_name="product"),
        customer_id_column=Column(column_name="customer"),
        plant_id_column=Column(column_name="plant"),
        quantity_column=QuantityColumn(column_name="quantity", unit="kilogram"),
        characteristics_columns=[
            CharacteristicColumnFloat(
                column_name="float_column",
                characteristic_name="float-characteristic",
            ),
            CharacteristicColumnInteger(
                column_name="integer_column",
                characteristic_name="integer-characteristic",
            ),
            CharacteristicColumnString(
                column_name="string_column",
                characteristic_name="string-characteristic",
            ),
            CharacteristicColumnBool(
                column_name="bool_column",
                characteristic_name="bool-characteristic",
            ),
        ],
    )


@pytest.mark.asyncio
async def test_load_from_io_buffered(
    io_buffered_csv_source: DemandCSVFileSource,
    expected_demand: list[demand_pb2.Demand],
) -> None:
    actual_demand = [_ async for _ in io_buffered_csv_source]
    actual_demand.sort(key=lambda _: _.customer_id)
    expected_demand.sort(key=lambda _: _.customer_id)
    assert actual_demand == expected_demand


@pytest.fixture
def demand_csv_without_header_content() -> list[str]:
    return [
        "product-id-1,Customer1,Plant1,100,1.0,1,string-value,true",
        "product-id-2,Customer2,Plant1,100,,1,string-value,true",
        "product-id-3,Customer3,Plant1,100,1.0,,string-value,true",
        "product-id-4,Customer4,Plant1,100,1.0,1,,false",
        "product-id-5,Customer5,Plant1,100,1.0,1,string-value,",
    ]


@pytest.fixture
def demand_csv_without_header_file(
    tmpdir: Path,
    demand_csv_without_header_content: list[str],
) -> str:
    # See https://stackoverflow.com/questions/40784950/pathlib-path-and-py-test-localpath
    path = Path(tmpdir / "test.csv")
    with open(path, "wb") as f:
        for _ in demand_csv_without_header_content:
            f.write(_.encode())
            f.write("\n".encode())
    return str(path)


@pytest.fixture
def csv_source_without_header(
    demand_csv_without_header_file: str,
) -> DemandCSVFileSource:
    return DemandCSVFileSource(
        path=demand_csv_without_header_file,
        has_header=False,
        product_id_column=Column(column_name=0),
        customer_id_column=Column(column_name=1),
        plant_id_column=Column(column_name=2),
        quantity_column=QuantityColumn(column_name=3, unit="kilogram"),
        characteristics_columns=[
            CharacteristicColumnFloat(
                column_name=4,
                characteristic_name="float-characteristic",
            ),
            CharacteristicColumnInteger(
                column_name=5,
                characteristic_name="integer-characteristic",
            ),
            CharacteristicColumnString(
                column_name=6,
                characteristic_name="string-characteristic",
            ),
            CharacteristicColumnBool(
                column_name=7,
                characteristic_name="bool-characteristic",
            ),
        ],
    )


@pytest.mark.asyncio
async def test_load_file_without_headers(
    csv_source_without_header: DemandCSVFileSource,
    expected_demand: list[demand_pb2.Demand],
) -> None:
    actual_demand = [_ async for _ in csv_source_without_header]
    assert actual_demand == expected_demand


@pytest.fixture
def buffered_csv_without_header(
    demand_csv_without_header_content: list[str],
) -> io.BufferedIOBase:
    bio = io.BytesIO()
    for _ in demand_csv_without_header_content:
        bio.write(_.encode())
        bio.write("\n".encode())
    bio.seek(0)
    return bio


@pytest.fixture
def io_buffered_csv_without_header_source(
    buffered_csv_without_header: io.BufferedIOBase,
) -> DemandCSVFileSource:
    return DemandCSVFileSource(
        path=buffered_csv_without_header,
        has_header=False,
        product_id_column=Column(column_name=0),
        customer_id_column=Column(column_name=1),
        plant_id_column=Column(column_name=2),
        quantity_column=QuantityColumn(column_name=3, unit="kilogram"),
        characteristics_columns=[
            CharacteristicColumnFloat(
                column_name=4,
                characteristic_name="float-characteristic",
            ),
            CharacteristicColumnInteger(
                column_name=5,
                characteristic_name="integer-characteristic",
            ),
            CharacteristicColumnString(
                column_name=6,
                characteristic_name="string-characteristic",
            ),
            CharacteristicColumnBool(
                column_name=7,
                characteristic_name="bool-characteristic",
            ),
        ],
    )


@pytest.mark.asyncio
async def test_load_from_io_buffered_without_header(
    io_buffered_csv_without_header_source: DemandCSVFileSource,
    expected_demand: list[demand_pb2.Demand],
) -> None:
    actual_demand = [_ async for _ in io_buffered_csv_without_header_source]
    actual_demand.sort(key=lambda _: _.customer_id)
    expected_demand.sort(key=lambda _: _.customer_id)
    assert actual_demand == expected_demand
