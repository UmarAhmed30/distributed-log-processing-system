wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/1.17.1/flink-connector-kafka-1.17.1.jar -OutFile "flink-connector-kafka-1.17.1.jar"

wget https://repo1.maven.org/maven2/org/apache/flink/flink-json/1.17.1/flink-json-1.17.1.jar -OutFile "flink-json-1.17.1.jar"

wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.0-1.17/flink-connector-jdbc-3.1.0-1.17.jar -OutFile "flink-connector-jdbc-3.1.0-1.17.jar"

wget https://repo1.maven.org/maven2/com/clickhouse/clickhouse-jdbc/0.6.0/clickhouse-jdbc-0.6.0-all.jar -OutFile "clickhouse-jdbc-0.6.0-all.jar"

wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.2.3/kafka-clients-3.2.3.jar -OutFile kafka-clients-3.2.3.jar

wget https://repo1.maven.org/maven2/com/clickhouse/flink-connector-clickhouse/1.0.0/flink-connector-clickhouse-1.0.0.jar -OutFile flink-connector-clickhouse-1.0.0.jar

wget https://repo1.maven.org/maven2/com/clickhouse/flink/flink-connector-clickhouse-1.17/0.1.1/flink-connector-clickhouse-1.17-0.1.1-all.jar -OutFile flink-connector-clickhouse-1.17-0.1.1-all.jar

wget https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-guava/30.1.1-jre-16.1/flink-shaded-guava-30.1.1-jre-16.1.jar -OutFile flink-shaded-guava-30.1.1-jre-16.1.jar

flink run -d -m flink_jobmanager:8081 -py /opt/flink/usrlib/clickhouse_job.py