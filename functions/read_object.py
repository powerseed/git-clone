import os
import zlib

from classes.GitBlob import GitBlob
from classes.GitCommit import GitCommit
from classes.GitTag import GitTag
from classes.GitTree import GitTree


def read_object(gitdir, sha):
    path = os.path.join(gitdir, "objects", sha[0:2], sha[2:])

    if not os.path.isfile(path):
        return None

    with open(path, "rb") as f:
        raw = zlib.decompress(f.read())

        index_of_white_space = raw.find(b' ')
        object_type = raw[0:index_of_white_space]

        index_of_null_byte = raw.find(b'\x00', index_of_white_space)
        size = int(raw[index_of_white_space:index_of_null_byte].decode("ascii"))

        if size != len(raw) - index_of_null_byte - 1:
            raise Exception("Malformed object {0}: bad length. ".format(sha))

        match object_type:
            case b'commit': git_object_subclass = GitCommit
            case b'tree': git_object_subclass = GitTree
            case b'tag': git_object_subclass = GitTag
            case b'blob': git_object_subclass = GitBlob
            case _: raise Exception("Unknown type {0} for object {1}.".format(object_type.decode("ascii"), sha))

        return git_object_subclass(raw[index_of_null_byte + 1:])