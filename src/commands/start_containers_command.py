import logging

from plumbum import local, FG

from src.commands.command_utils import get_cowboys


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

docker_compose = local["docker-compose"]
docker = local["docker"]


def start_containers():
    cowboy_count = len(get_cowboys())
    docker_compose["build"] & FG
    docker_compose["up", "--scale", f"cowboy={cowboy_count}"] & FG
