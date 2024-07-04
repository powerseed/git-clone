class GitObject(object):
    def __init__(self, data: None):
        if data is None:
            self.init()
        else:
            self.deserialize(data)

    def init(self):
        pass

    def serialize(data):
        raise Exception("Unimplemented")

    def deserialize(self, data):
        raise Exception("Unimplemented")