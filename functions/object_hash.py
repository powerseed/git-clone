from classes.GitBlob import GitBlob
from classes.GitCommit import GitCommit
from classes.GitTag import GitTag
from classes.GitTree import GitTree
from functions.write_object import write_object


def hash_object(file, object_type, gitdir=None):
    data = file.read()

    match object_type:
        case "commit":
            git_object = GitCommit(data)
        case "tree":
            git_object = GitTree(data)
        case "tag":
            git_object = GitTag(data)
        case "blob":
            git_object = GitBlob(data)
        case _:
            raise Exception("Unknown object type: %s" % object_type)

    return write_object(git_object, object_type, gitdir)
