# type: ignore
from typing import Any, AsyncIterator, Dict, Iterator

import google.rpc.status_pb2
import grpc
import pytest
from pydantic import ConfigDict, Field
from volur.pork.materials.v1alpha3 import material_pb2
from volur.sdk.client import VolurClient
from volur.sdk.sources.csv.base import MaterialSource


class UploadMaterialInformationStub:
    def __init__(self: grpc.StreamStreamMultiCallable, unauthenticated: bool) -> None:
        self.unauthenticated = unauthenticated

    def __call__(
        self: grpc.StreamStreamMultiCallable,
        request_iterator: Iterator[material_pb2.UploadMaterialInformationRequest],
        timeout: int | None = None,
        metadata: tuple[tuple[str, str | bytes], ...] | None = None,
        credentials: grpc.CallCredentials | None = None,
        wait_for_ready: bool | None = None,
        compression: grpc.Compression.NoCompression
        | grpc.Compression.Deflate
        | grpc.Compression.Gzip = None,
    ) -> Iterator[material_pb2.UploadMaterialInformationResponse]:
        if self.unauthenticated:
            raise grpc.RpcError("UNAUTHENTICATED")
        for _ in request_iterator:
            yield material_pb2.UploadMaterialInformationResponse(
                status=google.rpc.status_pb2.Status(code=200)
            )


class FakeMaterialsCSVFileSource(MaterialSource):
    def __aiter__(self: "MaterialSource") -> AsyncIterator[material_pb2.Material]: ...

    async def __anext__(self: "MaterialSource") -> material_pb2.Material: ...

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    data: list[material_pb2.Material] = Field(
        default_factory=list,
    )

    def __iter__(self: "FakeMaterialsCSVFileSource") -> Iterator[material_pb2.Material]:
        return self

    def __next__(self: "FakeMaterialsCSVFileSource") -> material_pb2.Material:
        if self.data:
            return self.data.pop(0)
        else:
            raise StopIteration


@pytest.fixture()
def materials() -> list[material_pb2.Material]:
    return [
        material_pb2.Material(material_id="1", plant="Plant1"),
        material_pb2.Material(material_id="2", plant="Plant1"),
        material_pb2.Material(material_id="3", plant="Plant1"),
        material_pb2.Material(material_id="4", plant="Plant2"),
        material_pb2.Material(material_id="5", plant="Plant3"),
    ]


@pytest.fixture()
def client() -> VolurClient:
    client = VolurClient(auth_token="Test")
    upload_material_information = UploadMaterialInformationStub(unauthenticated=False)
    client.material_stub.UploadMaterialInformation = upload_material_information
    return client


@pytest.fixture()
def expected_response() -> Dict[str, Any]:
    return {
        "status": "Successfully uploaded 5 materials.",
        "responses": [
            material_pb2.UploadMaterialInformationResponse(
                status=google.rpc.status_pb2.Status(code=200)
            )
            for _ in range(5)
        ],
    }


def test_upload_materials(
    client: VolurClient,
    materials: list[material_pb2.Material],
    expected_response: Dict[str, Any],
) -> None:
    source = FakeMaterialsCSVFileSource(data=materials)
    response_generator = client.upload_materials(source)
    response = next(response_generator, None)  # Get the first (and only) response

    assert response is not None
    assert response["status"] == expected_response["status"]
    assert len(response["responses"]) == len(expected_response["responses"])


@pytest.fixture()
def expected_empty_response() -> Dict[str, Any]:
    return {
        "status": "No materials were uploaded.",
        "responses": [],
    }


def test_upload_no_materials(
    client: VolurClient, expected_empty_response: Dict[str, Any]
) -> None:
    source = FakeMaterialsCSVFileSource(data=[])
    response_generator = client.upload_materials(source)
    response = next(response_generator, None)  # Get the first (and only) response

    assert response is not None
    assert response["status"] == expected_empty_response["status"]
    assert len(response["responses"]) == len(expected_empty_response["responses"])


@pytest.fixture()
def client_unauth() -> VolurClient:
    client_unauth = VolurClient(auth_token="Test")
    upload_material_information_unauth = UploadMaterialInformationStub(
        unauthenticated=True
    )
    client_unauth.material_stub.UploadMaterialInformation = (
        upload_material_information_unauth
    )
    return client_unauth


def test_client_wrong_auth(client_unauth: VolurClient) -> None:
    source = FakeMaterialsCSVFileSource()
    response_generator = client_unauth.upload_materials(source)
    with pytest.raises(grpc.RpcError, match="UNAUTHENTICATED"):
        next(response_generator, None)


def test_client_no_token() -> None:
    with pytest.raises(
        ValueError, match="Set VOLUR_AUTH_TOKEN variable or pass auth_token."
    ):
        VolurClient()
