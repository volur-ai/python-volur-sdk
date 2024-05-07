from dataclasses import dataclass, field
from typing import AsyncIterator

import grpc
from google.rpc.status_pb2 import Status
from loguru import logger
from volur.api.v1alpha1.settings import VolurApiSettings
from volur.pork.materials.v1alpha3 import material_pb2, material_pb2_grpc


@dataclass
class VolurApiAsyncClient:
    """A client for interacting with Völur API.

    This client is used to interact with the Völur API to upload the data
    securely and effectively. See the actual methods for more details.

    Note:
        This client was not intended to be used directly, instead use the SDK client
        from [volur.sdk.client.VolurClient][volur.sdk.client].
    """

    settings: VolurApiSettings = field(default_factory=VolurApiSettings)

    async def upload_materials_information(
        self: "VolurApiAsyncClient",
        materials: AsyncIterator[material_pb2.Material],
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
            AsyncIterator[material_pb2.UploadMaterialInformationRequest]
        ):
            try:
                async for material in materials:
                    yield material_pb2.UploadMaterialInformationRequest(
                        material=material,
                    )
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
            stub = material_pb2_grpc.MaterialInformationServiceStub(channel)
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