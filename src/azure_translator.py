"""Translator using Microsoft Azure translation API"""

from typing import Dict, Union

from requests import Request, Session

from models.nms_translator import NMSTranslator
from utils.translation_tools import engrishify


class AzureTranslator(NMSTranslator):
    """See module docstring"""

    config: Dict[str, Dict[str, Union[str, Dict[str, str]]]]

    def translate(self, text: str, from_lang="en", to_lang="is") -> str:
        """Parses function arguments into an Azure translate API request"""
        url = f'{self.config["translate_url"]}&from={from_lang}&to={to_lang}'
        body = [{"text": text}]

        headers = {
            "Ocp-Apim-Subscription-Key": self.config["translate_key"],
            "Content-Type": "application/json",
            "Content-Length": "1024",
        }

        with Session() as session:
            req = Request("POST", url=url, headers=headers, json=body)
            prepped = req.prepare()

            response = session.send(prepped).json()

        translation = {
            "from": from_lang,
            "to": to_lang,
            "input": text,
            "translation": engrishify(response[0]["translations"][0]["text"].lower()),
        }

        return translation["translation"]
