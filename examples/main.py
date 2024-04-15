import sys

from loguru import logger
from volur.sdk.client import VolurClient
from volur.sdk.sources.csv import (
    CharacteristicColumn,
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
                CharacteristicColumn(
                    column_name="ARRIVED_AT",
                    characteristic_name="arrived_at",
                ),
                CharacteristicColumn(
                    column_name="PRODUCT_LABEL",
                    characteristic_name="product_label",
                    data_type="string",
                ),
                CharacteristicColumn(
                    column_name="QUALITY_CATEGORY",
                    characteristic_name="quality_category",
                    data_type="string",
                ),
                CharacteristicColumn(
                    column_name="SOME_DUMMY_BOOLEAN_VALUE",
                    characteristic_name="is_frozen",
                    data_type="bool",
                ),
            ],
        )
    )


if __name__ == "__main__":
    main()
