from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common import WatermarkStrategy, Types, Row
from pyflink.datastream.connectors.jdbc import JdbcSink, JdbcConnectionOptions, JdbcExecutionOptions
import json
from datetime import datetime

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    
    # Kafka source
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers("kafka:19092") \
        .set_topics("raw_logs") \
        .set_group_id("flink_processor_group") \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .set_property("request.timeout.ms", "120000") \
        .set_property("session.timeout.ms", "60000") \
        .set_property("metadata.max.age.ms", "60000") \
        .set_property("connections.max.idle.ms", "540000") \
        .build()
    
    stream = env.from_source(
        kafka_source, 
        WatermarkStrategy.no_watermarks(), 
        "Kafka Source"
    )
    
    # Define output type
    output_type = Types.ROW([
        Types.STRING(),  # timestamp
        Types.STRING(),  # severity
        Types.STRING(),  # source_type
        Types.STRING(),  # service_name
        Types.STRING(),  # host
        Types.STRING(),  # host_ip
        Types.STRING(),  # file_path
        Types.STRING(),  # message
        Types.STRING(),  # raw_message
        Types.STRING(),  # trace_id
        Types.STRING()   # span_id
    ])
    
    # Transform function with timestamp conversion
    def parse_and_transform(json_str):
        try:
            data = json.loads(json_str)
            
            # Convert ISO 8601 timestamp to ClickHouse format
            timestamp_str = data.get('@timestamp', datetime.now().isoformat())
            try:
                # Parse ISO format and convert to ClickHouse format
                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                # ClickHouse expects 'YYYY-MM-DD HH:MM:SS' format
                timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                # Fallback to current time if parsing fails
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            level = data.get('log', {}).get('level', 'INFO')
            service_type = data.get('service', {}).get('type', 'unknown')
            service_name = data.get('service', {}).get('name', 'unknown-service')
            host_name = data.get('host', {}).get('name', 'unknown-host')
            host_ips = data.get('host', {}).get('ip', ['0.0.0.0'])
            host_ip = host_ips[0] if host_ips else '0.0.0.0'
            file_path = data.get('log', {}).get('file', {}).get('path', '')
            message = data.get('message', '')
            trace_id = data.get('trace_id', '')
            span_id = data.get('span_id', '')
            
            return Row(timestamp, level, service_type, service_name, host_name, 
                      host_ip, file_path, message, message, trace_id, span_id)
        except Exception as e:
            print(f"Error parsing: {e}, input was: {json_str}")
            return None
    
    transformed = stream.map(parse_and_transform, output_type=output_type) \
                       .filter(lambda x: x is not None)
    
    # JDBC options
    jdbc_execution_options = JdbcExecutionOptions.builder() \
        .with_batch_size(1000) \
        .with_batch_interval_ms(1000) \
        .with_max_retries(3) \
        .build()
    
    jdbc_connection_options = JdbcConnectionOptions.JdbcConnectionOptionsBuilder() \
        .with_url("jdbc:clickhouse://clickhouse:8123/logs_db") \
        .with_driver_name("com.clickhouse.jdbc.ClickHouseDriver") \
        .with_user_name("logs_user") \
        .with_password("logs_pass") \
        .build()
    
    # Sink
    transformed.add_sink(
        JdbcSink.sink(
            """INSERT INTO logs (timestamp, severity, source_type, service_name, 
               host, host_ip, file_path, message, raw_message, trace_id, span_id) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            output_type,
            jdbc_connection_options,
            jdbc_execution_options
        )
    )
    
    env.execute("Kafka to ClickHouse Pipeline")

if __name__ == "__main__":
    main()