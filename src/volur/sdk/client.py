from dataclasses import dataclass
from typing import Dict, Iterator, List, Union

import grpc
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from volur.pork.materials.v1alpha3 import material_pb2, material_pb2_grpc
from volur.sdk.sources.csv.base import MaterialSource


class VolurClientSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="VOLUR_",
    )
    auth_token: str | None


@dataclass
class VolurClient:
    def __init__(
        self: "VolurClient",
        auth_token: str | None = None,
        host: str = "localhost",
        port: int = 50051,
    ) -> None:
        try:
            settings = VolurClientSettings()
            self.metadata = (("authorization", f"Bearer {settings.auth_token}"),)
        except ValidationError as exc:
            if not auth_token:
                raise ValueError(
                    "Set VOLUR_AUTH_TOKEN variable or pass auth_token."
                ) from exc
            else:
                self.metadata = (("authorization", f"Bearer {auth_token}"),)
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.material_stub = material_pb2_grpc.MaterialInformationServiceStub(
            self.channel
        )

    def upload_materials(
        self: "VolurClient", source: MaterialSource
    ) -> Iterator[
        Dict[str, Union[str, List[material_pb2.UploadMaterialInformationResponse]]]
    ]:
        def generate_requests(
            materials: MaterialSource,
        ) -> Iterator[material_pb2.UploadMaterialInformationRequest]:
            for material in materials:
                yield material_pb2.UploadMaterialInformationRequest(material=material)

        responses = []

        for response in self.material_stub.UploadMaterialInformation(
            generate_requests(source), metadata=self.metadata
        ):
            responses.append(response)

        if responses:
            yield {
                "status": f"Successfully uploaded {len(responses)} materials.",
                "responses": responses,
            }
        else:
            yield {"status": "No materials were uploaded.", "responses": responses}
