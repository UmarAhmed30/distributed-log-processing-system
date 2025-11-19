FROM flink:1.18.1-scala_2.12

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN pip install apache-flink==1.18.1

USER flink
