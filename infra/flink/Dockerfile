FROM flink:1.18.1-scala_2.12

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN pip install apache-flink==1.18.1

COPY connectors/flink-connector-kafka-1.17.1.jar /opt/flink/lib/
COPY connectors/flink-connector-jdbc-3.1.0-1.17.jar /opt/flink/lib/
COPY connectors/clickhouse-jdbc-0.6.0-all.jar /opt/flink/lib/
COPY connectors/flink-json-1.17.1.jar /opt/flink/lib/
COPY connectors/kafka-clients-3.2.3.jar /opt/flink/lib/
COPY connectors/flink-connector-clickhouse-1.17-0.1.1-all.jar /opt/flink/lib/
COPY connectors/flink-shaded-guava-30.1.1-jre-16.1.jar /opt/flink/lib/

USER flink
