import os.path

from functions.read_object import read_object


def ls_tree(gitdir, is_recursive, tree_sha, prefix=""):
    tree_object = read_object(gitdir, tree_sha)
    leaf_list = tree_object.get_leaf_list()

    for leaf in leaf_list:
        if len(leaf.mode) == 5:
            file_type = leaf.mode[0:1]
        else:
            file_type = leaf.mode[0:2]

        match file_type:
            case b'04':
                file_type = "tree"
            case b'10':
                file_type = "blob"
            case b'12':
                file_type = "blob"
            case b'16':
                file_type = "commit"
            case _:
                raise Exception("Invalid file type %s. " % file_type)

        if is_recursive and file_type == "tree":
            ls_tree(gitdir, is_recursive, tree_sha, prefix=os.path.join(prefix, leaf.path))
        else:
            print("{0} {1} {2}\t{3}".format(
                leaf.mode.decode('ascii'),
                file_type,
                leaf.sha,
                os.path.join(prefix, leaf.path)
            ))
