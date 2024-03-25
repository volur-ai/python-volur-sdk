"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import google.rpc.status_pb2
import google.type.money_pb2
import typing
import volur.pork.demand.v1alpha1.characteristic_pb2
import volur.pork.products.v1alpha1.product_pb2
import volur.pork.shared.v1alpha1.quantity_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Demand(google.protobuf.message.Message):
    """Individual product of a list of products and their quantities that need to be
    delivered from a plant to a customer at a give date for a given price.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PRODUCT_FIELD_NUMBER: builtins.int
    PLANT_FIELD_NUMBER: builtins.int
    CUSTOMER_ID_FIELD_NUMBER: builtins.int
    QUANTITY_FIELD_NUMBER: builtins.int
    DISPATCH_AT_FIELD_NUMBER: builtins.int
    DEMAND_ON_FIELD_NUMBER: builtins.int
    PRICE_PER_UNIT_FIELD_NUMBER: builtins.int
    CHARACTERISTICS_FIELD_NUMBER: builtins.int
    plant: builtins.str
    """Identifier of the plant or facility where the demand is shipped from."""
    customer_id: builtins.str
    """A unique identifier for the customer."""
    @property
    def product(self) -> volur.pork.products.v1alpha1.product_pb2.Product:
        """Reference to product (can't only reference the id)."""

    @property
    def quantity(self) -> volur.pork.shared.v1alpha1.quantity_pb2.Quantity:
        """The amount of this demand."""

    @property
    def dispatch_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """The timestamp indicating when the demand should leave the facility (deadline)."""

    @property
    def demand_on(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Expected time of arrival of the demand at the customer's location."""

    @property
    def price_per_unit(self) -> google.type.money_pb2.Money:
        """Value representing the price per unit and currency of the product to deliver."""

    @property
    def characteristics(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[volur.pork.demand.v1alpha1.characteristic_pb2.Characteristic]:
        """A list of additional characteristics that further describe the demand (sale) of a product."""

    def __init__(
        self,
        *,
        product: volur.pork.products.v1alpha1.product_pb2.Product | None = ...,
        plant: builtins.str = ...,
        customer_id: builtins.str = ...,
        quantity: volur.pork.shared.v1alpha1.quantity_pb2.Quantity | None = ...,
        dispatch_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        demand_on: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        price_per_unit: google.type.money_pb2.Money | None = ...,
        characteristics: collections.abc.Iterable[volur.pork.demand.v1alpha1.characteristic_pb2.Characteristic] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["demand_on", b"demand_on", "dispatch_at", b"dispatch_at", "price_per_unit", b"price_per_unit", "product", b"product", "quantity", b"quantity"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["characteristics", b"characteristics", "customer_id", b"customer_id", "demand_on", b"demand_on", "dispatch_at", b"dispatch_at", "plant", b"plant", "price_per_unit", b"price_per_unit", "product", b"product", "quantity", b"quantity"]) -> None: ...

global___Demand = Demand

@typing.final
class UploadDemandInformationRequest(google.protobuf.message.Message):
    """Message representing a request to upload the demand of a product.
    It contains the demand of a product to be uploaded.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DEMAND_FIELD_NUMBER: builtins.int
    @property
    def demand(self) -> global___Demand:
        """The demand of a product to be uploaded."""

    def __init__(
        self,
        *,
        demand: global___Demand | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["demand", b"demand"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["demand", b"demand"]) -> None: ...

global___UploadDemandInformationRequest = UploadDemandInformationRequest

@typing.final
class UploadDemandInformationResponse(google.protobuf.message.Message):
    """Message representing a response from an attempt to upload the demand of a product.
    Contains a message describing the result of the demand upload operation
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STATUS_FIELD_NUMBER: builtins.int
    @property
    def status(self) -> google.rpc.status_pb2.Status:
        """The status of demand upload, including any messages or errors."""

    def __init__(
        self,
        *,
        status: google.rpc.status_pb2.Status | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["status", b"status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["status", b"status"]) -> None: ...

global___UploadDemandInformationResponse = UploadDemandInformationResponse

@typing.final
class DemandUploadStatus(google.protobuf.message.Message):
    """Contains a message describing the result of the demand upload operation,
    which could be success or error.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    MESSAGE_FIELD_NUMBER: builtins.int
    message: builtins.str
    """Message describing the status of the demand upload opearation."""
    def __init__(
        self,
        *,
        message: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["message", b"message"]) -> None: ...

global___DemandUploadStatus = DemandUploadStatus
