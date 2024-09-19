from typing import Any

import pytest

from volur.pork.shared.v1alpha1 import characteristic_pb2
from volur.sdk.v1alpha2.sources.csv import CharacteristicColumnFloat

ids = [
    "return-correct-characteristic-for-a-correct-float-value-in-column",
    "return-empty-characteristic-because-value-in-column-is-none",
    "raise-exception-because-value-is-not-valid-float",
]

test_data = [
    (
        {
            "column_name": "1.234",
        },
        CharacteristicColumnFloat(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_float=1.234,
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "",
        },
        CharacteristicColumnFloat(
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
            "column_name": "non-valid-float-value",
        },
        CharacteristicColumnFloat(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        None,
        True,
        "provided value non-valid-float-value in column column_name can not be interpreted as float characteristic",  # noqa: E501
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
def test_characteristic_column_float(
    data: dict[str | int, Any],
    column: CharacteristicColumnFloat,
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
