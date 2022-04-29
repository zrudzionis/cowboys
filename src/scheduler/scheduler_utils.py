import os

from src import constants


def keep_looping():
    return True


def is_shootout_in_progress():
    return os.path.exists(constants.SHOOTOUT_IN_PROGRESS_FILE_PATH)
