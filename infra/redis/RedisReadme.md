# Local Redis Setup (CSCI 5253 – Distributed Log Processing System)
This folder contains the **local Redis setup** used by our project.

We run Redis in Docker so everyone gets the same environment on their machine.
```bash
docker compose up -d
```
Chceck if the containers are running:

```bash
docker ps
```
To stop:

```bash
docker compose down
```
## Testing Redis
You can use the Redis CLI to test the Redis server.
```bash
docker exec -it redis redis-cli
```
Once inside the Redis CLI, you can run commands like:
```bash
127.0.0.1:6379> PING
```
Output should show:
PONG

You can also set and get a value:
```bash
SET test_key "hello-from-redis"
GET test_key
```
Output should show:
"hello-from-redis"

Exit the Redis CLI:
```bash127.0.0.1:6379> EXIT
```
