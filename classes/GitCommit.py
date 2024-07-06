from classes.GitObject import GitObject
from functions.convert_raw_to_key_value_pairs_for_tag_and_commit import \
    convert_raw_to_key_value_pairs_for_tag_and_commit


class GitCommit(GitObject):
    object_type = b'commit'

    def set_blob_data(self, data):
        self.blob_data = data

    def get_blob_data(self):
        return self.blob_data

    def get_key_value_pairs(self):
        return convert_raw_to_key_value_pairs_for_tag_and_commit(self.blob_data)
