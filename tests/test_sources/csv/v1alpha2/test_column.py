import pytest
from volur.sdk.v1alpha2.sources.csv import Column

test_ids = [
    "pass-with-a-column-name",
    "pass-with-an-index",
    "raise-exception-empty-string-column-name",
    "raise-exception-negative-column-index",
]

test_data = [
    (
        "test-column-name",
        False,
        None,
    ),
    (
        0,
        False,
        None,
    ),
    (
        "",
        True,
        "column name can not be empty string",
    ),
    (
        -1,
        True,
        "column index must be equal or more than 0",
    ),
]


@pytest.mark.parametrize(
    argnames=[
        "column_name",
        "should_raise_an_exception",
        "exception_text",
    ],
    argvalues=test_data,
    ids=test_ids,
)
def test_create_column(
    column_name: str | int,
    should_raise_an_exception: bool,
    exception_text: str | None,
) -> None:
    if should_raise_an_exception:
        with pytest.raises(ValueError, match=exception_text):
            Column(column_name=column_name)
    else:
        Column(column_name=column_name)
