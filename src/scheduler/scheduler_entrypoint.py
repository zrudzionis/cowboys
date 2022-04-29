
import logging
import time
import sys

from retry import retry

from src import constants
from src.cowboy.cowboy_service_client import CowboyServiceClient
from src.exceptions import RetryException
from src.scheduler.scheduler_utils import keep_looping, is_shootout_in_progress

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def main():
    shooter_address = constants.COWBOY_INTERNAL_ADDRESS
    give_damage_status_code = None
    shooter = None
    while keep_looping():
        shootout_in_progress = is_shootout_in_progress()
        cowboy_can_shoot = _cowboy_can_shoot(give_damage_status_code)

        if shootout_in_progress and not shooter:
            cowboy_client = CowboyServiceClient(shooter_address)
            shooter = cowboy_client.get_cowboy()

        if shootout_in_progress and cowboy_can_shoot:
            give_damage_status_code = _give_damage_retryable(cowboy_client, shooter.name)
            time.sleep(constants.GIVE_DAMAGE_SCHEDULED_DELAY_IN_SECONDS)

        if not shootout_in_progress:
            give_damage_status_code = None
            shooter = None


@retry(exceptions=RetryException, tries=constants.MAX_GIVE_DAMAGE_RETRIES, logger=LOGGER)
def _give_damage_retryable(cowboy_client: CowboyServiceClient, shooter_name: str):
    """
    Normally exponential backoff + jitter is used but in this case we expect
    to hit dead cowboys in which case operation can be retried immediately.
    """
    give_damage_status_code = cowboy_client.give_damage(shooter_name)

    if give_damage_status_code in constants.RETRYABLE_STATUS_CODES:
        raise RetryException()

    return give_damage_status_code


def _cowboy_can_shoot(give_damage_status_code: str):
    return give_damage_status_code not in constants.COWBOY_CANT_SHOOT_STATUS_CODES


if __name__ == "__main__":
    main()
