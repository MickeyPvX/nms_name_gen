import json

from app.models.type_validator import TypeValidator
from app.models.nms_translator import NMSTranslator
from app.models.nms_generator import NMSGenerator
from app.azure_translator import AzureTranslator
from app.pmf_gen import PortManFaux

config_map = {
    'translators': {
        'azure': AzureTranslator
    },
    'generators': {
        'portmanfaux': PortManFaux
    }
}


class NMSConfig(dict):

    global_properties = TypeValidator(dict)
    translator_config = TypeValidator(dict)
    translator = TypeValidator(NMSTranslator)
    generator = TypeValidator(NMSGenerator)

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = 'nms_config.json'

        with open('nms_config.json') as config_file:
            updater = {key.lower(): val for key, val in json.load(config_file).items()}
            super().__init__(**updater)

        self.global_properties = updater['global_properties']
        self.translator_config = updater['translators'][self.global_properties['translator']]
        self.translator = config_map['translators'].get(self.global_properties['translator'])(self.translator_config)
        self.generator = config_map['generators'].get(self.global_properties['generator'])()
