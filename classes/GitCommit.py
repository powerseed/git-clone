from classes.GitObject import GitObject


class GitCommit(GitObject):
    def __init__(self, data):
        super().__init__(data)