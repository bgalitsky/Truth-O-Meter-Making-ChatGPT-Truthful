import re


def clean_phrase(phrase):
    phrase_clean = phrase.replace('\n', '').replace('  ', ' ').strip().rstrip()
    if phrase_clean.startswith('a '):
        phrase_clean = phrase_clean[2:1000]
    if phrase_clean.startswith('an '):
        phrase_clean = phrase_clean[3:1000]
    if phrase_clean.startswith('the '):
        phrase_clean = phrase_clean[4:1000]
    return phrase_clean.lower()

def add_subsume_to_list(result_list, element, sub_not_super = True):
    results = []
    v_del = []
    if sub_not_super:
        for v in result_list:
            if v.find(element) > -1:
                v_del.append(v)
    """             
    else:
        for v in result_list:
            if element.find(v) > -1:
                v_del.append(v)
    """
    results = list(set(result_list) - set(v_del))
    if element not in results:
        results.append(clean_phrase(element))
    return results

class VerbPhraseProcessor():

    def get_verb_phrase_for_token(self, nlpdoc, mytoken):
        mylist = []

        patt = re.compile(mytoken)

        for token in nlpdoc:
            if token.pos_ == 'VERB' or token.pos_ == 'AUX':
                # print('    ')
                print(token.text)
                # print('    ')
                # get children on verb/aux
                nodechild = token.children
                getchild1 = []
                getchild2 = []
                # iterate over the children
                for child in nodechild:
                    getchild1.append(child)
                    # get children of children
                    listchild = list(child.children)
                    for grandchild in listchild:
                        getchild2.append(grandchild)
                # print('children are ' + str(getchild1))
                # print('grandchildren are ' + str(getchild2))
                # check if Spacy is a children or a children of a children
                test1 = [patt.search(tok.lemma_) for tok in getchild1]
                test2 = [patt.search(tok.lemma_) for tok in getchild2]
                # if YES, then parse the VP
                if any(test1) or any(test2):

                    fulltok = token.text
                    myiter = token
                    # the VP can actually start a bit before the VERB, so we look for the leftmost AUX/VERBS
                    candidates = [lefty for lefty in token.lefts]
                    candidates = [lefty for lefty in candidates if lefty.pos_ in ['AUX', 'VERB']]
                    # if we find one, then we start concatenating the tokens from there
                    if candidates:
                        fulltok = candidates[0].text
                        myiter = candidates[0]

                    while myiter.nbor().pos_ in ['VERB', 'PART', 'ADV', 'ADJ', 'ADP', 'NUM', 'DET', 'NOUN', 'PROPN', 'AUX']:
                        fulltok = fulltok + ' ' + myiter.nbor().text
                        myiter = myiter.nbor()
                    mylist.append(fulltok)
        return mylist




    def extract_verb_phrases(self, doc):
        verb_phrases = []
        verb_phrases_updated = []
        for token in doc:
            if token.pos_ == 'VERB' or token.pos_ == 'AUX':
                # Get the verb phrase by navigating through the dependency tree
                verb_phrase = ""
                b_accum = False
                for t in token.subtree:
                    if t.text == token.text:
                        b_accum = True
                    if b_accum and t.pos_ not in ['VERB', 'PART', 'ADV', 'ADJ', 'ADP', 'NUM', 'DET', 'NOUN', 'PROPN', 'AUX']:
                        break
                    if b_accum:
                        verb_phrase += t.text + ' '
                verb_phrase = verb_phrase.strip().rstrip()

                # no single verb accepted
                if len(verb_phrase.split())<2:
                    continue
                # should be the shortest phrase
                verb_phrases_updated = add_subsume_to_list(verb_phrases_updated, verb_phrase)
                """ 
                v_del = []
                for v in verb_phrases:
                    if v.find(verb_phrase) > -1:
                        v_del.append(v)
                verb_phrases.append(verb_phrase)
                verb_phrases_updated = list(set(verb_phrases) - set(v_del))
                """

        return verb_phrases_updated

    def extract_verb_phrases_via_nsubjpass(doc):
        verb_phrases = []
        for sent in doc.sents:
            print(sent.root)
            for child in sent.root.children:
                if child.dep_ == 'nsubjpass':
                    phrase_str = " ".join(list(child.subtree))
                    verb_phrases.appemnd(phrase_str)

        return verb_phrases

    pattern = [{'POS': 'VERB'}]
    """ 
    def extract_verb_phrases_via_textacy(doc):
        verb_phrases = textacy.extract.matches(txt, patterns=pattern)
        return list(verb_phrases)
    """

if __name__ == '__main__':
    import spacy
    nlp = spacy.load("en_core_web_lg")

    texts = ["Boris Galitsky is CEO of Microsoft",
        "Alexander Pushkin was born in Japan in 2020",
        "After many years Spacy has suddently become a monster-package in the NLP world.",
       "The machine that kills life will be decommissioned soon.",
       "This means that there is less competition for land and housing compared to other states where land is scarce, which can help keep prices relatively low."]

    proc = VerbPhraseProcessor()

    for text in texts:
    # Process the text with Spacy
        doc = nlp(text)
        print(proc.extract_verb_phrases(doc))

    print(proc.get_verb_phrase_for_token(doc, r'Spacy'))




