import configparser
import hashlib
import os
import zlib

from GitBlob import GitBlob
from GitCommit import GitCommit
from GitRepo import GitRepo
from GitTag import GitTag
from GitTree import GitTree


def get_file_path(repo, *path, is_making_directory=False):
    path = os.path.join(repo.gitdir, *path)

    if os.path.exists(path):
        if os.path.isdir(path):
            return path
        else:
            raise Exception("Path exists but is invalid: %s." % path)
    else:
        if is_making_directory:
            os.makedirs(path)
            return path
        else:
            return None


def create_new_repo(path):
    repo = GitRepo(path, True)

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception("%s is not a valid directory. " % path)
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(".git folder is not empty: %s" % repo.gitdir)
    else:
        os.makedirs(repo.worktree)

    assert get_file_path(repo, "branches", is_making_directory=True)
    assert get_file_path(repo, "objects", is_making_directory=True)
    assert get_file_path(repo, "refs", "tags", is_making_directory=True)
    assert get_file_path(repo, "refs", "heads", is_making_directory=True)

    with open(os.path.join(repo.gitdir, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    with open(os.path.join(repo.gitdir, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(os.path.join(repo.gitdir, "config"), "w") as f:
        config_parser = get_repo_default_config_parser()
        config_parser.write(f)

    return repo


def get_repo_default_config_parser():
    config_parser = configparser.ConfigParser()

    config_parser.add_section("core")
    config_parser.set("core", "repositoryformatversion", "0")
    config_parser.set("core", "filemode", "false")
    config_parser.set("core", "bare", "false")

    return config_parser


def find_root_directory(current_path, required=False):
    if os.path.isdir(os.path.join(current_path, ".git")):
        return current_path

    upper_path = os.path.join(current_path, "..")

    if current_path == upper_path:
        if required:
            raise Exception("Cannot find root directory.")
        else:
            return None

    find_root_directory(upper_path)


def object_read(repo, sha):
    path = os.path.join(repo.gitdir, "objects", sha[0:2], sha[2:])

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
            case b'commit': c = GitCommit
            case b'tree': c = GitTree
            case b'tag': c = GitTag
            case b'blob': c = GitBlob
            case _: raise Exception("Unknown type {0} for object {1}.".format(object_type.decode("ascii"), sha))

        return c(raw[index_of_null_byte + 1:])


def object_write(git_object, repo=None):
    data = git_object.serialize()

    result = git_object.object_type + b' ' + str(len(data)).encode() + b'\x00' + data

    sha = hashlib.sha1(result).hexdigest()

    if repo:
        directory = os.path.join(repo, "objects", sha[0:2])

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, sha[2:])

        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(zlib.compress(result))

    return sha





