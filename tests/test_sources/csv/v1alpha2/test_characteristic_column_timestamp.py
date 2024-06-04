from typing import Any

import pytest
from google.type.datetime_pb2 import Datetime
from volur.pork.shared.v1alpha1 import characteristic_pb2
from volur.sdk.v1alpha2.sources.csv import CharacteristicColumnDatetime

ids = [
    "return-correct-characteristic-for-a-correct-date-value-in-column1",
    "return-correct-characteristic-for-a-correct-date-value-in-column2",
    "return-empty-chracteristic-because-value-in-column-is-none",
    "raise-exception-because-value-is-not-valid-date",
    "raise-exception-because-value-is-not-string",
]

test_data = [
    (
        {
            "column_name": "15-06-2021 15:30:34",
        },
        CharacteristicColumnDatetime(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_date=Datetime(
                    year=2021, month=6, day=15, hours=15, minutes=30, seconds=34
                ),
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "10/06/2018 03:30:15 PM",
        },
        CharacteristicColumnDatetime(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_date=Datetime(
                    year=2018, month=6, day=10, hours=15, minutes=30, seconds=15
                ),
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "10/06/2018 03:10:34.45",
        },
        CharacteristicColumnDatetime(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_date=Datetime(
                    year=2018, month=6, day=10, hours=3, minutes=10, seconds=34
                ),
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "",
        },
        CharacteristicColumnDatetime(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "01-01-202",
        },
        CharacteristicColumnDatetime(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        None,
        True,
        "provided value 01-01-202 in column column_name has invalid date format",
    ),
    (
        {
            "column_name": 2020,
        },
        CharacteristicColumnDatetime(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        None,
        True,
        "provided value 2020 in column column_name can not be interpreted as date characteristic",  # noqa: E501
    ),
]


@pytest.mark.parametrize(
    argnames=[
        "data",
        "column",
        "expected",
        "should_raise_an_exception",
        "exception_text",
    ],
    argvalues=test_data,
    ids=ids,
)
def test_characteristic_column_date(
    data: dict[str | int, Any],
    column: CharacteristicColumnDatetime,
    expected: characteristic_pb2.CharacteristicValue | None,
    should_raise_an_exception: bool,
    exception_text: str | None,
) -> None:
    if should_raise_an_exception:
        with pytest.raises(ValueError, match=exception_text):
            actual = column.get_value(data)
    else:
        actual = column.get_value(data)
        assert actual == expected
