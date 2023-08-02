import codecs
import os


class AllowListManager:
    """
    Building the list of words which should be or not be head nouns for fact-checking phrases
    """

    def __init__(self):
        directory = os.path.dirname(__file__)
        self.sentiment_words = set(codecs.open(f'{directory}/resources/positive-words.txt', 'r', 'UTF-8').read().splitlines())
        self.words_last_names = set(
            codecs.open(f'{directory}/resources/last_names.txt', 'r', 'UTF-8').read().splitlines())
        self.words_english = set(
            codecs.open(f'{directory}/resources/english_words10000.txt', 'r', 'UTF-8').read().splitlines())
        self.words_abstract_nouns = set(
            codecs.open(f'{directory}/resources/abstract_noun.txt', 'r', 'UTF-8').read().splitlines())
        lowercase_list = [string.lower() for string in  self.words_abstract_nouns]
        self.words_abstract_nouns = lowercase_list


    def is_in_allow_list(self, w: str) -> bool:
        return w in self.all_words

    def is_in_sentiment_list(self, w: str) -> bool:
        return w in self.sentiment_words

    def is_in_last_names(self, w: str) -> bool:
        return w in self.words_last_names

    def is_in_words_english(self, w: str) -> bool:
        return w in self.words_english

    def is_in_abstract_noun(self, w: str) -> bool:
        return w in self.words_abstract_nouns

if __name__ == '__main__':
    man =  AllowListManager()
    print(man.is_in_abstract_noun('concern'))
    print(man.is_in_abstract_noun('cat'))