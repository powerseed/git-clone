from classes.GitObject import GitObject


class GitTag(GitObject):
    def __init__(self, data):
        super().__init__(data)