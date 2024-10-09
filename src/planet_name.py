"""NMS Planet name class"""

import json
from os import path

from config import NMSConfig
from models.type_validator import TypeValidator
from models.typed_list import TypedList
from utils.translation_tools import get_first_syl, map_or_translate


class PlanetName(object):
    """Class for holding Planet naming data"""

    config = TypeValidator(dict)
    star_name = TypeValidator(str)
    weather = TypeValidator(str)
    sentinals = TypeValidator(str)
    flora = TypeValidator(str)
    fauna = TypeValidator(str)
    filepath = TypeValidator(str)
    suffix_attrs = TypedList(str)
    suffix = TypeValidator(str)
    prospects = TypeValidator(set)

    def __init__(self, **kwargs):
        self.config = NMSConfig()
        self.filepath = path.join(f"{path.dirname(__file__)}", "translation_map.json")
        self.suffix_attrs = ["sentinals", "flora", "fauna"]
        self.suffix = ""
        self.__dict__.update(kwargs)

        with open(file=self.filepath, mode="r+", encoding="utf-8") as mapfile:
            self.translation_map = json.load(mapfile)

    def _check_suffix_attrs(self) -> None:
        """Checks if the necessary attributes have been given to generate a Planet name suffix"""
        if any([self.__dict__.get(attr) is None for attr in self.suffix_attrs]):
            raise AttributeError(f"{self.__class__.__name__} requires attributes {self.suffix_attrs}")

    def _update_translations(self, update_map):
        """If a new translation happened, update the translation map file for persistence"""
        self.translation_map.update(update_map)

        with open(file=self.filepath, mode="r+", encoding="utf-8") as mapfile:
            json.dump(
                self.translation_map,
                mapfile,
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )

    def gen_suffix(self):
        """Generates a Planet name suffix based on Planet characteristics"""
        self._check_suffix_attrs()

        suffix_dict = map_or_translate(
            [self.__dict__[attr] for attr in self.suffix_attrs],
            self.translation_map,
            self.config.translator,
        )
        self._update_translations(suffix_dict)

        self.suffix = (
            f"{get_first_syl(suffix_dict[self.sentinals]).title()}"
            f"{get_first_syl(suffix_dict[self.flora])}"
            f"{get_first_syl(suffix_dict[self.fauna])}"
        )

    def generate_names(self, number=10, min_len=4, extreme=False):
        """Generate potential Planet full names based on Planet characteristics"""
        if self.suffix == "":
            self._check_suffix_attrs()
            self.gen_suffix()

        if self.star_name is None or self.weather is None:
            raise AttributeError("Star name and planet weather are required")

        weather_trans = map_or_translate(self.weather, self.translation_map, self.config.translator)
        self._update_translations(weather_trans)

        ex = "Ex-" if extreme else ""

        self.prospects = {
            f"{ex}{prospect}-{self.suffix}"
            for prospect in self.config.generator.get_prospects(
                number=number,
                min_len=min_len,
                input_words=[self.star_name, weather_trans[self.weather]],
            )
        }

        return self.prospects
