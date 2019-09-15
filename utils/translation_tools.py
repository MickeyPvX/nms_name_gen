# This map associates Icelandic letters with their English pronunciations
engrish = {
    'á': 'ow',
    'ð': 'th',
    'é': 'ea',
    'í': 'e',
    'ó': 'oh',
    'ú': 'ou',
    'ý': 'ee',
    'þ': 'th',
    'æ': 'ae',
    'ö': 'eh'
}


def engrishify(word, replace_map):
    """
    A simple function for replacing characters in a string based on a replacement map

    :param word (str): the input word to modify
    :param replace_map (dict): dictionary of characters and their replacements
    :return (str):
    """
    bytes_word = word.encode('utf-8')
    for key, replace in replace_map.items():
        bytes_word = bytes_word.replace(key.encode('utf-8'), replace.encode('utf-8'))

    return bytes_word.decode('utf-8')
