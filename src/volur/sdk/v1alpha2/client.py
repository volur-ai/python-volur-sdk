import asyncio
from dataclasses import dataclass, field

from loguru import logger
from volur.api.v1alpha1.client import VolurApiAsyncClient
from volur.sdk.v1alpha2.sources import MaterialsSource, ProductsSource


@dataclass
class VolurClient:
    """Client to interact with Völur platform.

    This client helps to upload various data to Völur API from different
    sources.

    See the list of available methods to use.

    Example:
        ```python title="example.py" linenums=1
        client = VolurClient()
        source = MaterialsCSVFileAsyncSource(
            "materials.csv",
            material_id_column=Column(
                "material_id",
            ),
        )
        client.upload_materials_information(source)
        ```
    """

    api: VolurApiAsyncClient = field(default_factory=VolurApiAsyncClient)

    def upload_materials_information(
        self: "VolurClient",
        materials: MaterialsSource,
    ) -> None:
        result = asyncio.run(
            self.api.upload_materials_information(materials),
            debug=self.api.settings.debug,
        )
        if result.code != 0:
            logger.error(
                "error occurred while uploading materials information",
                response_status_code=result.code,
                response_status_message=result.message,
            )

    def upload_products_information(
        self: "VolurClient",
        products: ProductsSource,
    ) -> None:
        result = asyncio.run(
            self.api.upload_products_information(products),
            debug=self.api.settings.debug,
        )
        if result.code != 0:
            logger.error(
                "error occurred while uploading products information",
                response_status_code=result.code,
                response_status_message=result.message,
            )
        logger.info("successfully uploaded products information")
