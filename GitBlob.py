from GitObject import GitObject


class GitBlob(GitObject):
    def __init__(self, data):
        super().__init__(data)