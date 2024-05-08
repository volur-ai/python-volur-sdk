import logging

from azure.functions import FunctionApp, InputStream
from volur.sdk.v1alpha2 import VolurClient
from volur.sdk.v1alpha2.sources.csv import (
    CharacteristicColumnBool,
    CharacteristicColumnString,
    Column,
    MaterialsCSVFileSource,
    QuantityColumn,
)

app = FunctionApp()


@app.function_name(name="demo-volur-ai-sdk-azure-function")
@app.blob_trigger(
    arg_name="source",
    path="test-container/{name}",
    connection="AzureWebJobsStorage",
)
def run(source: InputStream) -> None:
    logging.info(f"trigerred a function by a blob {source.name}")
    client = VolurClient()
    client.upload_materials_information(
        MaterialsCSVFileSource(
            path=source,
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
