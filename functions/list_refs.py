import collections
import os

from functions.ref_resolve import resolve_ref


def get_refs_as_ordered_dictionary(parent_path):
    result = collections.OrderedDict()

    for file_name in sorted(os.listdir(parent_path)):
        file_path = os.path.join(parent_path, file_name)

        # It is a folder
        if os.path.isdir(file_path):
            result[file_name] = get_refs_as_ordered_dictionary(file_path)
        # It is a file.
        else:
            result[file_name] = resolve_ref(file_path)

    return result
