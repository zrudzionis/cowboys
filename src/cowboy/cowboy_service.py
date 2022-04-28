import json
import logging
import random
import socket
from typing import Optional
from threading import Lock

from src import constants
from src.constants import CowboyStatusCodes
from src.generated.cowboy_pb2_grpc import CowboyServiceServicer
from src.cowboy.cowboy_service_client import CowboyServiceClient
from src.service_discovery import service_discovery_client
from src.generated.cowboy_pb2 import (
    Cowboy,
    Response
)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class CowboyServiceServicer(CowboyServiceServicer):
    """
    It is possible for two cowboys to shoot each other at the same time.
    It is not possible for one cowboy to be shot by two cowboys.
    """
    me = None
    my_health_lock = Lock()

    target_cowboys = None

    def __init__(self) -> None:
        super().__init__()
        service_discovery_client.register(
            service_address=constants.SERVICE_DISCOVERY_INTERNAL_ADDRESS,
            service_name=constants.COWBOY_SERVICE_NAME,
            ip=socket.gethostbyname(socket.gethostname()),
            port=str(constants.COWBOY_SERVER_PORT)
        )

    def getCowboy(self, _, __):
        LOGGER.info("getCowboy was called")
        if self.me is None:
            return
        else:
            return self.me

    def setCowboy(self, request, _):
        LOGGER.info("setCowboy was called with: '%s'", request)
        self.me = request
        return _get_success_response()

    def setTargetCowboys(self, request, _):
        LOGGER.info("initTargetCowboys called with: '%s'", request.target)
        self.target_cowboys = request.target
        return _get_success_response()

    def takeDamage(self, request, _):
        """
        Method to take damage from another cowboy
        """
        shooter_name = request.name
        damage = request.damage

        LOGGER.info(
            "%s take damage was called by %s",
            self.me.name, shooter_name
        )

        with self.my_health_lock:
            if self.me.health <= 0:
                LOGGER.info(
                    "%s is dead so not taking damage by %s ",
                    self.me.name, shooter_name
                )
                return _get_response(CowboyStatusCodes.I_AM_DEAD_CODE)

            status_code = self._take_damage_synchronized(shooter_name, damage)

            LOGGER.info(
                "%s took %d damage from %s",
                self.me.name, damage, shooter_name
            )

            return _get_response(status_code)

    def giveDamage(self, _, __):
        """
        Method to give damage to another cowboy
        """
        LOGGER.info("%s giveDamage invoked", self.me.name)

        if self.me.health <= 0:
            LOGGER.info("%s unable to shoot while dead", self.me.name)
            return _get_response(CowboyStatusCodes.I_AM_DEAD_CODE)

        target = self._get_target()

        if target is None:
            LOGGER.info(
                "%s is unable to shoot anyone because there are no targets",
                self.me.name
            )
            return _get_response(CowboyStatusCodes.NO_TARGETS_AVAILABLE_CODE)

        LOGGER.info("%s selected target: %s",
            self.me.name, target.cowboyName
        )

        cowboy_client = CowboyServiceClient(target.serviceAddress)
        status_code = cowboy_client.take_damage(self.me, target.cowboyName)

        return self._handle_cowboy_take_damage_response(target, status_code)

    def _handle_cowboy_take_damage_response(self, target, status_code):
        return_status_code = None
        if status_code == CowboyStatusCodes.SUCCESS_CODE:
            LOGGER.info(
                "%s shot %s with damage: %d",
                self.me.name, target.cowboyName, self.me.damage
            )
            return_status_code = CowboyStatusCodes.SUCCESS_CODE
        elif status_code == CowboyStatusCodes.THIS_SHOT_KILLED_ME_SUCCESS_CODE:
            self._remove_target(target.cowboyName)
            LOGGER.info(
                "%s shot and killed %s with damage: %d",
                self.me.name, target.cowboyName, self.me.damage
            )
            return_status_code = CowboyStatusCodes.SUCCESS_CODE
        elif status_code == CowboyStatusCodes.I_AM_DEAD_CODE:
            self._remove_target(target.cowboyName)
            LOGGER.info(
                "%s tried shooting %s but he replied: %s",
                self.me.name, target.cowboyName, status_code
            )
            return_status_code = CowboyStatusCodes.TARGET_IS_DEAD_CODE
        else:
            return_status_code = CowboyStatusCodes.SHOT_FAILED_CODE

        return _get_response(return_status_code)

    def _get_target(self) -> Optional[Cowboy]:
        if not self.target_cowboys:
            return None
        else:
            return random.choice(self.target_cowboys)

    def _remove_target(self, target_name: str):
        LOGGER.info("%s removing %s from targets", self.me.name, target_name)
        self.target_cowboys = [
            cowboy
            for cowboy in self.target_cowboys
            if cowboy.cowboyName != target_name
        ]

    def _take_damage_synchronized(self, shooter_name: str, damage: int) -> str:
        if damage >= self.me.health:
            self.me.health = 0
            LOGGER.info("%s was killed by: %s.", self.me.name, shooter_name)
            return CowboyStatusCodes.THIS_SHOT_KILLED_ME_SUCCESS_CODE
        else:
            self.me.health -= damage
            LOGGER.info(
                "%s got shot by %s with damage: %s.",
                self.me.name, shooter_name, damage
            )
            return CowboyStatusCodes.SUCCESS_CODE


def _get_success_response():
    return Response(statusCode=CowboyStatusCodes.SUCCESS_CODE)


def _get_response(status_code: str):
    return Response(statusCode=status_code)
