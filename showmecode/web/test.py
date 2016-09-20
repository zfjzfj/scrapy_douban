#!/usr/bin/env python


import threading

from time import ctime
import os


def action(i):
    print "%s start" % i
    os.system("curl http://127.0.0.1:8888")
    print "%s stop" % i


for i in range(0,50):
    t = threading.Thread(target=action,args=(i,))
    t.start()
t.join()
print "It's over!"



