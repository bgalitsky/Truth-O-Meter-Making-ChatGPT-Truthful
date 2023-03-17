import difflib
from typing import List

from nltk.stem.snowball import SnowballStemmer
from nltk.metrics import edit_distance

def custom_tokenize(line: str) -> List[str]:
    # punctuation = r"""'",.!?[](){}#*&;"""
    # line = line.translate(str.maketrans('', '', punctuation))

    string_no_punctuation = line.replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ') \
        .replace('\"', '').replace('\'', ' ').replace('[', ' ').replace(']', ' ').replace('(', ' '). \
        replace(')', ' ').replace('{', ' ').replace('}', ' ').replace('#', ' ').replace('*', ' ') \
        .replace('&', ' ').replace(';', ' ')
    return string_no_punctuation.split()

class StringDistanceMeasurer:
    """
    Code originates from:
    https://github.com/bgalitsky/relevance-based-on-parse-trees/blob/d271e54dc6307d3ee5970431bd800a89a14e767d/src/main/java/opennlp/tools/similarity/apps/utils/StringDistanceMeasurer.java
    """

    def __init__(self):
        self.MIN_STRING_LENGTH_FOR_WORD = 3
        self.MIN_STRING_LENGTH_FOR_DISTORTED_WORD = 6
        self.ACCEPTABLE_DEVIATION_IN_CHAR = 2
        self.stemmer = SnowballStemmer("english")
        self.MIN_SCORE_FOR_LING = 100

    # gets string array and process numbers,
    def filter_word_array_no_stem(self, words):
        str_list = []
        for w in words:
            b_integer = True
            if w.isnumeric():
                b_integer = False

            if len(w) < self.MIN_STRING_LENGTH_FOR_WORD and not b_integer:
                continue
            w = w.lower()
            str_list.append(w)

        return str_list

    @staticmethod
    def list_sim_(s1, s2):
        sm = difflib.SequenceMatcher(None, s1, s2)
        return sm.ratio()

    # main entry point. Gets two strings and applies string match
    # and also linguistic match if score > a threshold

    def measure_string_distance(self, str1: str, str2: str) -> float:

        if str1 == "" or str2 == "" or len(str1) < 3 or len(str2) < 3:
            return 0.0
        if str1 == str2:
            return 1.0

        tokens1 = custom_tokenize(str(str1))
        tokens2 = custom_tokenize(str(str2))
        tokens1 = self.filter_word_array_no_stem(tokens1)
        tokens2 = self.filter_word_array_no_stem(tokens2)

        s1_unique_tokens = set(tokens1)
        s2_unique_tokens = set(tokens2)

        l1 = len(s1_unique_tokens)
        l2 = len(s2_unique_tokens)
        if l1 < 2:
            l1 = len(str1.split())
        if l2 < 2:
            l2 = len(str2.split())
        stok12 = s1_unique_tokens & s2_unique_tokens
        str_list_overlap = list( stok12 )
        l_overlap = len(str_list_overlap)

        # now we try to find similar words which are long
        count_similar_lev = 0
        tokens1_rm = [x for x in tokens1 if x not in str_list_overlap]
        tokens2_rm = [x for x in tokens2 if x not in str_list_overlap]

        for w1 in tokens1_rm:
            for w2 in tokens2_rm:
                if len(w1) > self.MIN_STRING_LENGTH_FOR_DISTORTED_WORD and len(
                        w2) > self.MIN_STRING_LENGTH_FOR_DISTORTED_WORD:
                    lev_dist = edit_distance(w1, w2)
                    if lev_dist <= self.ACCEPTABLE_DEVIATION_IN_CHAR:
                        count_similar_lev += 1

        l_overlap += count_similar_lev
        score = pow(float(l_overlap * l_overlap) / float(l1 * l2), 0.4)
        return score
