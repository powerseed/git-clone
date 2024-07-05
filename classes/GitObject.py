class GitObject(object):
    def __init__(self, data: None):
        if data is None:
            self.init()
        else:
            self.set_blob_data(data)

    def init(self):
        pass

    def set_blob_data(self, data):
        self.blob_data = data

    def get_blob_data(self):
        return self.blob_data
