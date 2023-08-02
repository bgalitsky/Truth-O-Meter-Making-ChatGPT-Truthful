import re

from spacy.matcher import Matcher

from nlp_utils.allow_list_manager import AllowListManager
from nlp_utils.verb_phrase_processor import add_subsume_to_list




class NounPhraseProcessor():

    def __init__(self, nlp):
        self.vocab_manager = AllowListManager()
        self.matcher = Matcher(nlp.vocab)
        pattern = [{"POS": "NOUN", "OP": "*"}]  ## getting all nouns
        self.matcher.add("NOUN_PATTERN", [pattern])



    def extract_noun_phrases(self, doc):
        phrases = []
        for np in doc.noun_chunks:
            phrases.append(self.clean_phrase(np.text))

        return phrases

    def extract_noun_phrases_via_pattern(self, doc):
        return self.matcher(doc, as_spans=True)

    def extract_complex_np(self, doc):
        noun_phrases = []
        for nc in doc.noun_chunks:
            for np in [nc, doc[nc.root.left_edge.i:nc.root.right_edge.i + 1]]:
                phrase_txt = np.text
                tokens = phrase_txt.split()
                if len(tokens)<2:
                    if not self.vocab_manager.is_in_words_english(phrase_txt):
                        noun_phrases= add_subsume_to_list(noun_phrases, phrase_txt, False)
                else:
                    head_noun = tokens[-1]
                    for tok in doc:
                        if tok.text == head_noun:
                            if tok.pos_ in ['NOUN', 'PROPN']:
                                noun_phrases= add_subsume_to_list(noun_phrases, phrase_txt, False)
                                break

        return noun_phrases

if __name__ == '__main__':
    import spacy
    nlp = spacy.load("en_core_web_lg")

    texts = ["Boris Galitsky is CEO of Microsoft"
        "Alexander Pushkin was born in Japan",
        "After many years Spacy has suddently become a monster-package in the NLP world.",
       "The machine that kills life will be decommissioned soon.",
       "This means that there is less competition for land and housing compared to other states where land is scarce, which can help keep prices relatively low."
              ]

    proc = NounPhraseProcessor()

    for text in texts:
        doc = nlp(text)
        print(proc.extract_complex_np(doc))






