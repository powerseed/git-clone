from classes.GitObject import GitObject


class GitBlob(GitObject):
    object_type = b'blob'