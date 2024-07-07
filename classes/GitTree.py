from classes.GitObject import GitObject
from functions.convert_raw_to_leaf_list_for_tree import convert_raw_to_leaf_list_for_tree


class GitTree(GitObject):
    object_type = b'tree'

    def get_leaf_list(self):
        return convert_raw_to_leaf_list_for_tree(self.blob_data)

    