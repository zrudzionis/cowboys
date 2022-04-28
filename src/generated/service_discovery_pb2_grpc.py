# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.generated.service_discovery_pb2 as service__discovery__pb2
import src.generated.shared_pb2 as shared__pb2


class ServiceDiscoveryServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getRegistered = channel.unary_unary(
                '/ServiceDiscoveryService/getRegistered',
                request_serializer=shared__pb2.Void.SerializeToString,
                response_deserializer=service__discovery__pb2.ServiceNodes.FromString,
                )
        self.register = channel.unary_unary(
                '/ServiceDiscoveryService/register',
                request_serializer=service__discovery__pb2.ServiceNode.SerializeToString,
                response_deserializer=shared__pb2.Void.FromString,
                )
        self.clearRegistered = channel.unary_unary(
                '/ServiceDiscoveryService/clearRegistered',
                request_serializer=shared__pb2.Void.SerializeToString,
                response_deserializer=shared__pb2.Void.FromString,
                )


class ServiceDiscoveryServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getRegistered(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def clearRegistered(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServiceDiscoveryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getRegistered': grpc.unary_unary_rpc_method_handler(
                    servicer.getRegistered,
                    request_deserializer=shared__pb2.Void.FromString,
                    response_serializer=service__discovery__pb2.ServiceNodes.SerializeToString,
            ),
            'register': grpc.unary_unary_rpc_method_handler(
                    servicer.register,
                    request_deserializer=service__discovery__pb2.ServiceNode.FromString,
                    response_serializer=shared__pb2.Void.SerializeToString,
            ),
            'clearRegistered': grpc.unary_unary_rpc_method_handler(
                    servicer.clearRegistered,
                    request_deserializer=shared__pb2.Void.FromString,
                    response_serializer=shared__pb2.Void.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ServiceDiscoveryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ServiceDiscoveryService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getRegistered(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ServiceDiscoveryService/getRegistered',
            shared__pb2.Void.SerializeToString,
            service__discovery__pb2.ServiceNodes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ServiceDiscoveryService/register',
            service__discovery__pb2.ServiceNode.SerializeToString,
            shared__pb2.Void.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def clearRegistered(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ServiceDiscoveryService/clearRegistered',
            shared__pb2.Void.SerializeToString,
            shared__pb2.Void.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
