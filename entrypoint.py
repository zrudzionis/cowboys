import logging
import sys

import typer

from src.commands.shoot_command import shoot
from src.commands.start_containers_command import start_containers

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def main():
    app = typer.Typer()
    app.command()(start_containers)
    app.command()(shoot)
    app()

if __name__ == "__main__":
    main()
