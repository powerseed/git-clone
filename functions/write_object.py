import hashlib
import os
import zlib


def write_object(git_object, object_type, gitdir=None):
    data = git_object.get_blob_data()

    result = object_type.encode() + b' ' + str(len(data)).encode() + b'\x00' + data

    sha = hashlib.sha1(result).hexdigest()

    if gitdir:
        directory = os.path.join(gitdir, "objects", sha[0:2])

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, sha[2:])

        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(zlib.compress(result))

    return sha
