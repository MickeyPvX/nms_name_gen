"""NMS Name generator config"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel

from azure_translator import AzureTranslator
from models.azure_properties import AzureProperties
from models.nms_generator import NMSGenerator
from models.nms_translator import NMSTranslator
from pmf_gen import PortManFaux


class Generator(str, Enum):
    """Enum class for types of word generators"""

    PORTMANFAUX = "portmanfaux"


class Translator(str, Enum):
    """Enum class for types of translator_properties"""

    AZURE = "azure"


class GlobalProperties(BaseModel):
    """Data model for the Global Properties section of nms_name_gen config"""

    generator: Generator
    translator: Translator


class TranslatorProperties(BaseModel):
    """Data model for the Translator Properties section of nms_name_gen config"""

    azure: Optional[AzureProperties] = None


GENERATOR_MAP = {Generator.PORTMANFAUX: PortManFaux}
TRANSLATOR_MAP = {Translator.AZURE: AzureTranslator}


class NMSConfig(BaseModel):
    """NMS Name generator config parser"""

    generator: Optional[NMSGenerator] = None
    global_properties: GlobalProperties
    translator: Optional[NMSTranslator] = None
    translator_properties: TranslatorProperties

    def model_post_init(self, __context):
        """Set the configured generator and translator"""
        self.generator = GENERATOR_MAP[self.global_properties.generator]()
        self.translator = TRANSLATOR_MAP[self.global_properties.translator](
            config=self.translator_properties.model_dump()[self.global_properties.translator]
        )
