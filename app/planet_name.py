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

    def __init__(self, star_name, weather, sentinals='standard', flora='standard', fauna='standard'):
        self.star_name = star_name
        self.weather = weather
        self.translator = Translator()

    def _translate(self, word, language='is'):
        translation = self.translator.translate(word, dest=language).text.lower()

        if translation == word.lower():
            raise ValueError(f'The translation service could not understand {word}')

        return translation
    
    def generate_names(self):
        pass
