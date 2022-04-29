from unittest import TestCase
from unittest.mock import patch, Mock

from src.constants import CowboyStatusCodes
from src.scheduler.scheduler_entrypoint import main

ENTRYPOINT_PATH = "src.scheduler.scheduler_entrypoint"
KEEP_LOOPING_PATH = ENTRYPOINT_PATH + ".keep_looping"
SHOOTOUT_IN_PROGRESS_PATH = ENTRYPOINT_PATH + ".is_shootout_in_progress"
COWBOY_SERVICE_CLIENT_PATH = ENTRYPOINT_PATH + ".CowboyServiceClient"
TIME_PATH = ENTRYPOINT_PATH + ".time"

class SchedulerTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.keep_looping_patcher = patch(KEEP_LOOPING_PATH)
        self.keep_looping = self.keep_looping_patcher.start()

        self.cowboy_service_client = Mock()
        self.cowboy_service_client_patcher = patch(COWBOY_SERVICE_CLIENT_PATH)
        self.cowboy_service_client_class = self.cowboy_service_client_patcher.start()
        self.cowboy_service_client_class.return_value = self.cowboy_service_client

        self.shootout_in_progress_patcher = patch(SHOOTOUT_IN_PROGRESS_PATH)
        self.shootout_in_progress = self.shootout_in_progress_patcher.start()

        self.time_patcher = patch(TIME_PATH)
        self.time_patcher.start()

    def tearDown(self) -> None:
        self.keep_looping_patcher.stop()
        self.cowboy_service_client_patcher.stop()
        self.shootout_in_progress_patcher.stop()
        self.time_patcher.stop()
        super().tearDown()

    def test_invokes_give_damage(self):
        self.keep_looping.side_effect = [True, False]
        self.shootout_in_progress.return_value = True
        self.cowboy_service_client.give_damage.return_value = CowboyStatusCodes.SUCCESS_CODE

        main()

        self.cowboy_service_client.give_damage.assert_called_once()

    def test_when_shootout_is_no_longer_in_progress_then_stops_shooting(self):
        self.keep_looping.side_effect = [True, True, False]
        self.shootout_in_progress.return_value = True
        self.cowboy_service_client.give_damage.return_value = CowboyStatusCodes.SUCCESS_CODE

        main()

        self.assertEqual(self.cowboy_service_client.give_damage.call_count, 2)


    def test_when_client_responds_with_retryable_error_then_we_retry(self):
        self.keep_looping.side_effect = [True, False]
        self.shootout_in_progress.return_value = True
        self.cowboy_service_client.give_damage.side_effect = [
            CowboyStatusCodes.SHOT_FAILED_CODE,
            CowboyStatusCodes.SUCCESS_CODE
        ]

        main()

        self.assertEqual(self.cowboy_service_client.give_damage.call_count, 2)


    def test_when_shootout_is_not_in_progress_then_we_dont_shoot(self):
        self.keep_looping.side_effect = [True, False]
        self.shootout_in_progress.return_value = False

        main()

        self.assertEqual(self.cowboy_service_client.give_damage.call_count, 0)
