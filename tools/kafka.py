import os
import logging
import confluent_kafka
from threading import Thread
from typing import List
# Export exception class
KafkaException = confluent_kafka.KafkaException
Message = confluent_kafka.Message


class Consumer:
    def __init__(self, configs, topics, callback):
        logging.info('Kafka consumer starting on topics {}...'.format(topics))
        self._consumer = confluent_kafka.Consumer(configs)
        self._topics = topics
        self._callback = callback
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        self._consumer.subscribe(self._topics)
        while not self._cancelled:
            msg = self._consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                self._callback(msg)

    def close(self):
        logging.info('Kafka consumer closing...')
        self._cancelled = True
        self._consumer.close()
        self._poll_thread.join()


class Producer:
    def __init__(self, configs):
        logging.info('Kafka producer starting...')
        self._producer = confluent_kafka.Producer(configs)
        self._cancelled = False
        self._poll_thread = Thread(target=self._poll_loop)
        self._poll_thread.start()

    def _poll_loop(self):
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self):
        logging.info('Kafka producer closing...')
        self._cancelled = True
        self._poll_thread.join()

    def produce(self, topic, value, on_delivery=None):
        self._producer.produce(topic, value, on_delivery=on_delivery)


consumers: List[Consumer] = []
producer: Producer = None


def add_consumer(topics, callback):
    global consumers
    consumers.append(
        Consumer({
            "bootstrap.servers": os.getenv('KAFKA_URL'),
            "group.id": os.getenv('KAFKA_CONSUMER_GROUP')
        }, topics, callback)
    )


def close():
    global consumers, producer
    if producer:
        producer.close()
    for consumer in consumers:
        consumer.close()


def get_producer() -> Producer:
    global producer
    return producer


def create_producer():
    global producer
    producer = Producer({
        "bootstrap.servers": os.getenv('KAFKA_URL')
    })
