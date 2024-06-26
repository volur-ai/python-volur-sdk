"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import abc
import collections.abc
import grpc
import grpc.aio
import typing
import volur.helloworld.v1beta1.hello_world_pb2

_T = typing.TypeVar("_T")

class _MaybeAsyncIterator(collections.abc.AsyncIterator[_T], collections.abc.Iterator[_T], metaclass=abc.ABCMeta): ...

class _ServicerContext(grpc.ServicerContext, grpc.aio.ServicerContext):  # type: ignore[misc, type-arg]
    ...

class GreeterServiceStub:
    def __init__(self, channel: typing.Union[grpc.Channel, grpc.aio.Channel]) -> None: ...
    SayHello: grpc.UnaryUnaryMultiCallable[
        volur.helloworld.v1beta1.hello_world_pb2.SayHelloRequest,
        volur.helloworld.v1beta1.hello_world_pb2.SayHelloResponse,
    ]

class GreeterServiceAsyncStub:
    SayHello: grpc.aio.UnaryUnaryMultiCallable[
        volur.helloworld.v1beta1.hello_world_pb2.SayHelloRequest,
        volur.helloworld.v1beta1.hello_world_pb2.SayHelloResponse,
    ]

class GreeterServiceServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def SayHello(
        self,
        request: volur.helloworld.v1beta1.hello_world_pb2.SayHelloRequest,
        context: _ServicerContext,
    ) -> typing.Union[volur.helloworld.v1beta1.hello_world_pb2.SayHelloResponse, collections.abc.Awaitable[volur.helloworld.v1beta1.hello_world_pb2.SayHelloResponse]]: ...

def add_GreeterServiceServicer_to_server(servicer: GreeterServiceServicer, server: typing.Union[grpc.Server, grpc.aio.Server]) -> None: ...
