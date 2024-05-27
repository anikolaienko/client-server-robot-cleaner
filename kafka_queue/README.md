# Useful docs:
* Image docs: https://hub.docker.com/r/bitnami/kafka
* Client tutorial: https://www.conduktor.io/kafka/kafka-consumer-cli-tutorial


# Pull image
```bash
docker pull bitnami/kafka:3.7.0
```

# Run server
```bash
docker compose up
```

# Run client
```bash
docker run -it --rm --network kafka_queue_app-tier bitnami/kafka:3.7.0 /bin/bash

# or just create topic
docker run -it --rm --network kafka_queue_app-tier bitnami/kafka:3.7.0 kafka-topics.sh --create --topic commands --bootstrap-server kafka-server:9092

# or just run producer
docker run -it --rm --network kafka_queue_app-tier bitnami/kafka:3.7.0 kafka-console-producer.sh --topic commands --bootstrap-server kafka-server:9092
```

# Kafla client command
```bash
# create topics
kafka-topics.sh --create --topic commands --bootstrap-server kafka-server:9092
kafka-topics.sh --create --topic errors --bootstrap-server kafka-server:9092

# list topics
kafka-topics.sh --list --bootstrap-server kafka-server:9092

# run produce
kafka-console-producer.sh --topic commands --bootstrap-server kafka-server:9092

# run consumer
kafka-console-consumer.sh --topic commands --bootstrap-server kafka-server:9092

# All available:
kafka-topics.sh
kafka-configs.sh
kafka-console-consumer.sh
kafka-console-producer.sh
kafka-avro-console-consumer.sh
kafka-avro-console-producer.sh
kafka-verifiable-consumer.sh
kafka-verifiable-producer.sh
kafka-preferred-replica-election.sh
kafka-replica-verification.sh
kafka-reassign-partitions.sh
kafka-broker-api-versions.sh
kafka-consumer-groups.sh
kafka-delete-records.sh
kafka-log-dirs.sh
kafka-dump-log.sh
kafka-acls.sh
ksql.sh
```
