from typing import Any

import pytest
from volur.pork.shared.v1alpha1 import characteristic_pb2
from volur.sdk.v1alpha2.sources.csv.base import CharacteristicColumnString

ids = [
    "return-correct-characteristic-for-a-correct-string-value-in-column",
    "raise-exception-column-does-not-exist",
    "return-empty-chracteristic-because-value-in-column-is-none",
]

test_data = [
    (
        {
            "column_name": "string-value",
        },
        CharacteristicColumnString(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_string="string-value",
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "1234",
        },
        CharacteristicColumnString(
            column_name="column_name_does_not_exist",
            characteristic_name="characteristic_name",
        ),
        None,
        True,
        "can not fetch the string characteristic column with name column_name_does_not_exist",  # noqa: E501
    ),
    (
        {
            "column_name": "",
        },
        CharacteristicColumnString(
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
def test_characteristic_column_string(
    data: dict[str, Any],
    column: CharacteristicColumnString,
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
