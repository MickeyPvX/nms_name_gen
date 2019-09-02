from .type_validator import TypeValidator
from .typed_list import TypedList
from utils.star_class_map import spectral_class_map, oddity_map
from app.portmanfaux import PortManFaux


class StarClass(object):

    spectral_class_str = TypeValidator(str)
    spectral_class = TypeValidator(str)
    brightness = TypeValidator(int)
    oddities = TypedList(str)

    def __init__(self, spectral_class):
        self.spectral_class_str = spectral_class
        self.spectral_class = self.spectral_class_str[0].upper()
        self.oddities = []

        if 2 > len(self.spectral_class_str) > 4:
            raise ValueError('Spectral class input must be between 2 and 4 characters')
        elif self.spectral_class not in spectral_class_map:
            raise ValueError(f'Spectral class {self.spectral_class_str[0].upper()} does not exist')

        self.brightness = int(self.spectral_class_str[1])

        if len(self.spectral_class_str) > 2:
            for char in self.spectral_class_str[2:]:
                if char.upper() not in oddity_map:
                    print(f'"{char.upper()}" not a recognized oddity code; ignoring...')
                elif char.upper() not in self.oddities:
                    self.oddities.append(char.upper())

    def generate_names(self, region, number=10, min_len=4):
        brightness_index = self.brightness // 2
        deity_name = spectral_class_map[self.spectral_class][brightness_index]
        prefix = f'{oddity_map[self.oddities[0]]}-' if len(self.oddities) == 2 else ''
        suffix = f'-{oddity_map[self.oddities[-1]]}' if len(self.oddities) >= 1 else ''

        name_gen = PortManFaux(input_words=[deity_name, region])

        return {f'{prefix}{name}{suffix}' for name in name_gen.get_prospects()}
