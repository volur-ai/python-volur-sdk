import asyncio
from dataclasses import dataclass, field

from loguru import logger
from volur.api.client import VolurApiAsyncClient
from volur.sdk.sources.csv.base import MaterialSource


@dataclass
class VolurClient:
    api: VolurApiAsyncClient = field(default_factory=VolurApiAsyncClient)

    def upload_materials_information(
        self: "VolurClient",
        materials: MaterialSource,
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
