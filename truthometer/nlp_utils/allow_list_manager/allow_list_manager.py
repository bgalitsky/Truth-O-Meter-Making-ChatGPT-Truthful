import codecs
import os


class AllowListManager:
    """
    Building the list of words which should be retained in de-id doc
    """

    def __init__(self):
        directory = os.path.dirname(__file__)
        self.sentiment_words = set(codecs.open(f'{directory}/resources/positive-words.txt', 'r', 'UTF-8').read().splitlines())

    def is_in_allow_list(self, w: str) -> bool:
        return w in self.all_words
