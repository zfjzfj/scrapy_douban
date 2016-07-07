class Chain(object):

    def __init__(self, path=''):
        self._path = path
	print "xxxl",self._path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path


print Chain().status.user.timeline.list

