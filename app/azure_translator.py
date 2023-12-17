from requests import Session, Request
from utils.translation_tools import engrishify

from .models.typed_list import TypedList
from .models.type_validator import TypeValidator
from .models.nms_translator import NMSTranslator


class AzureTranslator(NMSTranslator):

    config = TypeValidator(dict)
    headers = TypeValidator(dict)
    response = TypedList(dict)
    translation = TypeValidator(dict)

    def __init__(self, config):
        self.config = config
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.config['translate_key'],
            'Content-Type': 'application/json',
            'Content-Length': '1024'
        }

    def translate(self, text: str, from_lang='en', to_lang='is'):
        url = f'{self.config["translate_url"]}&from={from_lang}&to={to_lang}'
        body = [{'text': text}]

        with Session() as session:
            req = Request('POST', url=url, headers=self.headers, json=body)
            prepped = req.prepare()

            self.response = session.send(prepped).json()

        self.translation = {
            'from': from_lang,
            'to': to_lang,
            'input': text,
            'translation': engrishify(self.response[0]['translations'][0]['text'].lower())
        }

        return self.translation['translation']
