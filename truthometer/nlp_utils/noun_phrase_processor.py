import re

from spacy.matcher import Matcher

from truthometer.nlp_utils.allow_list_manager import AllowListManager
from truthometer.nlp_utils.verb_phrase_processor import add_subsume_to_list


prohibited_np = ['', 'a', 'the']

quantifiers_determiners = ['some', 'various', 'diverse', 'more', 'less',
'these', 'those',
'rather', 'several', 'numerous', 'few', 'many', 'multiple', 'abundant', 'miscellaneous', 'assorted', 'plentiful',
'limited', 'frequent', 'myriad', 'sparse', 'different', 'few', 'countless',
'of', 'for', 'in', 'by', 'with', 'about', 'against', 'among', 'at', 'between', 'during', 'through', 'over', 'under',
                           'into', 'near', 'since', 'until', 'without', 'within', 'certain', 'potential']




def split_long_noun_phrase(phrase_str: str):
    if phrase_str.find(',')>-1:
        phrase_str = phrase_str.replace(',and ', ', ').replace(' and ', ', ').replace(' or ', ', ')
        part = phrase_str.split(', ')
        accum_list = []
        for o in part:
            cleaned = o #.strip().rstrip()
            if len(cleaned)>1:
                tokens = cleaned.split()
                if len(tokens) < 4:
                    accum_list.append(cleaned)
                else:
                    accum_list = accum_list + _split_long_phrase(tokens)
        return [phrase_str] #accum_list

    tokens = phrase_str.split()
    if len(tokens) < 4:
        return [phrase_str]
    for t in tokens:
        if t == 'or' or t == 'and':
            parts = phrase_str.split(' '+t+' ')
            accum_list = []
            for o in parts:
                cleaned = o.strip().rstrip()
                if len(cleaned) > 1:
                    tokens = cleaned.split()
                    if len(tokens) < 4:
                        accum_list.append(cleaned)
                    else:
                        accum_list = accum_list + _split_long_phrase(tokens)
            return accum_list

    return _split_long_phrase(tokens)

def _split_long_phrase(tokens):
    accum_str = ''
    accum_list = []
    count = 0
    for t in reversed(tokens):
        if count > 0:
            accum_str = t + " " + accum_str
            accum_list.append(accum_str)
            if len(tokens)-count-2 >3:
                start = len(tokens)-count-2 - 3
            else:
                start = 0
            prefix = ' '.join(tokens[start:len(tokens)-count-2])
            if len(prefix)>2:
                accum_list.append(prefix)
            if count>2:
                break
        else:
            accum_str = t
        count+=1

    return accum_list

def remove_subsume(map_snip_seed):
    keys = map_snip_seed.keys()
    keys_to_be_deleted = []
    for k in keys:
        for k1 in keys:
            #k is super-string
            if k.find(k1) > -1 and k1.find(k) <0:
                if k not in keys_to_be_deleted:
                    keys_to_be_deleted.append(k)
    new_map_snip_seed = dict(map_snip_seed)
    for d in keys_to_be_deleted:
        del new_map_snip_seed[d]
    return new_map_snip_seed

def remove_subsume_list(keys):
    keys_to_be_deleted = []
    for k in keys:
        for k1 in keys:
            #k is super-string
            if k.find(k1) > -1 and k1.find(k) <0:
                if k not in keys_to_be_deleted:
                    keys_to_be_deleted.append(k)
    new_keys = list(keys)
    for d in keys_to_be_deleted:
        new_keys.remove(d)
    return new_keys

def add_subsume_to_extended_list(noun_phrases, phrase_txt, sub_not_super = True):
    if phrase_txt in prohibited_np:
        return noun_phrases

    expansion_lst = split_long_noun_phrase(phrase_txt)
    if '' in expansion_lst:
        expansion_lst.remove('')
    for element in   expansion_lst:
        noun_phrases = add_subsume_to_list(noun_phrases, element, sub_not_super)
    return noun_phrases

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
                    if not self.vocab_manager.is_in_words_english(phrase_txt.lower()):
                        noun_phrases= add_subsume_to_extended_list(noun_phrases, phrase_txt, False)
                else:
                    head_noun = tokens[-1]
                    for tok in doc:
                        #check that phrase ends with noun
                        if tok.text == head_noun:
                            if tok.pos_ in ['NOUN', 'PROPN']:                               #False
                                noun_phrases= add_subsume_to_extended_list(noun_phrases, phrase_txt, False)
                                break

        # removing 'some' in the beginning of phrase
        cleaned_prefix_noun_phrases = []
        for n_space in noun_phrases:
            n = n_space.strip().replace(',,',',')
            if n in prohibited_np or n in quantifiers_determiners or n =='':
                continue
            bFound = False
            for w in quantifiers_determiners:
                if n.startswith(w+' '):
                    cleaned_prefix_noun_phrases.append(n[len(w):100000].strip())
                    bFound = True
                    break
            # typical case
            if not bFound:
                cleaned_prefix_noun_phrases.append(n)

        noun_phrases_dupe = list(set(cleaned_prefix_noun_phrases))

        return noun_phrases_dupe

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

    map = {}

    map["Increased risk of genetic mutations"] = 1
    map["Increased risk of genetic"] = 2
    map["Increased risk"] = 3
    map["associated with advanced parental age"] = 30
    map["associated with advanced parental"] = 31
    map["with advanced"] = 32

    new_map = remove_subsume(map)
    print(new_map)
    keys = map.keys()
    new_keys = remove_subsume_list(keys)
    print(new_keys)

    import spacy
    nlp = spacy.load("en_core_web_lg")

    #for p in [#'los banos', 'almonds',
    #          'some of the key agricultural products grown near los banos', 'key agricultural products', 'key agricultural products grown near los banos']:
    #    print(split_long_noun_phrase(p))

    texts = [
        "Increased risk of genetic mutations, particularly those associated with advanced parental age, can lead to a higher likelihood of various genetic disorders and conditions",
        "Some of the key agricultural products grown near los banos include almonds",
        "Aleksandr Sergeyevich Pushkin,  Russian poet, novelist, dramatist, and short-story writer; he has often been considered his country’s greatest poet and the founder of modern French literature",
        "Pushkin began writing poetry as a student at the Louvre at Paris, a school for aristocratic youth",
        "Boris Galitsky is CEO of Microsoft",
        "Alexander Pushkin was born in Japan in 2020",
        "This means that there is less competition for land and housing compared to other states where land is scarce, which can help keep prices relatively low.",
        "The machine that kills life will be decommissioned soon.",
        "After many years Spacy has suddently become a monster-package in the NLP world."
            ]


    proc = NounPhraseProcessor(nlp)
    print(proc.compute_similarity("thailand", "Caucasus"))

    print(proc.compute_similarity("Thailand", 'crimea'))
    print(proc.compute_similarity("Caucasus", 'crimea'))

    for text in texts:
        doc = nlp(text)
        print(proc.extract_complex_np(doc))


    """ 

    """



