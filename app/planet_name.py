import json

from os.path import dirname
from .models.type_validator import TypeValidator
from .portmanfaux import PortManFaux
from utils.translation_tools import engrishify, check_chars, get_first_syl
from googletrans import Translator


class PlanetName(object):

    star_name = TypeValidator(str)
    weather = TypeValidator(str)
    sentinals = TypeValidator(str)
    flora = TypeValidator(str)
    fauna = TypeValidator(str)

    def __init__(self, **kwargs):
        self.translator = Translator()
        self.generator = PortManFaux()
        self.filepath = f'{dirname(__file__)}\\translation_map.json'
        self.suffix_attrs = ['sentinals', 'flora', 'fauna']
        self.suffix = None
        self.__dict__.update(kwargs)

        with open(self.filepath, 'r+') as mapfile:
            self.translation_map = json.load(mapfile)

    def _translate(self, word, language='is'):
        translation = self.translator.translate(word, src='en', dest=language).text.lower()

        if translation == word.lower():
            raise ValueError(f'The translation service could not understand {word}')

        return engrishify(translation)

    def _map_or_translate(self, word_list: list):
        word_list = [word.lower() for word in word_list]
        new_map = {
            word: get_first_syl(self._translate(word))
            for word in word_list
            if self.translation_map.get(word) is None
        }
        self.translation_map.update(new_map)

        if new_map:
            with open(self.filepath, 'w') as mapfile:
                json.dump(self.translation_map, mapfile)

        return [self.translation_map[word] for word in word_list]

    def _check_suffix_attrs(self):
        if any([self.__dict__.get(attr) is None for attr in self.suffix_attrs]):
            raise AttributeError(f'{self.__class__.__name__} requires attributes {self.suffix_attrs}')
        else:
            return

    def gen_suffix(self, **kwargs):
        suffix_input = {k.lower(): v for k, v in kwargs.items() if k.lower() in self.suffix_attrs}
        self.__dict__.update(suffix_input)

        self._check_suffix_attrs()

        suffix_dict = dict(
            zip(
                self.suffix_attrs,
                self._map_or_translate([self.__dict__[attr] for attr in self.suffix_attrs])
            )
        )

        self.suffix = f'{suffix_dict["sentinals"].title()}{suffix_dict["flora"]}{suffix_dict["fauna"]}'

    def generate_names(self, number=10, min_len=4):
        if self.suffix is None:
            self._check_suffix_attrs()
            self.gen_suffix()

        print(self.suffix)
