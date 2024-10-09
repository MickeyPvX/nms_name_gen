"""NMS Planet name class"""

import json
from os import path
from typing import Dict, Optional

from pydantic import BaseModel, computed_field

from config import NMSConfig
from utils.translation_tools import get_first_syl, map_or_translate


class PlanetName(BaseModel):
    """Class for holding Planet naming data"""

    config: NMSConfig
    fauna: str
    filepath: Optional[str] = None
    flora: str
    sentinals: str
    star_name: str
    suffix: str = ""
    weather: str

    @computed_field
    @property
    def translation_map(self) -> Dict[str, str]:
        """Checking that we can load the translation map"""
        if self.filepath is None:
            self.filepath = path.join(f"{path.dirname(__file__)}", "translation_map.json")
        with open(file=self.filepath, mode="r+", encoding="utf-8") as mapfile:
            return json.load(mapfile)

    def _update_translations(self, update_map):
        """If a new translation happened, update the translation map file for persistence"""
        self.translation_map.update(update_map)

        with open(file=self.filepath, mode="r+", encoding="utf-8") as mapfile:
            json.dump(
                self.translation_map,
                mapfile,
                sort_keys=True,
                indent=2,
                separators=(",", ": "),
            )

    def gen_suffix(self):
        """Generates a Planet name suffix based on Planet characteristics"""
        suffix_dict = map_or_translate(
            [self.sentinals, self.flora, self.fauna],
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
            self.gen_suffix()

        if self.star_name is None or self.weather is None:
            raise AttributeError("Star name and planet weather are required")

        weather_trans = map_or_translate(self.weather, self.translation_map, self.config.translator)
        self._update_translations(weather_trans)

        ex = "Ex-" if extreme else ""

        prospects = {
            f"{ex}{prospect}-{self.suffix}"
            for prospect in self.config.generator.get_prospects(
                number=number,
                min_len=min_len,
                input_words=[self.star_name, weather_trans[self.weather]],
            )
        }

        return prospects
