#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kafka import KafkaConsumer
import time

# consumer = KafkaConsumer(bootstrap_servers='127.0.0.1:9092',
                         # auto_offset_reset='earliest')
consumer = KafkaConsumer(bootstrap_servers='99.12.156.137:9092')
# consumer.subscribe(['LI08_A_CMB10_A3DTA_A3TXCDTAP_SRC'])
consumer.subscribe(['SZM00-ZM9-MON'])
print consumer


for message in consumer:
    print  time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    print message
    # print message.value
    # print message.topic