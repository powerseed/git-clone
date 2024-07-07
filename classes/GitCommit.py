from classes.GitObject import GitObject
from functions.convert_raw_to_key_value_pairs_for_tag_and_commit import \
    convert_raw_to_key_value_pairs_for_tag_and_commit


class GitCommit(GitObject):
    object_type = b'commit'

    def get_key_value_pairs(self):
        return convert_raw_to_key_value_pairs_for_tag_and_commit(self.blob_data)
