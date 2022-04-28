def validate_cowboy_count(cowboy_count: int):
    if cowboy_count < 2:
        raise SystemExit("Shootout requires at least 2 cowboys!")


def validate_cowboy_and_service_count(cowboy_count: int, service_count: int):
    if cowboy_count != service_count:
        raise SystemExit(
            f"Number of cowboys ({cowboy_count}) and services ({service_count}) must match!"
        )
