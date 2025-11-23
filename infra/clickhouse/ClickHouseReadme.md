# Local ClickHouse Setup (CSCI 5253 – Distributed Log Processing System)
This folder contains the **local ClickHouse setup** used by our project.

We run ClickHouse in Docker so everyone gets the same environment on their machine.
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
## 3. ClickHouse Config (used by services)
The Docker setup automatically creates:

Database: logs_db

User: logs_user

Password: logs_pass

These are defined in the Compose file under the environment: section.

```bash
cp config/clickhouse.local.env.example config/clickhouse.local.env
```

## 4. Testing ClickHouse
```bash
curl "http://localhost:8123/?user=logs_user&password=logs_pass&query=SELECT%201"
```
Output should show:
1

docker exec -it clickhouse bash

clickhouse-client --user=logs_user --password=logs_pass -d logs_db