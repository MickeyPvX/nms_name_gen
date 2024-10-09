"""NMS Name generator config"""

import json
import os
from pathlib import Path

from azure_translator import AzureTranslator
from models.nms_generator import NMSGenerator
from models.nms_translator import NMSTranslator
from models.type_validator import TypeValidator
from pmf_gen import PortManFaux

config_map = {"translators": {"azure": AzureTranslator}, "generators": {"portmanfaux": PortManFaux}}


class NMSConfig(dict):
    """NMS Name generator config parser"""

    global_properties = TypeValidator(dict)
    translator_config = TypeValidator(dict)
    translator = TypeValidator(NMSTranslator)
    generator = TypeValidator(NMSGenerator)

    def __init__(self, config_path=None):
        if config_path is None:
            base_path = Path(__file__).parent.resolve()
            config_path = os.path.join(base_path, "nms_config.json")

        with open(file=config_path, encoding="utf-8") as config_file:
            updater = {key.lower(): val for key, val in json.load(config_file).items()}
            super().__init__(**updater)

        self.global_properties = updater["global_properties"]
        self.translator_config = updater["translators"][self.global_properties["translator"]]
        self.translator = config_map["translators"].get(self.global_properties["translator"])(self.translator_config)
        self.generator = config_map["generators"].get(self.global_properties["generator"])()
