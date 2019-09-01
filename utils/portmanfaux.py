from app.models.type_validator import TypeValidator
from app.models.typed_list import TypedList
from random import randint


class PortManFaux(object):
    """
    As opposed to a true portmanteau where the sound and meaning of two words are blended, this
    portman-faux programmatically generates combinations of two inputs with no real logic as to
    their combined meaning.  Oh well.

    :param input_words (list): the words to smash together
    """

    input_words = TypedList(str)
    prospects = TypeValidator(set)
    faux_list = TypedList(str)

    def __init__(self, input_words=[]):
        self.input_words = input_words
        self.prospects = set()
        self.faux_list = []

        if len(input_words) > 0:
            self._gen_faux()

    def _gen_faux(self):
        """
        Generates all possible word combinations
        """
        if len(self.input_words) != 2:
            # Currently only working on 2 words at a time
            raise ValueError(f'input_words: {self.input_words} is not a list with len() == 2')
        else:
            w1 = self.input_words[0]
            w2 = self.input_words[1]

            for x in range(1, len(w1)):
                for y in range(1, len(w2)):
                    self.faux_list.append(f'{w1[:-x]}{w2[y:]}')
                    self.faux_list.append(f'{w2[:-y]}{w1[x:]}')

    def get_prospects(self, number=10, min_len=4):
        """
        Selects n portman-faux words at random

        :param number (int): number of words to select
        :param min_len (int): minimum length of the words to select
        :return (set):
        """
        filtered_list = [prospect.title() for prospect in self.faux_list if len(prospect) >= min_len]
        num_possible = len(filtered_list)

        if num_possible == 0:
            print(f'No words can be generated with a minimum length of {min_len}')
            return
        elif num_possible < number:
            print(
                f'Only {num_possible} of the {number} requested words can be generated with a minimum length of {min_len}'
            )
            self.prospects = set(filtered_list)
        else:
            self.prospects.clear()

            while len(self.prospects) < number:
                self.prospects.add(filtered_list[randint(0, len(filtered_list) - 1)])

        return self.prospects
