def convert_key_value_pairs_to_raw_for_tag_and_commit(ordered_dictionary):
    raw = b''

    for key, value_list in ordered_dictionary.items():
        if key is None:
            continue

        for value in value_list:
            raw += key + b' ' + value.replace(b'\n', b'\n ') + b'\n'

    raw += b'\n' + ordered_dictionary[None] + b'\n'

    return raw
