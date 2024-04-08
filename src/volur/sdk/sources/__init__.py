import abc
from typing import AsyncIterator, Coroutine, Iterator

from pydantic import BaseModel
from volur.pork.materials.v1alpha3 import material_pb2


class MaterialSource(BaseModel):
    @abc.abstractmethod
    def __iter__(self: "MaterialSource") -> Iterator[material_pb2.Material]: ...  # type: ignore[override]

    @abc.abstractmethod
    def __next__(self: "MaterialSource") -> material_pb2.Material: ...

    @abc.abstractmethod
    def __aiter__(self: "MaterialSource") -> AsyncIterator[material_pb2.Material]: ...
    @abc.abstractmethod
    def __anext__(
        self: "MaterialSource",
    ) -> Coroutine[None, None, material_pb2.Material]: ...
