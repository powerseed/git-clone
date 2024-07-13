def print_out_refs_ordered_dictionary(ordered_dictionary, parent_path="refs"):
    for key, value in ordered_dictionary.items():
        if type(value) is str:
            print("{0} {1}/{2}".format(value, parent_path, key))
        else:
            print_out_refs_ordered_dictionary(value, parent_path + "/" + key)
