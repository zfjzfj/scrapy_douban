from contextlib import contextmanager

@contextmanager
def make_context(status) :
    print 'enter'
    try :
        yield status
    except RuntimeError, err :
        print 'error' , err
    finally :
        print 'exit'

with make_context("ok") as value :
    print value


from contextlib import contextmanager
from contextlib import nested
from contextlib import closing

@contextmanager
def make_context(name) :
    print 'enter', name
    yield name
    print 'exit', name

with nested(make_context('A'), make_context('B')) as (a, b) :
    print a
    print b

with make_context('A') as a, make_context('B') as b :
    print a
    print b

class Door(object) :
    def open(self) :
        print 'Door is opened'
    def close(self) :
        print 'Door is closed'

with closing(Door()) as door :
    door.open()
