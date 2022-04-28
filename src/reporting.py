import logging
import time
from typing import List

from src import constants
from src.cowboy.cowboy_service_client import CowboyServiceClient
from src.generated.cowboy_pb2 import Cowboy
from src.generated.service_discovery_pb2 import ServiceNode

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def report_on_cowboys(cowboy_services: List[ServiceNode]) -> None:
    alive_cowboys = [1, 1]
    while len(alive_cowboys) > 1 :
        alive_cowboys = _get_alive_cowboys(cowboy_services)
        _report_alive_cowboys(alive_cowboys)
        time.sleep(constants.REPORTING_DELAY_IN_SECONDS)
    _report_last_man_standing(alive_cowboys)


def _get_alive_cowboys(cowboy_services: List[ServiceNode]) -> None:
    alive_cowboys = []
    for cowboy_service in cowboy_services:
        cowboy_service_client = CowboyServiceClient.from_service_node(cowboy_service)
        cowboy = cowboy_service_client.get_cowboy()
        if cowboy.health > 0:
            alive_cowboys.append(cowboy)
    return alive_cowboys


def _report_alive_cowboys(alive_cowboys: List[Cowboy]) -> None:
    LOGGER.info("=================== REPORT ===================")
    LOGGER.info("Alive cowboy count: %s", len(alive_cowboys))
    for cowboy in alive_cowboys:
        LOGGER.info("%s is alive with health: %s", cowboy.name, cowboy.health)


def _report_last_man_standing(alive_cowboys: List[Cowboy]) -> None:
    alive_count = len(alive_cowboys)
    if alive_count == 1:
        last_alive = alive_cowboys[0]
        LOGGER.info(
            "Last man standing is %s with remaining health: %s",
            last_alive.name,
            last_alive.health
        )
    elif alive_count == 0:
        LOGGER.info("All cowboys died in the shootout!")
