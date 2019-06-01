#!/usr/bin/env bash

docker ps -a
docker stop redis, kafka, zookeeper
docker rm redis, kafka, zookeeper

docker run -d --name zookeeper -p 2181:2181 jplock/zookeeper
docker run -d --name kafka -p 7203:7203 -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=192.168.151.122 -e ZOOKEEPER_IP=192.168.151.122 ches/kafka
docker run -p 6379:6379 --name redis -d redis

sleep 5
docker run --rm ches/kafka kafka-topics.sh -create --topic es-data --replication-factor 1 --partitions 1 --zookeeper 192.168.151.122:2181 --config retention.ms=86400000
docker run --rm ches/kafka kafka-topics.sh -create --topic cassandra-data --replication-factor 1 --partitions 1 --zookeeper 192.168.151.122:2181 --config retention.ms=300000
