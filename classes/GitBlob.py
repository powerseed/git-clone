from classes.GitObject import GitObject


class GitBlob(GitObject):
    object_version = b'blob'

    def set_blob_data(self, data):
        self.blob_data = data

    def get_blob_data(self):
        return self.blob_data