import logging
from typing import List

from grpc import insecure_channel

from src.generated.cowboy_pb2 import Cowboy, Shooter, TargetCowboy, TargetCowboys
from src.generated.cowboy_pb2_grpc import CowboyServiceStub
from src.generated.service_discovery_pb2 import ServiceNode
from src.generated.shared_pb2 import Void
from src.protobuf_utils import protobuf_to_dict


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class CowboyServiceClient:
    def __init__(self, service_address: str):
        self._channel = insecure_channel(service_address)
        self._service = CowboyServiceStub(self._channel)

    def __del__(self):
        self._channel.close()

    @staticmethod
    def from_service_node(service_node: ServiceNode) -> "CowboyServiceClient":
        return CowboyServiceClient(f"{service_node.ip}:{service_node.port}")

    def take_damage(self, shooter: Cowboy, target_name: str) -> str:
        LOGGER.info("%s shooting at %s", shooter.name, target_name)

        response = self._service.takeDamage(
            Shooter(
                name=shooter.name,
                damage=shooter.damage
            )
        )
        status_code = response.statusCode

        LOGGER.info("%s received response status: %s", shooter.name, status_code)

        return status_code

    def give_damage(self, shooter_name: str) -> str:
        LOGGER.info("invoking giveDamage on: %s", shooter_name)
        response = self._service.giveDamage(Void())
        status_code = response.statusCode
        LOGGER.info("%s giveDamage returned: %s", shooter_name, status_code)
        return status_code

    def get_cowboy(self) -> Cowboy:
        LOGGER.debug("invoking getCowboy")
        response = self._service.getCowboy(Void())
        LOGGER.debug("getCowboy returned: %s", protobuf_to_dict(response))
        return response

    def set_cowboy(self, cowboy: Cowboy) -> str:
        LOGGER.debug("invoking setCowboy")
        response = self._service.setCowboy(cowboy)
        status_code = response.statusCode
        LOGGER.debug("setCowboy returned: %s", status_code)
        return status_code

    def set_target_cowboys(
        self,
        target_cowboys: List[TargetCowboy],
        cowboy_name: str
    ) -> str:
        LOGGER.debug("invoking setTargetCowboys")
        response = self._service.setTargetCowboys(
            TargetCowboys(target=target_cowboys)
        )
        status_code = response.statusCode
        LOGGER.debug(
            "Cowboy %s setTargetCowboys returned status code: %s",
            cowboy_name,
            status_code
        )
        return status_code
