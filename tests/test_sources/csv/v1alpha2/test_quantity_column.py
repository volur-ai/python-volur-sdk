from typing import Any, Literal

import pytest

from volur.pork.shared.v1alpha1 import quantity_pb2
from volur.sdk.v1alpha2.sources.csv import QuantityColumn

create_quantity_column_test_ids = [
    "create-quantity-column-with-name",
    "create-quantity-column-with-index",
    "raise-exception-empty-string-column-name",
    "raise-exception-negative-column-index",
    "raise-exception-empty-unit",
]

create_quantity_column_test_data = [
    (
        "test-column-id",
        "kilogram",
        False,
        None,
    ),
    (
        0,
        "kilogram",
        False,
        None,
    ),
    (
        "",
        "kilogram",
        True,
        "column name can not be empty string",
    ),
    (
        -1,
        "kilogram",
        True,
        "column index must be equal or more than 0",
    ),
    (
        0,
        "",
        True,
        "unit can not be empty string",
    ),
]


@pytest.mark.parametrize(
    argnames=[
        "column_name",
        "unit",
        "should_raise_an_exception",
        "exception_text",
    ],
    argvalues=create_quantity_column_test_data,
    ids=create_quantity_column_test_ids,
)
def test_create_quantity_column(
    column_name: str | int,
    unit: Literal["kilogram", "pound", "box", "piece"],
    should_raise_an_exception: bool,
    exception_text: str | None,
) -> None:
    if should_raise_an_exception:
        with pytest.raises(ValueError, match=exception_text):
            QuantityColumn(column_name=column_name, unit=unit)
    else:
        QuantityColumn(column_name=column_name, unit=unit)


quantity_column_get_value_test_ids = [
    "raise-exception-provided-value-can-not-be-interpreted-kilogram",
    "raise-exception-provided-value-can-not-be-interpreted-pound",
    "raise-exception-provided-value-can-not-be-interpreted-box",
    "raise-exception-provided-value-can-not-be-interpreted-piece",
    "return-a-quantity-column-kilogram",
    "return-a-quantity-column-pound",
    "return-a-quantity-column-box",
    "return-a-quantity-column-piece",
]

quantity_column_get_value_test_data = [
    (
        QuantityColumn(
            column_name="test-column-name",
            unit="kilogram",
        ),
        {
            "test-column-name": "non-valid-kilogram-value",
        },
        None,
        True,
        "provided value non-valid-kilogram-value in column test-column-name can not be interpreted as kilogram",  # noqa: E501
    ),
    (
        QuantityColumn(
            column_name="test-column-name",
            unit="pound",
        ),
        {
            "test-column-name": "non-valid-pound-value",
        },
        None,
        True,
        "provided value non-valid-pound-value in column test-column-name can not be interpreted as pound",  # noqa: E501
    ),
    (
        QuantityColumn(
            column_name="test-column-name",
            unit="box",
        ),
        {
            "test-column-name": "non-valid-box-value",
        },
        None,
        True,
        "provided value non-valid-box-value in column test-column-name can not be interpreted as box",  # noqa: E501
    ),
    (
        QuantityColumn(
            column_name="test-column-name",
            unit="piece",
        ),
        {
            "test-column-name": "non-valid-piece-value",
        },
        None,
        True,
        "provided value non-valid-piece-value in column test-column-name can not be interpreted as piece",  # noqa: E501
    ),
    (
        QuantityColumn(
            column_name="test-column-name",
            unit="kilogram",
        ),
        {
            "test-column-name": 1.0,
        },
        quantity_pb2.Quantity(
            value=quantity_pb2.QuantityValue(
                kilogram=1.0,
            )
        ),
        False,
        None,
    ),
    (
        QuantityColumn(
            column_name="test-column-name",
            unit="pound",
        ),
        {
            "test-column-name": 1.0,
        },
        quantity_pb2.Quantity(
            value=quantity_pb2.QuantityValue(
                pound=1.0,
            )
        ),
        False,
        None,
    ),
    (
        QuantityColumn(
            column_name="test-column-name",
            unit="box",
        ),
        {
            "test-column-name": 1,
        },
        quantity_pb2.Quantity(
            value=quantity_pb2.QuantityValue(
                box=1,
            )
        ),
        False,
        None,
    ),
    (
        QuantityColumn(
            column_name="test-column-name",
            unit="piece",
        ),
        {
            "test-column-name": 1.0,
        },
        quantity_pb2.Quantity(
            value=quantity_pb2.QuantityValue(
                piece=1,
            )
        ),
        False,
        None,
    ),
]


@pytest.mark.parametrize(
    argnames=[
        "column",
        "data",
        "expected",
        "should_raise_an_exception",
        "exception_text",
    ],
    argvalues=quantity_column_get_value_test_data,
    ids=quantity_column_get_value_test_ids,
)
def test_quantity_column_get_value(
    column: QuantityColumn,
    data: dict[str | int, Any],
    expected: quantity_pb2.Quantity | None,
    should_raise_an_exception: bool,
    exception_text: str | None,
) -> None:
    if should_raise_an_exception:
        with pytest.raises(ValueError, match=exception_text):
            column.get_value(data)
    else:
        actual = column.get_value(data)
        assert actual == expected
