import os.path

from functions.get_gitdir import get_gitdir


def resolve_ref(ref_file_path):
    if not os.path.isfile(ref_file_path):
        return None

    with open(ref_file_path, "r") as f:
        data = f.read()[:-1]

    if data.startswith("ref: "):
        return resolve_ref(os.path.join(get_gitdir(os.getcwd()), data[5:]))
    else:
        return data
