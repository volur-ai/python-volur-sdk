from typing import Any

import pytest
from volur.pork.shared.v1alpha1 import characteristic_pb2
from volur.sdk.v1alpha2.sources.csv import CharacteristicColumnBool

create_characteristic_column_bool_test_ids = [
    "create-a-charachteristic-column-bool",
    "raise-exception-empty-string-column-name",
    "raise-exception-negative-column-index",
    "raise-exception-empty-string-characteristic-name",
]

create_characteristic_column_bool_test_data = [
    (
        "test-column-name",
        "test-characteristic-name",
        False,
        None,
    ),
    (
        "",
        "test-charactrestic-name",
        True,
        "column name can not be empty string",
    ),
    (
        -1,
        "test-characteristic-name",
        True,
        "column index must be equal or more than 0",
    ),
    (
        "test-column-name",
        "",
        True,
        "characteristic name can not be empty",
    ),
]


@pytest.mark.parametrize(
    argnames=[
        "column_name",
        "characteristic_name",
        "should_raise_an_exception",
        "exception_text",
    ],
    argvalues=create_characteristic_column_bool_test_data,
    ids=create_characteristic_column_bool_test_ids,
)
def test_create_characteristic_column_bool(
    column_name: str,
    characteristic_name: str,
    should_raise_an_exception: bool,
    exception_text: str | None,
) -> None:
    if should_raise_an_exception:
        with pytest.raises(ValueError, match=exception_text):
            CharacteristicColumnBool(
                column_name=column_name,
                characteristic_name=characteristic_name,
            )
    else:
        CharacteristicColumnBool(
            column_name=column_name,
            characteristic_name=characteristic_name,
        )


ids = [
    "return-correct-characteristic-for-a-correct-true-bool-value-in-column",
    "return-correct-characteristic-for-a-correct-false-bool-value-in-column",
    "return-correct-characteristic-for-a-correct-extended-true-bool-value-in-column",
    "return-correct-characteristic-for-a-correct-extended-false-bool-value-in-column",
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
        "provided value not-valid-bool-value in column column_name can not be interpreted as bool characteristic",  # noqa: E501
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
def test_characteristic_column_get_value(
    data: dict[str | int, Any],
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
