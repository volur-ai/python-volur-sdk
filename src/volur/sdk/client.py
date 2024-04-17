import asyncio
from dataclasses import dataclass, field

from loguru import logger
from volur.api.client import VolurApiAsyncClient
from volur.sdk.sources.csv.base import MaterialsSource, ProductSource


@dataclass
class VolurClient:
    """Client to interact with Völur platform.

    This client helps to upload various data sources to the Völur system from different
    sources using the Völur API.

    See the list of available methods to use.

    Examples:
        ```python title="example_material.py" linenums=1
        client = VolurClient()
        source = MaterialsCSVFileAsyncSource(
            "materials.csv",
            material_id_column=Column(
                "material_id",
            ),
        )
        client.upload_materials_information(source)
        ```

         ```python title="example_product.py" linenums=1
        client = VolurClient()
        source = ProductCSVFileAsyncSource(
            "product.csv",
            product_id_column=Column(
                "product_id",
            ),
        )
        client.upload_product_information(source)
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
        logger.info("successfully uploaded materials information")

    def upload_product_information(
        self: "VolurClient",
        product: ProductSource,
    ) -> None:
        result = asyncio.run(
            self.api.upload_product_information(product),
            debug=self.api.settings.debug,
        )
        if result.code != 0:
            logger.error(
                "error occurred while uploading product information",
                response_status_code=result.code,
                response_status_message=result.message,
            )
        logger.info("successfully uploaded product information")
