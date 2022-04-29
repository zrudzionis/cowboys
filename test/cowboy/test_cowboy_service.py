import unittest
from unittest.mock import Mock, patch
from src.constants import CowboyStatusCodes

from src.cowboy.cowboy_service import CowboyService, CowboyServiceClient
from src.generated.cowboy_pb2 import Cowboy, Shooter, TargetCowboy, TargetCowboys
from src.generated.shared_pb2 import Void


SHOOTER_BOB = Shooter(
    name="Bob",
    damage=2
)
COBOY_BILL = Cowboy(
    name="Bill",
    health=10,
    damage=3
)
TARGET_COBOY_BILL_JIM = TargetCowboy(
    serviceAddress="172.0.0.1:8000",
    cowboyName="Jim"
)
TARGET_COBOY_BILLS = TargetCowboys(
    target=[
        TARGET_COBOY_BILL_JIM
    ]
)

class CowboyServiceGetterSetterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cowboy = COBOY_BILL
        self.service_discovery_client = Mock()
        self.service = CowboyService(self.service_discovery_client)

    def test_upon_creation_registers_with_service_discovery_service(self):
        self.service_discovery_client.register.assert_called_once()

    def test_set_cowboy(self):
        response = self.service.setCowboy(self.cowboy)
        self.assertEqual(response.statusCode, CowboyStatusCodes.SUCCESS_CODE)

    def test_get_cowboy(self):
        self.service.setCowboy(self.cowboy)
        cowboy = self.service.getCowboy(Void())
        self.assertEqual(cowboy, self.cowboy)

    def test_set_target_cowboys(self):
        target_cowboys = TargetCowboys(
            target=[
                TargetCowboy(
                    serviceAddress="Bill",
                    cowboyName="Jim"
                )
            ]
        )
        response = self.service.setTargetCowboys(target_cowboys)
        self.assertEqual(response.statusCode, CowboyStatusCodes.SUCCESS_CODE)


class CowboyServiceGiveTakeDamageTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cowboy = COBOY_BILL
        self.service_discovery_client = Mock()
        self.service = CowboyService(self.service_discovery_client)
        self.service.setCowboy(COBOY_BILL)
        self.service.setTargetCowboys(TARGET_COBOY_BILLS)

    def test_take_damage(self):
        shooter = SHOOTER_BOB
        response = self.service.takeDamage(shooter)
        self.assertEqual(response.statusCode, CowboyStatusCodes.SUCCESS_CODE)

        latest_cowboy_state = self.service.getCowboy(Void())
        self.assertEqual(latest_cowboy_state.health, 8)

    @patch.object(CowboyServiceClient, "take_damage")
    def test_give_damage(self, take_damage_mock):
        take_damage_mock.return_value = CowboyStatusCodes.SUCCESS_CODE
        response = self.service.giveDamage(Void())
        self.assertEqual(response.statusCode, CowboyStatusCodes.SUCCESS_CODE)
        take_damage_mock.assert_called_once_with(COBOY_BILL, TARGET_COBOY_BILL_JIM.cowboyName)
