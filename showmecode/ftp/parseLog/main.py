#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, logging, time
from kafka import KafkaConsumer, KafkaProducer
import yaml
import os
import json
import sys
import pymongo


reload(sys)
sys.setdefaultencoding('utf8')



EVENTNAMES = ["WKEPFM","APPIST","THDSTS","DBPOOL","PRCDAT","TCPTHD","QUEPFM",\
"LTPPFM","PFMDAT"  ]

class Config(object):

    @classmethod
    def getConfig(cls,configFile = "config.yaml"):
        if not os.path.exists(configFile):
            return None
        file = open(configFile)
        config = yaml.load(file)
        return config


class Events(threading.Thread):
    daemon = True
    def __init__(self,tableName,record):
        threading.Thread.__init__(self)
        self.tableName = tableName
        self.record = record
        config = Config.getConfig()
        self.dbName = config['mongodb']['Server1']['dbname']
        self.ip = config['mongodb']['Server1']['ip']
        self.port = config['mongodb']['Server1']['port']
        logging.info ("%s insert a record" % self.tableName)
        # print ("%s insert a record" % self.tableName)

    def getDB(self):
        # 建立连接
        client = pymongo.MongoClient(host=self.ip, port=self.port)
        db = client[self.dbName]
        #或者 db = client.example
        return db

    def getCollection(self):
        # 选择集合（mongo中collection和database都是延时创建的）
        db = self.getDB()
        coll = db[self.tableName]
        # print db.collection_names()
        return coll

    def insertMultiDocs(self):
        # 批量插入documents,插入一个数组
        coll = self.getCollection()
        # information = [{"name": "xiaoming", "age": "25"}, {"name": "xiaoqiang", "age": "24"}]
        # print self.record
        recordID = coll.insert(self.record)
        return recordID


    def run(self):
        # pass
        self.insertMultiDocs()


class Producer(threading.Thread):
    daemon = True

    def __init__(self,syslog):
        threading.Thread.__init__(self)
        config = Config.getConfig()
        self.topic = config['kafka']['Producer1']['topic']
        self.ip = config['kafka']['Producer1']['ip']
        self.port = config['kafka']['Producer1']['port']
        self.producer = KafkaProducer(bootstrap_servers = '%s:%s' % (self.ip,self.port),\
                acks = 1)
        self.syslog = syslog

    def run(self):
        # pass
        print "starting to send  cmbevents..."
        print self.syslog
        future = self.producer.send(self.topic,value=self.syslog.encode("utf-8"),\
                partition = 1)
        # record_metadata = future.get(timeout=10)
        # print record_metadata.offset,record_metadata.topic,record_metadata.partition
        print "end to send  cmbevents..."

class Consumer(threading.Thread):
    daemon = True
    def __init__(self):
        threading.Thread.__init__(self)
        config = Config.getConfig()
        self.topic = config['kafka']['Consumer1']['topic']
        self.ip = config['kafka']['Consumer1']['ip']
        self.port = config['kafka']['Consumer1']['port']
        self.warnTimes = config['logWarnCount']
        self.consumer = KafkaConsumer(bootstrap_servers=('%s:%s' % (self.ip,self.port)),
                                 auto_offset_reset='largest')
        self.consumer.subscribe([self.topic])

    @property
    def eventName(self):
        return self._eventName

    @eventName.setter
    def eventName(self,value):
        self._eventName = "$%s$" % value


    def Insert2DB(self):
        for event in EVENTNAMES:
            self.eventName = event
            if self.logLevel.has_key(self.eventName):
                record = self.logLevel[self.eventName]
                e = Events(event,record)
                e.start()
                e.join()


    def parseLog(self):
        count = 0
        for message in self.consumer:
            logging.info (("kafka offset %s has been processed!") % (message.offset))
            # print message
            try:
                value = json.loads(message.value)
            except:
                continue
            if not value.has_key('BODY'): continue
            self.logLevel = value['BODY']
            if not self.logLevel.has_key('$ERRORLOG$'):
                self.Insert2DB()
            else:
                logInfo = self.logLevel['$ERRORLOG$']
                for item in logInfo:
                    errTime = item['xLogTim'][0:19]
                    if int(item["xLogLvl"]) <= 1:
                        sysLogLevel = 1
                        # Error Log is not successive.
                        count = 0
                    elif int(item["xLogLvl"]) == 3:
                        sysLogLevel = 2
                        # Error Log is not successive.
                        count = 0
                    elif int(item["xLogLvl"]) == 4:
                        sysLogLevel = 3
                        # Error Log is not successive.
                        count = 0
                    else:
                        count += 1
                        if count >= self.warnTimes:
                            sysLogLevel = 2
                        else:
                            sysLogLevel = 1

                    syslog = "|_|Kafka|BusinessApp|ERRORLOG|%s|%s|kafka_errorlog|1|%s|%s|%s\
|##|Kafka|##|%s|0|0|0|0|一线-开放业务管理|_|" % (self.topic,self.ip,\
    errTime,item['xLogMsg'],item['xErrCod'],sysLogLevel)
                    print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
                    p = Producer(syslog)
                    p.start()
                    # p.join()
                    print "=" * 180




    def run(self):
        self.parseLog()


def main():
    t = Consumer()
    t.start()
    t.join()

    # e = Events('tablename_test1')
    # e.start()
    # e.join()
    # for i in range(1,10):
        # p = Producer("fake syslog" + str(i))
        # p.start()
        # p.join()

if __name__ == "__main__":
    logging.basicConfig(
        format = '%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO,
        filename = "test.log"
        )
    main()
