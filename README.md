# Distributed Log Processing System

A scalable, cloud-native **Distributed Log Processing Platform** built
to ingest, process, and analyze logs in real time.

This project showcases a complete **distributed data pipeline**
including:

-   Log ingestion & validation using **Filebeat**
-   Stream buffering with **Kafka**
-   Real-time processing & schema unification via **Apache Flink**
-   High-performance OLAP storage in **ClickHouse**
-   Low-latency caching & live querying with **Redis**
-   Support for **AI-powered summarization & anomaly detection**

------------------------------------------------------------------------

## Local Setup

### **Prerequisites**

-   Docker Desktop (Windows/macOS)
-   Docker & Docker Compose
-   PowerShell (Windows) or curl/wget (macOS/Linux)

------------------------------------------------------------------------

## 1. Build the Custom Flink Docker Image

Navigate to:

    cd infra/utils

### **For macOS (ARM64 / M1 / M2 / M3)**

    FROM flink:1.18.1-scala_2.12
    USER root

    RUN apt-get update &&     apt-get install -y python3 python3-pip openjdk-11-jdk-headless &&     ln -s /usr/bin/python3 /usr/bin/python

    COPY connectors/* /opt/flink/lib/

    ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

    RUN pip install apache-flink==1.18.1
    USER flink

### **For Windows / Linux (x86_64)**

    FROM flink:1.18.1-scala_2.12
    USER root

    RUN apt-get update &&     apt-get install -y python3 python3-pip &&     ln -s /usr/bin/python3 /usr/bin/python

    RUN pip install apache-flink==1.18.1

    COPY connectors/* /opt/flink/lib/
    USER flink

------------------------------------------------------------------------

## 2. Download Flink--ClickHouse Connectors

    cd infra/flink/connectors

Windows PowerShell:

    wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/1.17.1/flink-connector-kafka-1.17.1.jar -OutFile flink-connector-kafka-1.17.1.jar

    wget https://repo1.maven.org/maven2/org/apache/flink/flink-json/1.17.1/flink-json-1.17.1.jar -OutFile flink-json-1.17.1.jar

    wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.0-1.17/flink-connector-jdbc-3.1.0-1.17.jar -OutFile flink-connector-jdbc-3.1.0-1.17.jar

    wget https://repo1.maven.org/maven2/com/clickhouse/clickhouse-jdbc/0.6.0/clickhouse-jdbc-0.6.0-all.jar -OutFile clickhouse-jdbc-0.6.0-all.jar

    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.2.3/kafka-clients-3.2.3.jar -OutFile kafka-clients-3.2.3.jar

    wget https://repo1.maven.org/maven2/com/clickhouse/flink-connector-clickhouse/1.0.0/flink-connector-clickhouse-1.0.0.jar -OutFile flink-connector-clickhouse-1.0.0.jar

    wget https://repo1.maven.org/maven2/com/clickhouse/flink/flink-connector-clickhouse-1.17/0.1.1/flink-connector-clickhouse-1.17-0.1.1-all.jar -OutFile flink-connector-clickhouse-1.17-0.1.1-all.jar

    wget https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-guava/30.1.1-jre-16.1/flink-shaded-guava-30.1.1-jre-16.1.jar -OutFile flink-shaded-guava-30.1.1-jre-16.1.jar

macOS/Linux version:

    wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/1.17.1/flink-connector-kafka-1.17.1.jar -O flink-connector-kafka-1.17.1.jar

    wget https://repo1.maven.org/maven2/org/apache/flink/flink-json/1.17.1/flink-json-1.17.1.jar -O flink-json-1.17.1.jar

    wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.0-1.17/flink-connector-jdbc-3.1.0-1.17.jar -O flink-connector-jdbc-3.1.0-1.17.jar

    wget https://repo1.maven.org/maven2/com/clickhouse/clickhouse-jdbc/0.6.0/clickhouse-jdbc-0.6.0-all.jar -O clickhouse-jdbc-0.6.0-all.jar

    wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.2.3/kafka-clients-3.2.3.jar -O kafka-clients-3.2.3.jar

    wget https://repo1.maven.org/maven2/com/clickhouse/flink-connector-clickhouse/1.0.0/flink-connector-clickhouse-1.0.0.jar -O flink-connector-clickhouse-1.0.0.jar

    wget https://repo1.maven.org/maven2/com/clickhouse/flink/flink-connector-clickhouse-1.17/0.1.1/flink-connector-clickhouse-1.17-0.1.1-all.jar -O flink-connector-clickhouse-1.17-0.1.1-all.jar

    wget https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-guava/30.1.1-jre-16.1/flink-shaded-guava-30.1.1-jre-16.1.jar -O flink-shaded-guava-30.1.1-jre-16.1.jar


------------------------------------------------------------------------

## 3. Create `.env` File

    CLICKHOUSE_HOST=localhost
    CLICKHOUSE_HTTP_PORT=8123
    CLICKHOUSE_TCP_PORT=9000
    CLICKHOUSE_DB=your_db_name
    CLICKHOUSE_USER=your_user
    CLICKHOUSE_PASSWORD=your_password

    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_DB=0

    GOOGLE_API_KEY=your_api_key

------------------------------------------------------------------------

## 4. Start the Entire Stack

    docker compose up --build -d

------------------------------------------------------------------------

## 5. Kafka Setup

Create topic:

    docker exec -it kafka /opt/kafka/bin/kafka-topics.sh   --create --bootstrap-server localhost:9092 --topic raw_logs

List topics:

    docker exec -it kafka /opt/kafka/bin/kafka-topics.sh   --bootstrap-server localhost:9092 --list

------------------------------------------------------------------------

## 6. Restart Fluent-Bit

    docker restart fluent-bit

------------------------------------------------------------------------

## 7. ClickHouse Setup

Enter container:

    docker exec -it clickhouse bash

Start client:

    clickhouse-client --user=logs_user --password=logs_pass -d your_db_name

Create table:

    CREATE TABLE logs (
        log_id UUID DEFAULT generateUUIDv4(),
        timestamp DateTime64(3, 'UTC'),
        severity LowCardinality(String),
        source_type LowCardinality(String),
        service_name LowCardinality(String),
        host String,
        host_ip IPv4,
        file_path String,
        message String,
        raw_message String,
        trace_id String,
        span_id String,
        metadata String
    )
    ENGINE = ReplacingMergeTree
    ORDER BY timestamp
    TTL timestamp + INTERVAL 30 DAY;

------------------------------------------------------------------------

## 8. Submit Flink Job

    docker exec -it flink_jobmanager bash

    flink run -d -m flink_jobmanager:8081   -py /opt/flink/usrlib/clickhouse_job.py

Flink UI: http://localhost:8081\

API Docs: http://localhost:8000/docs

------------------------------------------------------------------------

## 9. Generate Test Logs

    cd runtime
    python fake_service_log_writer.py

Dashboard:\
http://localhost:5000/
