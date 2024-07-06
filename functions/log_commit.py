from functions.read_object import read_object


def log_commit(gitdir, commit_sha):
    log_commit_recursion(gitdir, commit_sha, set())


def log_commit_recursion(gitdir, commit_sha, sha_of_visited_commits):
    if commit_sha in sha_of_visited_commits:
        return

    commit_object = read_object(gitdir, commit_sha)
    assert commit_object.object_type == b'commit'
    key_value_pairs = commit_object.get_key_value_pairs()

    message = key_value_pairs[None].decode("utf8").strip()
    message = message.replace("\\", "\\\\")
    message = message.replace("\"", "\\\"")

    if '\n' in message:
        message = message[:message.index('\n')]

    print("  c_{0} [label=\"{1}: {2}\"]".format(commit_sha, commit_sha[0:7], message))

    if not b'parent' in key_value_pairs.keys():
        return

    parents = key_value_pairs[b'parent']

    for parent in parents:
        log_commit_recursion(gitdir, str(parent, encoding='utf-8'), sha_of_visited_commits)
