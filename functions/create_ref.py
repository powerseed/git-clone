import os.path


def create_ref(gitdir, file_path, sha_object_referred_to):
    with open(os.path.join(gitdir, file_path), 'w') as f:
        f.write(sha_object_referred_to + "\n")
