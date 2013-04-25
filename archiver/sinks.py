class Sink(object):
    pass

class EvernoteSink(Sink):
    def __init__(self, token):
        self.token = token

class Database(Sink):
    pass