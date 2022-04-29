## Cowboys

## Thoughts on possible solutions

There are many ways to approach this problem.
I will describe couple of them briefly.

### Cowboy to cowboy and arbiter observing (implemented)

Is based on p2p communication between cowboys.
From time to time arbiter looks at the current state of cowboys and
report who is alive. Last man that is alive wins. One drawback
of this appraoch is that it is possible to have no winner at the end
of the shootout meaning that last cowboys shoot each other.
* Pros:
    * No single point of failure
    * Scalable
* Cons:
    * More complex
    * 0 or 1 surviving cowboy

### Cowboy to arbiter

We can have cowboys talking to arbiter.
Cowboys would send information who they chose to shoot.
Arbiter would aquire two locks.
One on shooting cowboy's health and
one on cowboy's that is being shot health.
* Pros:
    * 1 surviving cowboy
* Cons:
    * Single point of failure
    * Arbiter is only vertically scalable

### Cowboy to queue to arbiter

Cowboys choose who they want to shoot
and push their selection to queue.
Arbiter is reading the queue and interpreting the messages.
Dead cowboy messages are dropped.
Messages to shoot dead cowboys are dropped.
Messages are interpreted in order of earliest creation time first.
* Pros:
    * Scalable
* Cons:
    * Cowboy can shoot a dead cowboy

### Cowboy to queue to arbiter that is reinterpreting

Cowboys know how many other cowboys (n) there are.
Cowboy chooses a number (1..n) that he wants to shoot
and pushes this number to queue.
Arbiter is reading the queue and interpreting the messages.
Dead cowboy messages are dropped.
When arbiter receives a message of cowboy shooting someone
he takes number of currently alive cowboys (excluding shooter).
Let's call this number m. Arbiter calculates a new value
n mod m.
Calculated value will be point to cowboys that must be shot.

* Pros:
    * Scalable
* Cons:
    * Business logic leaks across multiple services


## Setup

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
