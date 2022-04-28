#!/bin/bash

# print trace
set -x

# exit on first failure
set -e

python3 -m "src.cowboy.cowboy_entrypoint" & python3 -m "src.scheduler.scheduler_entrypoint"
