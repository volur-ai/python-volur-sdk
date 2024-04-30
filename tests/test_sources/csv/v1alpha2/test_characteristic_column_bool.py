from typing import Any

import pytest
from volur.pork.shared.v1alpha1 import characteristic_pb2
from volur.sdk.v1alpha2.sources.csv.base import CharacteristicColumnBool

ids = [
    "return-correct-characteristic-for-a-correct-true-bool-value-in-column",
    "return-correct-characteristic-for-a-correct-false-bool-value-in-column",
    "return-correct-characteristic-for-a-correct-extended-true-bool-value-in-column",
    "return-correct-characteristic-for-a-correct-extended-false-bool-value-in-column",
    "return-empty-chracteristic-because-value-in-column-is-none",
    "raise-exception-column-does-not-exist",
    "raise-exception-because-value-is-not-valid-bool",
]

test_data = [
    (
        {
            "column_name": "True",
        },
        CharacteristicColumnBool(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_bool=True,
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "False",
        },
        CharacteristicColumnBool(
            column_name="column_name",
            characteristic_name="characteristic_name",
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_bool=False,
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "yes",
        },
        CharacteristicColumnBool(
            column_name="column_name",
            characteristic_name="characteristic_name",
            extra_values_true=[
                "yes",
            ],
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_bool=True,
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "no",
        },
        CharacteristicColumnBool(
            column_name="column_name",
            characteristic_name="characteristic_name",
            extra_values_false=[
                "no",
            ],
        ),
        characteristic_pb2.Characteristic(
            name="characteristic_name",
            value=characteristic_pb2.CharacteristicValue(
                value_bool=False,
            ),
        ),
        False,
        None,
    ),
    (
        {
            "column_name": "",
        },
        CharacteristicColumnBool(
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
            "column_name": "True",
        },
        CharacteristicColumnBool(
            column_name="column_name_does_not_exist",
            characteristic_name="characteristic_name",
        ),
        None,
        True,
        "can not fetch the bool characteristic column with name column_name_does_not_exist",  # noqa: E501
    ),
    (
        {
            "column_name": "not-valid-bool-value",
        },
        CharacteristicColumnBool(
            column_name="column_name",
            characteristic_name="characteristic_name",
            extra_values_true=[
                "yes",
            ],
            extra_values_false=[
                "no",
            ],
        ),
        None,
        True,
        "can not parse value not-valid-bool-value in column column_name as bool value",
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
    column: CharacteristicColumnBool,
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
