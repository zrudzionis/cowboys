import logging
import sys
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from src.generated import service_discovery_pb2
from src.generated.service_discovery_pb2_grpc import add_ServiceDiscoveryServiceServicer_to_server
from src.service_discovery.service_discovery_service import ServiceDiscoveryServicer
from src import constants

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=constants.SERVICE_DISCOVERY_SERVER_MAX_THREADS)
    )
    add_ServiceDiscoveryServiceServicer_to_server(ServiceDiscoveryServicer(), server)

    # the reflection service will be aware of
    # "ServiceDiscoveryService" and "ServerReflection" services
    SERVICE_NAMES = (
        service_discovery_pb2.DESCRIPTOR.services_by_name["ServiceDiscoveryService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    LOGGER.info("Reflections enabled.")

    server_port = constants.SERVICE_DISCOVERY_SERVER_PORT
    server.add_insecure_port(f"[::]:{server_port}")
    LOGGER.info(f"Server started on port: {server_port}...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
