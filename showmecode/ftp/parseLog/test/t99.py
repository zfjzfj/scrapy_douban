#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kafka import KafkaConsumer


# consumer = KafkaConsumer(bootstrap_servers='127.0.0.1:9092',
                         # auto_offset_reset='earliest')
consumer = KafkaConsumer(bootstrap_servers='99.12.141.128:9092',
                         auto_offset_reset='earliest')
# consumer.subscribe(['LI08_A_CMB10_A3DTA_A3TXCDTAP_SRC'])
consumer.subscribe(['cmbevents'])
print consumer


for message in consumer:
    print message.value
    print message.topic
    print message.timestamp
