#!/usr/bin/env python
# -*- coding: utf8 -*-


import socket
import threading
from time import ctime
import os

def action(i):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('127.0.0.1', 8888))
    # 接收欢迎消息:
    print "%s,%s" %(i,s.recv(1024))
    s.send('exit')
    print "%s is over" % i
    s.close()

for i in range(0,10):
    x = threading.Thread(target=action,args=(i,))
    x.start()
    print "%s thread is start" % i

x.join()

print "It's over!"