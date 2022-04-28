import logging
import sys
from concurrent import futures

import grpc
from grpc_reflection.v1alpha import reflection

from src.generated import cowboy_pb2
from src.generated.cowboy_pb2_grpc import add_CowboyServiceServicer_to_server
from src.cowboy.cowboy_service import CowboyServiceServicer
from src import constants

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=constants.COWBOY_SERVER_MAX_THREADS)
    )
    add_CowboyServiceServicer_to_server(CowboyServiceServicer(), server)

    # the reflection service will be aware of
    # "CowboyService" and "ServerReflection" services
    SERVICE_NAMES = (
        cowboy_pb2.DESCRIPTOR.services_by_name["CowboyService"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    LOGGER.info("Reflections enabled.")

    server_port = constants.COWBOY_SERVER_PORT
    server.add_insecure_port(f"[::]:{server_port}")
    LOGGER.info(f"Server started on port: {server_port}...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
