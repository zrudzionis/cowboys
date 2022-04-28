import logging
from typing import List

from src.generated.shared_pb2 import Void
from src.generated.service_discovery_pb2 import ServiceNodes, ServiceNode
from src.generated.service_discovery_pb2_grpc import ServiceDiscoveryServiceServicer
from src.protobuf_utils import protobuf_to_dict

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class ServiceDiscoveryServicer(ServiceDiscoveryServiceServicer):
    service_nodes: List[ServiceNode] = []

    def getRegistered(self, _, __):
        LOGGER.info("getRegistered returning: %s", self.service_nodes)
        return ServiceNodes(serviceNode=self.service_nodes)

    def register(self, request, _):
        LOGGER.info("Register receveid: %s", protobuf_to_dict(request))
        self.service_nodes.append(request)
        return Void()

    def clearRegistered(self, _, __):
        LOGGER.info("clearRegistered invoked")
        self.service_nodes = []
        return Void()
