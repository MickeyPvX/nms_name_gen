import json
import uuid
import requests

from os.path import dirname
from .models.type_validator import TypeValidator
from .models.typed_list import TypedList
from .models.azure_translator import AzureTranslator
from .portmanfaux import PortManFaux
from utils.translation_tools import engrishify, check_chars, get_first_syl


class PlanetName(object):

    star_name = TypeValidator(str)
    weather = TypeValidator(str)
    sentinals = TypeValidator(str)
    flora = TypeValidator(str)
    fauna = TypeValidator(str)
    generator = TypeValidator(PortManFaux)
    filepath = TypeValidator(str)
    suffix_attrs = TypedList(str)
    suffix = TypeValidator(str)
    prospects = TypeValidator(set)

    def __init__(self, **kwargs):
        self.translator = AzureTranslator()
        self.generator = PortManFaux()
        self.filepath = f'{dirname(__file__)}\\translation_map.json'
        self.suffix_attrs = ['sentinals', 'flora', 'fauna']
        self.suffix = ''
        self.__dict__.update(kwargs)

        with open(self.filepath, 'r+') as mapfile:
            self.translation_map = json.load(mapfile)

    def _map_or_translate(self, word_list: list, singleton=False):
        if not isinstance(word_list, list):
            raise TypeError(f'"{word_list}" is not a list of strings')

        word_list = [word.lower() for word in word_list]
        new_map = {
            word: get_first_syl(self.translator.translate(word))
            for word in word_list
            if self.translation_map.get(word) is None
        }

        if new_map:
            self.translation_map.update(new_map)
            with open(self.filepath, 'w') as mapfile:
                json.dump(self.translation_map, mapfile)

        if singleton:
            return self.translation_map[word_list[0]]
        else:
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
        if self.suffix == '':
            self._check_suffix_attrs()
            self.gen_suffix()

        if self.star_name is None or self.weather is None:
            raise AttributeError('Star name and planet weather are required')

        print(self.star_name, self.weather)
        weather_trans = self._map_or_translate([self.weather], singleton=True)

        self.prospects = {
            f'{prospect}-{self.suffix}'
            for prospect in self.generator.get_prospects(
                number=number,
                min_len=min_len,
                input_words=[self.star_name, weather_trans]
            )
        }

        return self.prospects
