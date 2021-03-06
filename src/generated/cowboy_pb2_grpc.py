# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.generated.cowboy_pb2 as cowboy__pb2
import src.generated.shared_pb2 as shared__pb2


class CowboyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getCowboy = channel.unary_unary(
                '/CowboyService/getCowboy',
                request_serializer=shared__pb2.Void.SerializeToString,
                response_deserializer=cowboy__pb2.Cowboy.FromString,
                )
        self.setCowboy = channel.unary_unary(
                '/CowboyService/setCowboy',
                request_serializer=cowboy__pb2.Cowboy.SerializeToString,
                response_deserializer=cowboy__pb2.Response.FromString,
                )
        self.setTargetCowboys = channel.unary_unary(
                '/CowboyService/setTargetCowboys',
                request_serializer=cowboy__pb2.TargetCowboys.SerializeToString,
                response_deserializer=cowboy__pb2.Response.FromString,
                )
        self.giveDamage = channel.unary_unary(
                '/CowboyService/giveDamage',
                request_serializer=shared__pb2.Void.SerializeToString,
                response_deserializer=cowboy__pb2.Response.FromString,
                )
        self.takeDamage = channel.unary_unary(
                '/CowboyService/takeDamage',
                request_serializer=cowboy__pb2.Shooter.SerializeToString,
                response_deserializer=cowboy__pb2.Response.FromString,
                )


class CowboyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getCowboy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setCowboy(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setTargetCowboys(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def giveDamage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def takeDamage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CowboyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getCowboy': grpc.unary_unary_rpc_method_handler(
                    servicer.getCowboy,
                    request_deserializer=shared__pb2.Void.FromString,
                    response_serializer=cowboy__pb2.Cowboy.SerializeToString,
            ),
            'setCowboy': grpc.unary_unary_rpc_method_handler(
                    servicer.setCowboy,
                    request_deserializer=cowboy__pb2.Cowboy.FromString,
                    response_serializer=cowboy__pb2.Response.SerializeToString,
            ),
            'setTargetCowboys': grpc.unary_unary_rpc_method_handler(
                    servicer.setTargetCowboys,
                    request_deserializer=cowboy__pb2.TargetCowboys.FromString,
                    response_serializer=cowboy__pb2.Response.SerializeToString,
            ),
            'giveDamage': grpc.unary_unary_rpc_method_handler(
                    servicer.giveDamage,
                    request_deserializer=shared__pb2.Void.FromString,
                    response_serializer=cowboy__pb2.Response.SerializeToString,
            ),
            'takeDamage': grpc.unary_unary_rpc_method_handler(
                    servicer.takeDamage,
                    request_deserializer=cowboy__pb2.Shooter.FromString,
                    response_serializer=cowboy__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'CowboyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CowboyService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getCowboy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CowboyService/getCowboy',
            shared__pb2.Void.SerializeToString,
            cowboy__pb2.Cowboy.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def setCowboy(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CowboyService/setCowboy',
            cowboy__pb2.Cowboy.SerializeToString,
            cowboy__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def setTargetCowboys(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CowboyService/setTargetCowboys',
            cowboy__pb2.TargetCowboys.SerializeToString,
            cowboy__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def giveDamage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CowboyService/giveDamage',
            shared__pb2.Void.SerializeToString,
            cowboy__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def takeDamage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/CowboyService/takeDamage',
            cowboy__pb2.Shooter.SerializeToString,
            cowboy__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
