"""NMSGenerator base model"""

from typing import List, Set

from pydantic import BaseModel


class NMSGenerator(BaseModel):
    """Base model for generators that generate entity names"""

    def get_prospects(self, input_words: List[str], number: int, min_len: int) -> Set[str]:
        """Generate potential names"""
        raise NotImplementedError()
