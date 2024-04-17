from dataclasses import dataclass, field
from typing import AsyncIterator

import grpc
from google.rpc.status_pb2 import Status
from loguru import logger
from volur.api.settings import VolurApiSettings
from volur.pork.materials.v1alpha3.material_pb2 import (
    UploadMaterialInformationRequest,
)
from volur.pork.materials.v1alpha3.material_pb2_grpc import (
    MaterialInformationServiceStub,
)
from volur.pork.products.v1alpha2.product_pb2 import (
    UploadProductInformationRequest,
)
from volur.pork.products.v1alpha2.product_pb2_grpc import (
    ProductInformationServiceStub,
)
from volur.sdk.sources.csv.base import MaterialsSource, ProductSource


@dataclass
class VolurApiAsyncClient:
    """A client for interacting with Völur API.

    This client is used to interact with the Völur API to upload data
    securely and effectively. See the actual methods for more details.

    Note:
        This client was not intended to be used directly, instead use the SDK client
        from [volur.sdk.client.VolurClient][volur.sdk.client].
    """

    settings: VolurApiSettings = field(default_factory=VolurApiSettings)

    async def upload_materials_information(
        self: "VolurApiAsyncClient",
        materials: MaterialsSource,
    ) -> Status:
        """Uploads Materials Information to the Völur platform using the Völur
        API.

        This method is using a source to get the materials data and then send
        it to the Völur API. This method is asynchronous and will return a
        status of the operation.

        Args:
            materials: a source of materials data to be uploaded to the Völur
                platform.

        Returns:
            The status of the operation.
        """

        async def generate_requests() -> (
            AsyncIterator[UploadMaterialInformationRequest]
        ):
            try:
                async for material in materials:
                    yield UploadMaterialInformationRequest(material=material)
            except Exception:
                logger.exception(
                    "error occurred while generating requests",
                )

        try:
            logger.info("start uploading materials data")
            channel = grpc.aio.secure_channel(
                self.settings.address,
                grpc.ssl_channel_credentials(),
            )
            stub = MaterialInformationServiceStub(channel)
            requests = generate_requests()
            stream = stub.UploadMaterialInformation(
                requests,  # type: ignore[arg-type]
                metadata=(
                    (
                        "authorization",
                        f"Bearer {self.settings.token.get_secret_value()}",
                    ),
                ),
            )
            while True:
                response = await stream.read()  # type: ignore[attr-defined]
                if response == grpc.aio.EOF:  # type: ignore[attr-defined]
                    logger.info("successfully uploaded materials information")
                    break
                if response.HasField("status"):
                    if response.status.code != 0:
                        logger.error(
                            f"error occurred while uploading materials information "
                            f"{response.status.code} {response.status.message}",
                        )
                    else:
                        logger.debug(
                            "successfully uploaded materials information",
                        )
                else:
                    raise ValueError("response from a server does not contain status")
            return Status(code=0)
        except grpc.aio.AioRpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.UNAUTHENTICATED:
                logger.error(
                    "used token in invalid,"
                    " please set a valid token using"
                    " `VOLUR_API_TOKEN` environment variable",
                )
            else:
                with logger.contextualize(
                    rpc_error_code=rpc_error.code(),
                    rpc_error_details=rpc_error.details(),
                ):
                    logger.exception(
                        "error occurred while uploading materials information",
                    )
            code: int
            code, _ = rpc_error.code().value  # type: ignore[misc]
            message = _ if (_ := rpc_error.details()) else ""
            return Status(
                code=code,
                message=message,
            )

    async def upload_product_information(
        self: "VolurApiAsyncClient",
        products: ProductSource,
    ) -> Status:
        """Uploads Product Information to the Völur platform using the Völur
        API.

        This method is using a source to get the product data and then send
        it to the Völur API. This method is asynchronous and will return a
        status of the operation.

        Args:
            products: a source of product data to be uploaded to the Völur
                platform.

        Returns:
            The status of the operation.
        """

        async def generate_requests() -> AsyncIterator[UploadProductInformationRequest]:
            try:
                async for product in products:
                    yield UploadProductInformationRequest(product=product)
            except Exception:
                logger.exception(
                    "error occurred while generating requests",
                )

        try:
            logger.info("start uploading product data")
            channel = grpc.aio.secure_channel(
                self.settings.address,
                grpc.ssl_channel_credentials(),
            )
            stub = ProductInformationServiceStub(channel)
            requests = generate_requests()
            stream = stub.UploadProductInformation(
                requests,  # type: ignore[arg-type]
                metadata=(
                    (
                        "authorization",
                        f"Bearer {self.settings.token.get_secret_value()}",
                    ),
                ),
            )
            while True:
                response = await stream.read()  # type: ignore[attr-defined]
                if response == grpc.aio.EOF:  # type: ignore[attr-defined]
                    logger.info("successfully uploaded product information")
                    break
                if response.HasField("status"):
                    if response.status.code != 0:
                        logger.error(
                            f"error occurred while uploading product information "
                            f"{response.status.code} {response.status.message}",
                        )
                    else:
                        logger.debug(
                            "successfully uploaded product information",
                        )
                else:
                    raise ValueError("response from a server does not contain status")
            return Status(code=0)
        except grpc.aio.AioRpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.UNAUTHENTICATED:
                logger.error(
                    "used token in invalid,"
                    " please set a valid token using"
                    " `VOLUR_API_TOKEN` environment variable",
                )
            else:
                with logger.contextualize(
                    rpc_error_code=rpc_error.code(),
                    rpc_error_details=rpc_error.details(),
                ):
                    logger.exception(
                        "error occurred while uploading product information",
                    )
            code: int
            code, _ = rpc_error.code().value  # type: ignore[misc]
            message = _ if (_ := rpc_error.details()) else ""
            return Status(
                code=code,
                message=message,
            )
