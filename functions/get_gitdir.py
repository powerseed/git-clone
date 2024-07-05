import os
import sys


def get_gitdir(current_path, required=False):
    current_gitdir = os.path.join(current_path, ".git")

    if os.path.isdir(current_gitdir):
        return current_gitdir

    upper_path = os.path.join(current_path, "..")
    upper_path = os.path.realpath(upper_path)

    if current_path == upper_path:
        if required:
            raise Exception("Cannot find root directory.")
        else:
            return None

    return get_gitdir(upper_path)
