import os


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
