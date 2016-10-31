#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, logging, time
from kafka import KafkaConsumer, KafkaProducer


class Producer(threading.Thread):
    # daemon = True
    def run(self):
        producer = KafkaProducer(bootstrap_servers='99.12.156.134:9092')
        while True:
            producer.send('my-topic', b"test")
            producer.send('my-topic', b"\xc2Hola, mundo!")
            time.sleep(1)


class Consumer(threading.Thread):
    # daemon = True
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='99.12.156.134:9092',
                                 auto_offset_reset='earliest')
        consumer.subscribe(['SZM00-ZM9-MON'])
        for message in consumer:
            logging.info message.value
            logging.info message.topic
            logging.info message.timestamp
            logging.info(message.offset)
            logging.info(type(message.value))
            # print (message)

def main():
    threads = [
        #Producer(),
        Consumer()
    ]

    for t in threads:
        t.start()

if __name__ == "__main__":
    logging.basicConfig(
        format = '%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO,
        filename = "test.log"
        )
    main()
