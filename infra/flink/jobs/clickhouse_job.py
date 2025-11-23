from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import (
    StreamTableEnvironment,
    EnvironmentSettings,
)

def main():
    # --------------------------------------------
    # 1. Create Flink env
    # --------------------------------------------
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.in_streaming_mode()
    table_env = StreamTableEnvironment.create(env, environment_settings=settings)

    # --------------------------------------------
    # 2. Kafka Source Table
    # --------------------------------------------
    table_env.execute_sql("""
        CREATE TABLE kafka_logs (
            log_id STRING,
            timestamp TIMESTAMP(3),
            severity STRING,
            source_type STRING,
            service_name STRING,
            host STRING,
            host_ip STRING,
            message STRING,
            raw_message STRING,
            trace_id STRING,
            span_id STRING,
            metadata STRING,
            `partition` BIGINT METADATA VIRTUAL,
            `offset` BIGINT METADATA VIRTUAL
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'raw_logs',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'flink-log-group',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        );
    """)

    # --------------------------------------------
    # 3. ClickHouse Sink Table
    # --------------------------------------------
    table_env.execute_sql("""
        CREATE TABLE clickhouse_logs (
            log_id UUID,
            timestamp TIMESTAMP(3),
            severity String,
            source_type String,
            service_name String,
            host String,
            host_ip String,
            message String,
            raw_message String,
            trace_id String,
            span_id String,
            metadata String
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:clickhouse://localhost:8123/logs_db',
            'table-name' = 'logs',
            'username' = 'logs_user',
            'password' = 'logs_pass',
            'sink.batch-size' = '1000',
            'sink.flush-interval' = '2s'
        );
    """)

    # --------------------------------------------
    # 4. Stream Transformation (Optional)
    # --------------------------------------------
    # You can enrich logs here, parse metadata, etc.
    result = table_env.execute_sql("""
        INSERT INTO clickhouse_logs
        SELECT
            log_id,
            timestamp,
            severity,
            source_type,
            service_name,
            host,
            host_ip,
            message,
            raw_message,
            trace_id,
            span_id,
            metadata
        FROM kafka_logs;
    """)

    result_wait = result.wait()
    print("Flink job completed:", result_wait)


if __name__ == "__main__":
    main()
