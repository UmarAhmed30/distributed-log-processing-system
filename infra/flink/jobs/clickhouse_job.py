import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.in_streaming_mode()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    t_env.execute_sql("""
        CREATE TABLE source_kafka (
            `@timestamp` STRING,
            `log` ROW<
                `level` STRING,
                `file` ROW<`path` STRING>
            >,
            `service` ROW<
                `type` STRING,
                `name` STRING
            >,
            `host` ROW<
                `name` STRING,
                `ip` ARRAY<STRING>
            >,
            `message` STRING,
            `trace_id` STRING,
            `span_id` STRING
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'raw_logs',
            'properties.bootstrap.servers' = 'kafka:9092',
            'properties.group.id' = 'flink_processor_group',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true'
        )
    """)

    t_env.execute_sql("""
        CREATE TABLE sink_clickhouse (
            log_id STRING,
            `timestamp` TIMESTAMP(3),
            severity STRING,
            source_type STRING,
            service_name STRING,
            host STRING,
            host_ip STRING,
            file_path STRING,
            message STRING,
            raw_message STRING,
            trace_id STRING,
            span_id STRING,
            metadata STRING
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:clickhouse://clickhouse:8123/logs_db',
            'table-name' = 'logs',
            'username' = 'logs_user',
            'password' = 'logs_pass',
            'driver' = 'com.clickhouse.jdbc.ClickHouseDriver',
            'sink.buffer-flush.max-rows' = '1000',
            'sink.buffer-flush.interval' = '1s'
        )
    """)

    t_env.execute_sql("""
        INSERT INTO sink_clickhouse
        SELECT
            UUID() as log_id,
            TO_TIMESTAMP(`@timestamp`) as `timestamp`,
            COALESCE(`log`.`level`, 'INFO') as severity,
            COALESCE(`service`.`type`, 'unknown') as source_type,
            COALESCE(`service`.`name`, 'unknown-service') as service_name,
            COALESCE(`host`.`name`, 'unknown-host') as host,
            COALESCE(`host`.`ip`[1], '0.0.0.0') as host_ip,
            COALESCE(`log`.`file`.`path`, '') as file_path,
            `message`,
            `message` as raw_message,
            COALESCE(`trace_id`, '') as trace_id,
            COALESCE(`span_id`, '') as span_id
        FROM source_kafka
    """)

if __name__ == "__main__":
    main()

# Sample Kafka Payload (JSON):

# {
#     "@timestamp": "2025-11-23T10:00:00.123Z",
#     "log": {
#         "level": "ERROR",
#         "file": {
#             "path": "/var/log/payment-service/app.log"
#         }
#     },
#     "service": {
#         "type": "application"
#         "name": "payment-service"
#     },
#     "host": {
#         "name": "worker-node-01",
#         "ip": ["192.168.1.15", "10.0.0.5"]
#     },
#     "message": "Transaction failed due to timeout connecting to database.",
#     "trace_id": "a1b2c3d4e5f6",
#     "span_id": "1234567890",
# }
