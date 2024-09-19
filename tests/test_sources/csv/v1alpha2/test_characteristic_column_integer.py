from typing import Any

import pytest

from volur.pork.shared.v1alpha1 import characteristic_pb2
from volur.sdk.v1alpha2.sources.csv import CharacteristicColumnInteger

ids = [
    "return-correct-characteristic-for-a-correct-integer-value-in-column",
    "return-empty-chracteristic-because-value-in-column-is-none",
    "raise-exception-because-value-is-not-valid-integer",
]

test_data = [
    (
        {
            "column_name": "1234",
        },
        CharacteristicColumnInteger(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_integer=1234,
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "",
        },
        CharacteristicColumnInteger(
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
            "column_name": "non-valid-integer-value",
        },
        CharacteristicColumnInteger(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        None,
        True,
        "provided value non-valid-integer-value in column column_name can not be interpreted as integer characteristic",  # noqa: E501
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
def test_characteristic_column_integer(
    data: dict[str | int, Any],
    column: CharacteristicColumnInteger,
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
