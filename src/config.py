"""NMS Name generator config"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Union

from pydantic import BaseModel

from azure_translator import AzureTranslator
from models.nms_generator import NMSGenerator
from models.nms_translator import NMSTranslator
from pmf_gen import PortManFaux

CONFIG_MAP = dict(translators=dict(azure=AzureTranslator), generators=dict(portmanfaux=PortManFaux))


class NMSConfig(BaseModel):
    """NMS Name generator config parser"""

    config_path: Optional[str]
    generator: NMSGenerator
    global_properties: Dict[str, Dict[str, Union[str, Dict[str, str]]]]
    translator: NMSTranslator
    translator_config: Dict[str, str]

    def __post_init__(self):
        if self.config_path is None:
            base_path = Path(__file__).parent.resolve()
            config_path = os.path.join(base_path, "nms_config.json")

        with open(file=config_path, encoding="utf-8") as config_file:
            updater = {key.lower(): val for key, val in json.load(config_file).items()}

        self.global_properties = updater["global_properties"]
        self.translator_config = updater["translators"][self.global_properties["translator"]]
        self.translator = CONFIG_MAP["translators"].get(self.global_properties["translator"])(
            config=self.translator_config
        )
        self.generator = CONFIG_MAP["generators"].get(self.global_properties["generator"])()
