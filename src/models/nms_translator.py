"""NMSTranslator base model"""


class NMSTranslator(object):
    """Base model for translators"""

    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """Translates from_lang string to to_lang string"""
        raise NotImplementedError()
