def leaf_sort_key(leaf):
    if leaf.mode.startswith(b'10'):
        return leaf.path
    else:
        return leaf.path + b'/'


def convert_leaf_list_to_raw_for_tree(leaf_list):
    leaf_list.items.sort(key=leaf_sort_key)

    raw = b''

    for leaf in leaf_list.items:
        path = leaf.path.encode("utf8")
        sha = int(leaf.sha, 16)
        sha = sha.to_bytes(20, "big")

        raw += leaf.mode + b' ' + path + b'\x00' + sha

    return raw
