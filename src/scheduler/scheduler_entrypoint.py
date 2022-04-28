
import logging
import time
import os
import sys

from retry import retry

from src import constants
from src.constants import CowboyStatusCodes
from src.cowboy.cowboy_service_client import CowboyServiceClient
from src.exceptions import RetryException


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

COWBOY_CANT_SHOOT_STATUS_CODES = [
    CowboyStatusCodes.I_AM_DEAD_CODE,
    CowboyStatusCodes.NO_TARGETS_AVAILABLE_CODE
]

RETRYABLE_STATUS_CODES = [
    CowboyStatusCodes.SHOT_FAILED_CODE,
    CowboyStatusCodes.TARGET_IS_DEAD_CODE
]


def main():
    shooter_address = constants.COWBOY_INTERNAL_ADDRESS
    give_damage_status_code = None
    while True:
        is_shootout_in_progress = _is_shootout_in_progress()
        cowboy_can_shoot = _cowboy_can_shoot(give_damage_status_code)

        if is_shootout_in_progress and not shooter:
            cowboy_client = CowboyServiceClient(shooter_address)
            shooter = cowboy_client.get_cowboy()

        if is_shootout_in_progress and cowboy_can_shoot:
            give_damage_status_code = _give_damage_retryable(cowboy_client, shooter.name)
            time.sleep(constants.GIVE_DAMAGE_SCHEDULED_DELAY_IN_SECONDS)

        if not is_shootout_in_progress:
            give_damage_status_code = None
            shooter = None


@retry(exceptions=RetryException, tries=constants.MAX_GIVE_DAMAGE_RETRIES, logger=LOGGER)
def _give_damage_retryable(cowboy_client: CowboyServiceClient, shooter_name: str):
    """
    Normally exponential backoff + jitter is used but in this case we expect
    to hit dead cowboys in which case operation can be retried immediately.
    """
    give_damage_status_code = cowboy_client.give_damage(shooter_name)

    if give_damage_status_code in RETRYABLE_STATUS_CODES:
        raise RetryException()

    return give_damage_status_code


def _is_shootout_in_progress():
    return os.path.exists(constants.SHOOTOUT_IN_PROGRESS_FILE_PATH)


def _cowboy_can_shoot(give_damage_status_code: str):
    return give_damage_status_code not in COWBOY_CANT_SHOOT_STATUS_CODES


if __name__ == "__main__":
    main()
