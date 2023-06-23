from typing import List
import spacy

#nlp = spacy.load("en_core_web_lg")

entity_types_of_interest = ['NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'PERSON']

pronouns_short = ['I', 'he', 'him', 'his', 'her', 'theirs', 'someone', 'it', 'they',
                  'hers', 'whose', 'these', 'those', 'that', 'which', 'one', 'ones',
                  "us", "you", "them", "who", "what", "which", "me", "ourselves",
                  "ourself", "yourselves", "herself", "itself", "themselves",
                  "themself", "myself", "ours", "yours", "its", "theirs",
                  "oneself", "your", "whom", "mine", "himself", "its", "their", "one's"
                  ]
""" 
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
example = "Located just outside Anamur, this well-preserved castle was built by the Romans in the 3rd century and later expanded by the Byzantines and the Seljuks."

ner_results = nlp(example)
print(ner_results)

import spacy

doc = nlp("get_entities_to_add_to_the_following_sentence")
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])
"""
sent = "Local cuisine: Anamur is known for its delicious local cuisine, which includes dishes such as stuffed mussels, grilled octopus, and goat meat."


def get_entities_to_add_to_the_following_sentence(doc) -> List[str]:
    words = []
    for word in doc.ents:
        if word.label_ in entity_types_of_interest:
            words.append(word.text)
        # print(word.label_)
    return words


def match_entities_in_a_pair_of_phrase_docs(phrase_doc1, phrase_doc2):
    ents1 = []
    ents2 = []
    ents_phrs1 = {}
    ents_phrs2 = {}
    for word in phrase_doc1.ents:
        if word.label_ in entity_types_of_interest:
            ents1.append(word.text)
            ents_phrs1[word.label_] = word.text

    for word in phrase_doc2.ents:
        if word.label_ in entity_types_of_interest:
            ents2.append(word.text)
            ents_phrs2[word.label_] = word.text
    #find unmatched entity type
    ents2_diff = ents2.copy()
    ents1_diff = ents1.copy()

    ents2_diff.difference(ents1)
    ents1_diff.difference(ents2)

    missing_words1 = []
    missing_words2 = []
    for e in ents2_diff:
        missing_words1.append(ents_phrs2.get(e))
    for e in ents1_diff:
        missing_words2.append(ents_phrs1.get(e))

    return missing_words1, missing_words2

""" 
if __name__ == '__main__':
    sent1 = "Rajesh Trivedi is a CEO of Microsoft"
    sent2 = "Rajesh Trivedi - Founder & CEO - Astra"
    phrase_doc1 = nlp(sent1)
    phrase_doc2 = nlp(sent2)
    match_map = match_entities_in_a_pair_of_phrase_docs(phrase_doc1, phrase_doc2)
    print(match_map)

# print(get_entities_to_add_to_the_following_sentence(nlp(sent)))
"""

"""
SpaCy recognizes the following built-in entity types:
PERSON - People, including fictional.

NORP - Nationalities or religious or political groups.

FAC - Buildings, airports, highways, bridges, etc.

ORG - Companies, agencies, institutions, etc.

GPE - Countries, cities, states.

LOC - Non-GPE locations, mountain ranges, bodies of water.

PRODUCT - Objects, vehicles, foods, etc. (Not services.)

EVENT - Named hurricanes, battles, wars, sports events, etc.

WORK_OF_ART - Titles of books, songs, etc.

LAW - Named documents made into laws.

LANGUAGE - Any named language.

DATE - Absolute or relative dates or periods.

TIME - Times smaller than a day.

PERCENT - Percentage, including "%".

MONEY - Monetary values, including unit.

QUANTITY - Measurements, as of weight or distance.

ORDINAL - "first", "second", etc.

CARDINAL - Numerals that do not fall under another type.
"""
