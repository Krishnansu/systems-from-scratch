# Lesson 140 — Kafka Commands and Lab

## Start a disposable local broker

```bash
docker run -d --name sfs-kafka \
  -p 9092:9092 \
  apache/kafka:4.1.0
```

This is a single-broker learning setup, not a production cluster. If the tag is unavailable, use an available official Apache Kafka image tag.

## Open a shell

```bash
docker exec -it sfs-kafka bash
```

## Create a topic with three partitions

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic orders \
  --partitions 3 \
  --replication-factor 1
```

## Describe the topic

```bash
/opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic orders
```

## Produce records

```bash
/opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders
```

## Consume from the beginning

```bash
/opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders \
  --from-beginning
```

Try two consumers with the same group ID, then a second group ID. Observe how consumers in one group share partition assignments while separate groups independently consume the topic.

For keyed-record experiments, use a producer that supports explicit keys and inspect partition selection. A single-broker lab with replication factor 1 does not demonstrate broker-failure tolerance.

## Cleanup

```bash
docker rm -f sfs-kafka
```
