## Cowboys

### Quickstart

`cowboys.json` contains a list of cowboys.
If you want to add or remove a cowboy this is the place
to do it.

Create virtualenv (virtualenvwrapper must be installed):
```
mkvirtualenv cowboys
```

Activate virtualenv:
```
workon cowboys
```

Install dependencies:
```
pip3 install -r requirements.txt
```


Start cowboy containers in window #1:
```
python entrypoint.py start-containers
```

Start shootout in window #2. After containers are started you can run shootout multiple times without tearing down containers:
```
python entrypoint.py shoot
```

### Requirements

Versions below were used to test this solution.

Python:
```
python --version
Python 3.8.10
```

Docker:
```
docker --version
Docker version 20.10.7, build 20.10.7-0ubuntu5~20.04.2
```

Docker compose:
```
docker-compose --version
docker-compose version 1.25.0, build unknown
```

Some containers start on fixed ports like service discovery service that uses port 8001.


### Interact with cowboys

It is possible to interact with cowboys directly using grpcurl.
You need to get specific cowboy container ip (`docker ps`) and then below commands can be used.


Set cowboy:
```
 grpcurl -plaintext -d '{"name": "David", "health": 10, "damage": 2}' <CONTAINER_IP>:8000 CowboyService/setCowboy
```

Set target cowboys:
```
  grpcurl -plaintext -d '{"targets": [{"cowboyName": "David", "serviceAddress":"a"},{"cowboyName": "John", "serviceAddress":"b"}]}' <CONTAINER_IP>:8000 CowboyService/setTargetCowboys
```

Make cowboy shoot:
```
grpcurl -plaintext -d '{}' <CONTAINER_IP>:8000 CowboyService/giveDamage
```

Shoot at cowboy:
```
grpcurl -plaintext -d '{"name": "Admin", "damage": 2}' <CONTAINER_IP>:8000 CowboyService/takeDamage
```

### Quality related commands

Run tests:
```
python3 -m pytest
```

Run tests and collect coverage report:
```
coverage run --source=./src --module pytest --verbose test && coverage report -m
```
