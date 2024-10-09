"""StarClass module"""

from typing import List

from pydantic import BaseModel, StringConstraints, computed_field
from typing_extensions import Annotated

from config import NMSConfig
from utils.star_class_map import ODDITY_MAP, SPECTRAL_CLASS_MAP


class StarClass(BaseModel):
    """Holds data related to the class of star to be named"""

    config: NMSConfig
    spectral_class_str: Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True)]

    @computed_field
    @property
    def deity(self) -> str:
        """Computes the deity of the StarClass"""
        return SPECTRAL_CLASS_MAP[self.spectral_class_str[0].upper()][int(self.spectral_class_str[1]) // 2]

    def model_post_init(self, __context):
        """Checking the spectral class string format"""
        if 2 > len(self.spectral_class_str) > 4:
            raise ValueError("Spectral class input must be between 2 and 4 characters")
        elif self.spectral_class_str[0] not in SPECTRAL_CLASS_MAP:
            raise ValueError(f"Spectral class {self.spectral_class_str[0].upper()} does not exist")

    def generate_names(self, region: str, number: int = 10, min_len: int = 4) -> List[str]:
        """Generates potential Star full names based on Star characteristics"""
        oddities = [char.upper() for char in self.spectral_class_str[2:] if char.upper() in ODDITY_MAP]

        prefix = f"{ODDITY_MAP[oddities[0]]}-" if len(oddities) == 2 else ""
        suffix = f"-{ODDITY_MAP[oddities[-1]]}" if len(oddities) >= 1 else ""

        return {
            f"{prefix}{name}{suffix}"
            for name in self.config.generator.get_prospects(
                input_words=[self.deity, region], number=number, min_len=min_len
            )
        }
