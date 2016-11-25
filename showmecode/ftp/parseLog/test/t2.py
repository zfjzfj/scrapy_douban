import time
import random
import threading

class worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        t = random.randint(1,10)
        time.sleep(t)
        print "This is " + self.getName() + ";I sleep %d second."%(t)

tsk = []
for i in xrange(0,5):
    time.sleep(0.1)
    thread = worker()
    thread.setDaemon(True)
    thread.start()
    tsk.append(thread)
print "This is the end of main thread."
