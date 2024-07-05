import sys

from functions.find_git_object import find_git_object
from functions.read_object import read_object


def cat_file(gitdir, object_type, object_name):
    sha = find_git_object(gitdir, object_name, object_type)
    git_object = read_object(gitdir, sha)
    sys.stdout.buffer.write(git_object.get_blob_data())
