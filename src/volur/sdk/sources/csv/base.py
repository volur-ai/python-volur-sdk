"""A package that contains interfaces for sources."""

import abc
from typing import AsyncIterator

from volur.pork.materials.v1alpha3 import material_pb2
from volur.pork.products.v1alpha2 import product_pb2


class MaterialsSource:
    """
    Base class for the material sources.

    This class in an abstract class that defines the interface for the materials CSV
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


class ProductSource:
    """
    Base class for the product sources.

    This class in an abstract class that defines the interface for the products CSV
    source.
    """

    @abc.abstractmethod
    def __aiter__(self: "ProductSource") -> AsyncIterator[product_pb2.Product]:
        """ProductSource implements Asynchronous Iterator.

        This allows you to use any implementation of ProductSource as

        ```python title="example.py" linenums="1"
        source = ProductSourceImplementation()
        for _ in source:
            # do something with Product
        ```
        """
        ...

    @abc.abstractmethod
    async def __anext__(
        self: "ProductSource",
    ) -> product_pb2.Product:
        """You can fetch the next element in the asynchronous iterator."""
        ...
