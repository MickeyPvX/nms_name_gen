"""NMSGenerator base model"""


class NMSGenerator(object):
    """Base model for generators that generate entity names"""

    def get_prospects(self):
        """Generate potential names"""
        raise NotImplementedError()
