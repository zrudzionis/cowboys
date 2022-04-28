
import logging
from typing import List

from grpc import insecure_channel

from src import constants
from src.generated.service_discovery_pb2 import ServiceNode
from src.generated.service_discovery_pb2_grpc import ServiceDiscoveryServiceStub
from src.generated.shared_pb2 import Void


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def register(service_address: str, service_name: str, ip: str, port: str):
    LOGGER.info("Client invoking service discovery: register")
    channel = insecure_channel(service_address)
    service_discovery_service = ServiceDiscoveryServiceStub(channel)
    service_discovery_service.register(
        ServiceNode(
            serviceName=service_name,
            ip=ip,
            port=port
        )
    )
    channel.close()


def get_registered(service_address: str) -> List[ServiceNode]:
    LOGGER.info("Client invoking service discovery: getRegistered")
    channel = insecure_channel(service_address)
    service_discovery_service = ServiceDiscoveryServiceStub(channel)
    response = service_discovery_service.getRegistered(Void())
    channel.close()
    return response.serviceNode
