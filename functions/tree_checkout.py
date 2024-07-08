import os

from functions.read_object import read_object


def tree_checkout(gitdir, tree_object, path):
    leaf_list = tree_object.get_leaf_list()

    for leaf in leaf_list:
        git_object = read_object(gitdir, leaf.sha)
        dest = os.path.join(path, leaf.path)

        if git_object.object_type == b'tree':
            os.makedirs(dest)
            tree_checkout(gitdir, git_object, dest)
        elif git_object.object_type == b'blob':
            with open(dest, 'wb') as f:
                f.write(git_object.get_blob_data())
