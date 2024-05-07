import sys

from loguru import logger
from volur.sdk.v1alpha2 import VolurClient
from volur.sdk.v1alpha2.sources.csv import (
    CharacteristicColumnString,
    CharacteristicColumnBool,
    Column,
    MaterialsCSVFileSource,
    QuantityColumn,
)

logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])


def main() -> None:
    client = VolurClient()
    logger.info("start uploading data to Snowflake")
    client.upload_materials_information(
        MaterialsCSVFileSource(
            path="data.csv",
            material_id_column=Column(column_name="MATERIAL_ID"),
            quantity_column=QuantityColumn(
                column_name="WEIGHT",
                unit="kilogram",
            ),
            characteristics_columns=[
                CharacteristicColumnString(
                    column_name="ARRIVED_AT",
                    characteristic_name="arrived_at",
                ),
                CharacteristicColumnString(
                    column_name="PRODUCT_LABEL",
                    characteristic_name="product_label",
                ),
                CharacteristicColumnString(
                    column_name="QUALITY_CATEGORY",
                    characteristic_name="quality_category",
                ),
                CharacteristicColumnBool(
                    column_name="SOME_DUMMY_BOOLEAN_VALUE",
                    characteristic_name="is_frozen",
                ),
            ],
        )
    )


if __name__ == "__main__":
    main()
