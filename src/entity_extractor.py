from typing import List
import spacy
#nlp = spacy.load("en_core_web_lg")

pronouns_short = ['I', 'he', 'him' 'his', 'her', 'theirs', 'someone', 'it',
            'hers','whose', 'these', 'those','that']
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



def get_entities_to_add_to_the_following_sentence(doc)->List[str]:
    words = []
    for word in doc.ents:
        if word.label_ in ['NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'PERSON']:
            words.append(word.text)
        #print(word.label_)
    return words

#print(get_entities_to_add_to_the_following_sentence(nlp(sent)))

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