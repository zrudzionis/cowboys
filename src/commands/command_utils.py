import json
import logging
from typing import List

from src import constants
from src.generated.cowboy_pb2 import Cowboy

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def get_cowboys() -> List[Cowboy]:
    LOGGER.info("Loading cowboys from file: '%s'", constants.COWBOYS_FILE_PATH)
    with open(constants.COWBOYS_FILE_PATH, "r") as fd:
        cowboy_dicts = json.load(fd)
        cowboys = [
            Cowboy(
                name=cowboy_dict["name"],
                health=cowboy_dict["health"],
                damage=cowboy_dict["damage"]
            )
            for cowboy_dict in cowboy_dicts
        ]
        LOGGER.info("Cowboys loaded")
        return cowboys
