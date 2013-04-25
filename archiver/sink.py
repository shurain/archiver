class Sink(object):
    pass

class EvernoteSink(Sink):
    def __init__(self, token):
        self.token = token

    def push(self):
        pass

class Database(Sink):
    pass