import json


class NMSConfig(dict):

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = 'nms_config.json'

        with open('nms_config.json') as config_file:
            updater = {key.lower(): val for key, val in json.load(config_file).items()}
            super().__init__(**updater)
