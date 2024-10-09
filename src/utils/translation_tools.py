"""Tools for translating from Icelandic"""

from typing import Dict, Iterable, List, Union

from models.nms_translator import NMSTranslator

DUPLETS = {"th", "sh", "ch", "ph", "rh", "sk", "ll"}
# This map associates Icelandic letters with their English pronunciations
ENGRISH = {"á": "ow", "ð": "th", "é": "ea", "í": "e", "ó": "oh", "ú": "ou", "ý": "ee", "þ": "th", "æ": "ae", "ö": "eh"}
VOWELS = "aeiouy"


def engrishify(word: str) -> str:
    """
    A simple function for replacing characters in a string based on a replacement map

    :param word (str): the input word to modify
    :param replace_map (dict): dictionary of characters and their replacements
    :return (str):
    """
    bytes_word = word.encode("utf-8")
    for key, replace in ENGRISH.items():
        bytes_word = bytes_word.replace(key.encode("utf-8"), replace.encode("utf-8"))

    return bytes_word.decode("utf-8")


def check_chars(word: str, check_str: str) -> List[bool]:
    """
    Checks an input word's characters to see if they are in check_str

    :param word (str): word to check
    :param check_str (str): string to compare
    :return (list[bool]):
    """
    return [char in check_str for char in word]


def get_first_syl(word: str) -> str:
    """
    Horribly naive way to find the first syllable of any word

    :param word (str): word to parse out the first syllable
    :return (str):
    """
    vowel_check = check_chars(word, VOWELS)
    for n, _ in enumerate(vowel_check):
        if vowel_check[n]:
            if vowel_check[n + 1]:
                continue
            elif len(word) == n + 2:
                return word
            elif vowel_check[n + 2]:
                return word[: n + 2]
            elif word[n + 1 : n + 3] in DUPLETS:
                if len(word) == n + 3:
                    return word
                elif vowel_check[n + 3]:
                    return word[: n + 3]
                else:
                    return word[: n + 3]
            else:
                if len(word) == n + 3:
                    return word
                elif vowel_check[n + 3]:
                    return word[: n + 2]
                elif word[n + 2 : n + 4] in DUPLETS:
                    return word[: n + 2]
                else:
                    return word[: n + 3]


def map_or_translate(
    words: Union[Iterable[str], str], translation_map: Dict[str, str], translator: NMSTranslator
) -> Dict[str, str]:
    """
    Determines if a translation has already been done and stored in the translation map,
    or if we need to reach out to the translator API to do a new translation
    :return (dict): {<word>: <translation>}
    """
    if isinstance(words, str):
        words = {words}

    words = {word.lower() for word in words}

    return {word: translation_map.get(word, translator.translate(word)) for word in words}
