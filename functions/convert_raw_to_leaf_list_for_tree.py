from classes.GitTreeLeaf import GitTreeLeaf


def convert_raw_to_leaf_list_for_tree(raw):
    length = len(raw)
    current_index = 0
    git_tree_leaf_list = list()

    while current_index < length:
        current_index, git_tree_leaf = convert_raw_to_object_for_one_leaf(raw, current_index)
        git_tree_leaf_list.append(git_tree_leaf)

    return git_tree_leaf_list


def convert_raw_to_object_for_one_leaf(raw, start_index):
    index_of_whitespace = raw.index(b' ', start_index)
    assert index_of_whitespace - start_index == 5 or index_of_whitespace - start_index == 6

    mode = raw[start_index:index_of_whitespace]
    if len(mode) == 5:
        mode = b' ' + mode

    index_of_null = raw.index(b'\x00', index_of_whitespace)
    path = raw[index_of_whitespace + 1:index_of_null]
    path = path.decode('utf8')

    sha = raw[index_of_null + 1:index_of_null + 21]
    sha = int.from_bytes(sha, "big")
    sha = format(sha, "040x")

    return index_of_null + 21, GitTreeLeaf(mode, path, sha)
