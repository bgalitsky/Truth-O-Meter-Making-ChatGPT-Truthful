#https://github.com/clir/clearnlp-guidelines/blob/master/md/specifications/dependency_labels.md
#https://machinelearningknowledge.ai/tutorial-on-spacy-part-of-speech-pos-tagging/


sent = "If a bank engages in fraudulent or unethical practices, it can suffer reputational damage, legal liabilities, " \
         "and loss of customers."
"""
Economic downturns: When the economy experiences a recession or downturn, people and businesses may struggle to repay loans, which can result in increased loan defaults and ultimately cause banks to suffer losses.

Asset quality deterioration: If a bank's loans and investments perform poorly, the bank's assets can decrease in value, which can lead to a decline in the bank's financial health.

Liquidity issues: Banks require a steady flow of cash to meet the demands of customers, such as withdrawals, loans, and investments. If a bank lacks sufficient liquidity, it may struggle to meet these demands, which can result in a loss of confidence and potentially cause the bank to fail.

Regulatory violations: Banks are subject to numerous regulations, and violations of these regulations can result in fines, penalties, and even closure.

"""

def extract_conj_triple_from_text(doc):
    for sent_doc in doc.sents:
        print(extract_conj_triple_from_sentence(sent_doc))


# finds a part of complex sentence with enumeration of phrases which are candidates for fact-checking
def extract_conj_triple_from_sentence(doc)->str:
    token_extraction = []
    # Print out the tokens
    token_prev = None
    b_possible_triplet_started = False
    b_in_triplet = False
    #for token in doc:
    #    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #          token.shape_, token.is_alpha, token.is_stop)
    if len(doc.text)<50:
        return ""

    for token in doc:
        if token_prev and token_prev.pos_ == 'VERB':
            if b_in_triplet:
                return ' '.join(token_extraction)

            b_possible_triplet_started = True
            token_extraction = []
            token_extraction.append(token.text)
        elif b_possible_triplet_started:
            token_extraction.append(token.text)

        if b_possible_triplet_started and token_prev and token_prev.text == ',' and token.lemma_ == 'and':
            b_in_triplet = True

        if b_in_triplet and token.pos_ not in ['ADJ', 'CONJ', 'NOUN', 'PROPN', 'PUNCT', 'DET', 'CCONJ', 'ADP']:
            return ' '.join(token_extraction)

        token_prev = token

    if b_in_triplet:
        return ' '.join(token_extraction)
    else:
        return None

if __name__ == '__main__':
    from fact_checker_via_web import nlp
    sent = "Whether a CD or brokerage account is better for a nonresident depends on several factors, including the individual's investment goals, risk tolerance, time horizon, tax situation, and other financial circumstances."
    print(extract_conj_triple_from_sentence(nlp(sent)))


