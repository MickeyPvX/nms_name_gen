"""Portmanfaux generator class"""

from typing import List, Set

from models.nms_generator import NMSGenerator


class PortManFaux(NMSGenerator):
    """
    As opposed to a true portmanteau where the sound and meaning of two words are blended, this
    portman-faux programmatically generates combinations of two inputs with no real logic as to
    their combined meaning.  Oh well.

    :param input_words (list): the words to smash together
    """

    def _gen_faux(self, input_words: List[str]):
        """
        Generates all possible word combinations
        """
        if len(input_words) != 2:
            # Currently only working on 2 words at a time
            raise ValueError(f"input_words: {input_words} is not a list with len() == 2")
        else:
            for x in range(1, len(input_words[0])):
                for y in range(1, len(input_words[1])):
                    yield f"{input_words[0][:-x]}{input_words[1][y:]}"
                    yield f"{input_words[1][:-y]}{input_words[0][x:]}"

    def get_prospects(self, input_words: List[str], number: int = 10, min_len: int = 4) -> Set[str]:
        """
        Selects n portman-faux words at random

        :param number (int): number of words to select
        :param min_len (int): minimum length of the words to select
        :return (generator):
        """
        prospects = set()

        filtered_set = {
            prospect.title() for prospect in self._gen_faux(input_words=input_words) if len(prospect) >= min_len
        }
        num_possible = len(filtered_set)

        if num_possible == 0:
            print(f"No words can be generated with a minimum length of {min_len}")
            return
        elif num_possible < number:
            print(
                f"Only {num_possible} of the {number} requested words "
                "can be generated with a minimum length of {min_len}"
            )
            prospects = filtered_set
        else:
            while len(prospects) < number:
                prospects.add(filtered_set.pop())

        return prospects
