import collections


def convert_raw_to_key_value_pairs_for_tag_and_commit(raw, start_index=0, ordered_dictionary=None):
    if not ordered_dictionary:
        ordered_dictionary = collections.OrderedDict()

    index_of_next_whitespace = raw.find(b' ', start_index)
    index_of_next_newline = raw.find(b'\n', start_index)

    if index_of_next_newline == start_index:
        commit_message = raw[index_of_next_newline+1:]
        ordered_dictionary[None] = commit_message
        return ordered_dictionary

    key = raw[start_index:index_of_next_whitespace]

    end_index = start_index
    while True:
        end_index = raw.find(b'\n', end_index + 1)
        if raw[end_index + 1] != ord(' '):
            break

    value = raw[index_of_next_whitespace + 1:end_index].replace(b'\n ', b'\n')

    if key in ordered_dictionary:
        ordered_dictionary[key].append(value)
    else:
        ordered_dictionary[key] = [value]

    return convert_raw_to_key_value_pairs_for_tag_and_commit(raw, start_index=end_index + 1, ordered_dictionary=ordered_dictionary)



