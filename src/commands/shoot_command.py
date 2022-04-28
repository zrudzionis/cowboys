import logging
import os
from typing import Dict, List, Tuple

from src import constants
from src.commands.command_utils import get_cowboys
from src.cowboy.cowboy_service_client import CowboyServiceClient
from src.reporting import report_on_cowboys
from src.generated.service_discovery_pb2 import ServiceNode
from src.generated.cowboy_pb2 import Cowboy, TargetCowboy
from src.service_discovery import service_discovery_client
from src.protobuf_utils import protobuf_to_dict
from src.validators import validate_cowboy_and_service_count, validate_cowboy_count

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def shoot():
    try:
        LOGGER.info("Starting shootout")
        cowboys, services = _get_cowboys_and_services()

        validate_cowboy_count(len(cowboys))
        validate_cowboy_and_service_count(len(cowboys), len(services))

        _initialize_cowboy_services(cowboys, services)
        _start_shootout()

        report_on_cowboys(services)
    finally:
        _cleanup()


def _initialize_cowboy_services(cowboys: List[Cowboy], services: List[ServiceNode]):
    cowboy_and_service_pairs = list(zip(cowboys, services))
    for (cowboy, service_node) in cowboy_and_service_pairs:
        LOGGER.info(
            "Initializing cowboy %s located at: %s",
            cowboy.name,
            protobuf_to_dict(service_node)
        )

        target_cowboys = _get_target_cowboys(cowboy, cowboy_and_service_pairs)
        LOGGER.info(
            "Cowboy %s has targets: %s",
            cowboy.name,
            [protobuf_to_dict(target) for target in target_cowboys]
        )

        cowboy_client = CowboyServiceClient.from_service_node(service_node)
        cowboy_client.set_cowboy(cowboy)
        cowboy_client.set_target_cowboys(target_cowboys, cowboy.name)


def _get_cowboys_and_services() -> Tuple[List[Dict], List[ServiceNode]]:
    cowboys = get_cowboys()
    LOGGER.info("Cowboys: %s", cowboys)
    services = service_discovery_client.get_registered(
        constants.SERVICE_DISCOVERY_EXTERNAL_ADDRESS
    )
    LOGGER.info("Services: %s", [protobuf_to_dict(service) for service in services])
    return cowboys, services


def _get_target_cowboys(
    cowboy: Cowboy,
    cowboy_and_service_pairs: List[Tuple[Cowboy, ServiceNode]]
):
    target_pairs = [
        (target_cowboy, target_service)
        for (target_cowboy, target_service) in cowboy_and_service_pairs
        if cowboy != target_cowboy
    ]
    return [
        TargetCowboy(
            serviceAddress=f"{target_service.ip}:{target_service.port}",
            cowboyName=target_cowboy.name
        )
        for (target_cowboy, target_service) in target_pairs
    ]


def _start_shootout():
    with open(constants.SHOOTOUT_IN_PROGRESS_FILE_PATH, "w"):
        pass


def _cleanup():
    if os.path.exists(constants.SHOOTOUT_IN_PROGRESS_FILE_PATH):
        os.remove(constants.SHOOTOUT_IN_PROGRESS_FILE_PATH)

