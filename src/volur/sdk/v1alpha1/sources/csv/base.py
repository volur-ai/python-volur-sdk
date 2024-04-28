"""A package that contains interfaces for sources."""

import abc
from typing import AsyncIterator

from volur.pork.materials.v1alpha3 import material_pb2


class MaterialsSource:
    """
    Base class for material sources.

    This class in an abstract class that defines the interface for materials CSV
    source.
    """

    @abc.abstractmethod
    def __aiter__(self: "MaterialsSource") -> AsyncIterator[material_pb2.Material]:
        """MaterialSource implements Asynchronous Iterator.

        This allows you to use any implementation of MaterialSource as

        ```python title="example.py" linenums="1"
        source = MaterialSourceImplementation()
        for _ in source:
            # do something with Material
        ```
        """
        ...

    @abc.abstractmethod
    async def __anext__(
        self: "MaterialsSource",
    ) -> material_pb2.Material:
        """You can fetch the next element in the asynchronous iterator."""
        ...
