import logging

from azure.functions import FunctionApp, InputStream
from volur.sdk.client import VolurClient
from volur.sdk.sources.csv import (
    CharacteristicColumn,
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
