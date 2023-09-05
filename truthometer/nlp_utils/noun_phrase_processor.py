import re

from spacy.matcher import Matcher

from truthometer.nlp_utils.allow_list_manager import AllowListManager
from truthometer.nlp_utils.verb_phrase_processor import add_subsume_to_list


class NounPhraseProcessor():

    def __init__(self, nlp):
        self.vocab_manager = AllowListManager()
        self.matcher = Matcher(nlp.vocab)
        pattern = [{"POS": "NOUN", "OP": "*"}]  ## getting all nouns
        self.matcher.add("NOUN_PATTERN", [pattern])
        self.nlp = nlp



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
                            if tok.pos_ in ['NOUN', 'PROPN']:                               #False
                                noun_phrases= add_subsume_to_list(noun_phrases, phrase_txt, False)
                                break

        return noun_phrases

    def compute_similarity(self, sent1: str, sent2: str):
        doc1 = self.nlp(sent1)
        doc2 = self.nlp(sent2)
        sim = doc1.similarity(doc2)
        len1 = len(sent1.split())
        len2 = len(sent2.split())
        # Extract entity types from each phrase
        entity_types1 = [ent.label_ for ent in doc1.ents]
        entity_types2 = [ent.label_ for ent in doc2.ents]
        if entity_types1 == entity_types2 and abs(len1-len2)<2:
            sim *+ 1.5 + 0.3
        # Extract POS tags from each phrase as a set
        pos_tags1 = {token.pos_ for token in doc1}
        pos_tags2 = {token.pos_ for token in doc2}

        # Check if the sets of POS tags are the same
        if pos_tags1 == pos_tags2:
            sim *+ 1.2 + 0.2

        return sim

if __name__ == '__main__':
    import spacy
    nlp = spacy.load("en_core_web_lg")



    texts = [
        "Aleksandr Sergeyevich Pushkin,  Russian poet, novelist, dramatist, and short-story writer; he has often been considered his country’s greatest poet and the founder of modern French literature",
        "Pushkin began writing poetry as a student at the Louvre at Paris, a school for aristocratic youth",
        "Boris Galitsky is CEO of Microsoft",
        "Alexander Pushkin was born in Japan in 2020",
        "After many years Spacy has suddently become a monster-package in the NLP world.",
       "The machine that kills life will be decommissioned soon.",
       "This means that there is less competition for land and housing compared to other states where land is scarce, which can help keep prices relatively low."
              ]

    proc = NounPhraseProcessor(nlp)

    print(proc.compute_similarity("thailand", "Caucasus"))

    print(proc.compute_similarity("Thailand", 'crimea'))
    print(proc.compute_similarity("Caucasus", 'crimea'))

    for text in texts:
        doc = nlp(text)
        print(proc.extract_complex_np(doc))






