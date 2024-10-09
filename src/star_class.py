"""StarClass module"""

from config import NMSConfig
from models.type_validator import TypeValidator
from models.typed_list import TypedList
from utils.star_class_map import ODDITY_MAP, SPECTRAL_CLASS_MAP


class StarClass(object):
    """Holds data related to the class of star to be named"""

    config = TypeValidator(dict)
    spectral_class_str = TypeValidator(str)
    spectral_class = TypeValidator(str)
    brightness = TypeValidator(int)
    oddities = TypedList(str)

    def __init__(self, spectral_class):
        self.config = NMSConfig()
        self.spectral_class_str = spectral_class.upper()
        self.spectral_class = self.spectral_class_str[0]
        self.oddities = []

        if 2 > len(self.spectral_class_str) > 4:
            raise ValueError("Spectral class input must be between 2 and 4 characters")
        elif self.spectral_class not in SPECTRAL_CLASS_MAP:
            raise ValueError(f"Spectral class {self.spectral_class_str[0].upper()} does not exist")

        self.brightness_index = int(self.spectral_class_str[1]) // 2
        self.deity = SPECTRAL_CLASS_MAP[self.spectral_class][self.brightness_index]

        if len(self.spectral_class_str) > 2:
            for char in self.spectral_class_str[2:]:
                if char.upper() not in ODDITY_MAP:
                    print(f'"{char.upper()}" not a recognized oddity code; ignoring...')
                elif char.upper() not in self.oddities:
                    self.oddities.append(char.upper())

    def generate_names(self, region, number=10, min_len=4):
        """Generates potential Star full names based on Star characteristics"""
        prefix = f"{ODDITY_MAP[self.oddities[0]]}-" if len(self.oddities) == 2 else ""
        suffix = f"-{ODDITY_MAP[self.oddities[-1]]}" if len(self.oddities) >= 1 else ""

        return {
            f"{prefix}{name}{suffix}"
            for name in self.config.generator.get_prospects(
                input_words=[self.deity, region], number=number, min_len=min_len
            )
        }
