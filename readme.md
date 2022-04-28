### Startup
```
python3 src/entrypoint.py
```
 
### Test operations using grpcurl

```
 grpcurl -plaintext -d '{"name": "David", "health": 10, "damage": 2}' localhost:8000 CowboyService/initMe
```

```
  grpcurl -plaintext -d '{"targets": [{"cowboyName": "David", "serviceAddress":"a"},{"cowboyName": "John", "serviceAddress":"b"}]}' localhost:8000 CowboyService/initTargetCowboys
```

### Decision making
Communication method has 2 options:
    1. Direct (TCP, UDP, HTTP, gRPC)
    2. Via message queue (TCP)

There are 3 types of information:
    1. Start of shootout - list of cowboys is shared
    2. Cowboy A shot Cowboy B - health points are removed
    3. Cowboy is dead - list of alive cowboys gets smaller  

Where all cowboys must be notified it would be best
to use queue with pub/sub. This would be: #1 and #3 information.
It is not acceptable to use queue for #2 since it would be
possible to shoot at the dead cowboy.   

#2 information can be exchanged in two ways:
    1. Cowboy to cowboy. Cowboy would hold it's health data
    2. Cowboy to coordinator. Coordinator is a service that
    would hold cowboys health state and decide when cowboy should die.

We choose to use cowboy-to-cowboy communication because it is scalable
and not complex. Imagine having 1000 or more cowboys sending messages to
a single coordinator. It would require either vertical scaling of
single coordinator instance or horizontal scaling. If we would do
horizontal scaling we would add a lot of complexity like:
partitioning health data, correct request routing,
coordinator server health monitoring and so on.

Since now cowboys communicate directly we need to decide between:
    1. UDP - message delivery is not guaranteed
    2. TCP - message delivery is guaranteed

We must choose TCP otherwise some of the shots might get lost.

Now we must choose between:
    1. HTTP
    2. gRPC

We would choose gRPC because it offers lower latency.

Now we need to consider some edge cases. We will call shooter cowboy - sender and cowboy getting shot - receiver:
    1. Sender shoots at receiver and received is either killed by the shot or already dead:
        1.1 Receiver replies that it is dead
        1.2 Sender updates its alive cowboys list
        1.3 If receiver was already dead sender tries to shoot again at random cowboy without a delay
    2. Both Jim and Bob can kill Peter with one shot (Jim, Bob -> Peter).
    They shoot at the same time and one of them kills Peter:
        1.1 Peter accepts both requests
        1.2 Request that first aquires health semaphore wins. 
    2. Jim shoots at Bob and Bob shoot at Peter at the same time (Jim -> Bob -> Peter).
    We can't allow these two operations to happen at the same time
    otherwise if Jim kills Bob then Peter could get shot by the deadman.
        2.2 Sender checks if he is alive (using locks) before attempting to shoot
        2.1 Sender releases the lock before sending request to avoid deadlock
        (Jim -> Bob -> Peter -> Jim)    

### Other

Generate python protobuf files:
```
python -m grpc_tools.protoc -I./protos --python_out=./src --grpc_python_out=./src ./protos/cowboy.proto
```


grpcurl -plaintext -d '{"name": "Bryan", "health": 10, "damage": 2}' localhost:8001 CowboyService/initMe



grpcurl -plaintext -d '{"name": "David", "health": 10, "damage": 2}' localhost:8000 CowboyService/initMe

grpcurl -plaintext -d '{"target": [{"cowboyName": "Bryan", "serviceAddress":"localhost:8001"}]}' localhost:8000 CowboyService/initTargetCowboys

grpcurl -plaintext -d '{}' localhost:49212 CowboyService/giveDamage

grpcurl -plaintext -d '{"name": "Admin", "damage": 2}' localhost:49212 CowboyService/takeDamage



sudo docker-compose up --scale cowboy=3


python entrypoint.py start-containers
python entrypoint.py shoot
