# Local Kafka Setup (CSCI 5253 – Distributed Log Processing System)

This folder contains the **local Kafka setup** used by our project.

We run Kafka in Docker so everyone gets the same environment on their machine.

---

## 1. Prerequisites

- Docker Desktop installed and running  
- (Optional, but useful) Homebrew + `kcat` for quick Kafka testing
- brew install kcat (check equivalent for your OS if not using MAC)

---

## 2. Starting Kafka

From this folder (where `docker-compose.yaml` is located), run:

```bash
docker compose up -d
```
Chceck if the containers are running:

```bash
docker ps
```
To stop Kafka:

```bash
docker compose down
```
## 3. Kafka Config (used by services)

We keep shared Kafka config in the repo under config/:

Template file (committed):
config/kafka.local.env.example

Local file (not committed):
config/kafka.local.env

First-time setup

From the repo root:
cp config/kafka.local.env.example config/kafka.local.env
Our services (FastAPI, Flink, etc.) will read these variables when connecting to Kafka.

## 4. Testing Kafka with kcat
You can use `kcat` to quickly test Kafka topics.

```bash
echo "hello-from-kafka" | kcat -P -b localhost:9092 -t test-topic
kcat -C -b localhost:9092 -t test-topic -o beginning -q
```
Output should show:
hello-from-kafka
