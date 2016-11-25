#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, logging, time
from kafka import KafkaConsumer, KafkaProducer
import yaml
import os
import json

class Config(object):

    @classmethod
    def getConfig(cls,configFile = "config.yaml"):
        if not os.path.exists(configFile):
            return None
        file = open(configFile)
        config = yaml.load(file)
        return config


# print getConfig()

class Producer(threading.Thread):
    daemon = True
    def run(self):
        producer = KafkaProducer(bootstrap_servers='99.12.156.134:9092')
        producer.send('SZM00-ZM9-MON', b'{"hello":"world"}')
        # time.sleep(1)
        # print "I am over!"


class Consumer(threading.Thread):
    daemon = True
    def __init__(self):
        threading.Thread.__init__(self)
        config = Config.getConfig()
        topic = config['kafka']['Server1']['topic'][0]
        ip = config['kafka']['Server1']['ip']
        port = config['kafka']['Server1']['port']
        self.consumer = KafkaConsumer(bootstrap_servers=('%s:%s' % (ip,port)),
                                 auto_offset_reset='latest')
        self.consumer.subscribe([topic])

    def parseErrorLog(self):
        for message in self.consumer:
            try:
                value = json.loads(message.value)
            except:
                continue
            if not value.has_key('BODY'): continue
            logLevel = value['BODY']
            print ("*" * 100)
            print logLevel.keys()
            if logLevel.has_key('$ERRORLOG$'):
                print (logLevel['$ERRORLOG$'][0]['xLogLvl'])
                logging.info (logLevel['$ERRORLOG$'][0]['xLogLvl'])
                logging.info(logLevel['$ERRORLOG$'][0]['xLogLvl'])
                logging.info(logLevel)
            print ("*" * 100)
            # logging.info (message.value)
            # logging.info (message.topic)
            # logging.info (message.timestamp)
            # logging.info(message.offset)
            # logging.info(type(message.value))
            # print (message)

    def run(self):
        self.parseErrorLog()


def main():
    threads = [
        # Producer(),
        Consumer()
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    logging.basicConfig(
        format = '%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO,
        filename = "test.log"
        )
    main()
