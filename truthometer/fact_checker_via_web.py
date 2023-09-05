import spacy
import argparse

from truthometer.external_apis.google_serp_searcher import GoogleSerpSearcher
from truthometer.nlp_utils.noun_phrase_processor import NounPhraseProcessor
from truthometer.nlp_utils.verb_phrase_processor import VerbPhraseProcessor, clean_phrase
from truthometer.html import VerificationPageBuilder
from truthometer.entity_extractor import get_entities_to_add_to_the_following_sentence, pronouns_short
from truthometer.external_apis.bing_searcher import BingSearcher
from truthometer.nlp_utils.allow_list_manager import AllowListManager
from truthometer.phrase_enumeration_manager import extract_conj_triple_from_text, extract_conj_triple_from_sentence
from truthometer.third_party_models.chat_gpt_answer_format_adapter import adapt_chatgpt_format
from pandas.io.clipboard import clipboard_get

#spacy nlp
nlp = spacy.load("en_core_web_lg")

#truth_o_meter_THRESH = 0.91



def run_web_search(query:str, is_bing = True):
    if is_bing:
        results = BingSearcher().run_search_for_a_query_and_offset(query, 0)
    else:
        results = GoogleSerpSearcher().run_search_for_a_query(query)
    return results


def clean_list(list):
    cleaned = []
    for l in list:
        is_alpha_or_space = all(c.isalpha() or c.isspace()  or c.isnumeric() for c in l)
        if is_alpha_or_space:
            cleaned.append(l)
        else:
            tokens = l.replace(',','').replace('.','').split()
            b_all_token_ok = True
            for t in tokens:
                if not (t.isalpha() or t.isnumeric()):
                    b_all_token_ok = False
            if b_all_token_ok:
                cleaned.append(l)

    return cleaned

def reject_substitution_candidate(miss_snip:str, miss_seed:str, snippet_verb_phrases, seed_verb_phrases)->bool:
    if miss_snip in snippet_verb_phrases and miss_seed not in seed_verb_phrases:
        return False
    if miss_snip not in snippet_verb_phrases and miss_seed in seed_verb_phrases:
        return False

    toks1 = miss_snip.split()
    toks2 = miss_seed.split()
    l1 = len(toks1)
    l2 = len(toks2)
    if l1==1 and l2 == 1:
        return False

    if abs(l1-l2)>1:
        return True

    overlap = list(set(toks1) & set(toks2))
    if len(overlap)<1 or len(overlap[0])<4:
        return True


def additional_filter(missing_in_snippet_filtered_score, map_snip_seed):
    phrase_del = []
    for phrase in missing_in_snippet_filtered_score:
        # if we want to replace by the phrase with the same head noun, abort rejection
        if phrase in map_snip_seed:
            map_phrase = map_snip_seed.get(phrase)
            if map_phrase.split()[-1] == phrase.split()[-1]  and len(phrase.split()[-1])>3 and len(phrase.split())<3:
                phrase_del.append(phrase)
        #else:
        #    phrase_del.append(phrase)

    missing_in_snippet_filtered_score = list(set(missing_in_snippet_filtered_score) - set(phrase_del))
    #remove subsumtion
    for phrase in missing_in_snippet_filtered_score:
        for phrase1 in missing_in_snippet_filtered_score:
            if phrase.find(phrase1)>-1 and not phrase ==phrase1:
                phrase_del.append(phrase1)

    return list(set(missing_in_snippet_filtered_score) - set(phrase_del)), map_snip_seed


class FactCheckerViaWeb():
    def __init__(self):
        self.html_builder = VerificationPageBuilder()
        self.vocabs = AllowListManager()
        self.verb_phrase_proc = VerbPhraseProcessor()
        self.noun_phrase_proc = NounPhraseProcessor(nlp)

    def pronouns_in_sentence(self, sentence: str) ->bool:
        tokens = sentence.lower().split(' ')
        for t in tokens:
            if t in pronouns_short:
                return True
        return False

    def not_acceptable_phrase_as_suspicious(self, phrase: str) -> bool:
        tokens = phrase.split(' ')
        for t in tokens:
            if t in self.vocabs.sentiment_words:
                return True
            if t in pronouns_short:
                return True

        # second: singe word should be a noun
        if len(phrase.split())==1:
            if self.noun_phrase_proc.vocab_manager.is_in_abstract_noun(phrase):
                return True
            doc_single_word = nlp(phrase)[0]
            if doc_single_word.pos_ in ['X', 'NOUN', 'PROPN'] or doc_single_word.ent_type_ in ['NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'PERSON']:
                return False

        return False

    def build_substitution_map(self, missing_in_snippet_filtered, missing_in_seed, snippet_verb_phrases, seed_verb_phrases, web_pages):
        map_phrase_score = {}
        map_snip_seed = {}
        map_seed_hit = {}
        web_text = ""
        for miss_snip in missing_in_snippet_filtered:
            sim_curr = -1

            for miss_seed in missing_in_seed:
                if reject_substitution_candidate(miss_snip, miss_seed, snippet_verb_phrases, seed_verb_phrases):
                    continue
                sim = self.noun_phrase_proc.compute_similarity(miss_snip, miss_seed)
                if sim > sim_curr:
                    sim_curr = sim
                    map_snip_seed[miss_snip] = miss_seed
                    map_phrase_score[miss_snip] = sim
                    count = 0
                    # find which hit has a closest phrase
                    for w in web_pages:
                        try:
                            if not w:
                                break

                            title = w.get('name')
                            snippet = w.get('snippet')
                            web_text += " " + title + ". " + snippet
                            if web_text.find(miss_seed) > -1:
                                map_seed_hit[miss_snip] = count
                                break

                        except Exception as ex:
                            print(ex)
                        count += 1
                        if count > 50:
                            break
                    # if no similarity at all, just set to default 0
                    if miss_snip not in map_seed_hit:
                        map_seed_hit[miss_snip] = 0
        return map_phrase_score, map_snip_seed, map_seed_hit

    # main fact-check function
    def fact_check_sentence(self, current_sentence: str, prev_sentence:str)->str:
        query = current_sentence+''
        # if needs to rely on coreference
        if self.pronouns_in_sentence(current_sentence) and prev_sentence:
            entities = get_entities_to_add_to_the_following_sentence(nlp(prev_sentence))
            prefix_for_it = " ".join(entities)
            query = prefix_for_it + " " + query

        web_pages =  run_web_search(query, True) #:BingSearcher().run_search_for_a_query_and_offset(query, 0)
        web_text = ""
        count = 0
        if web_pages:
            for w in web_pages:
                try:
                    # download the data behind the URL
                    if not w:
                        break

                    title = w.get('name')
                    snippet = w.get('snippet')
                    web_text += " " + title + ". " + snippet

                except Exception as ex:
                    print(ex)
                count += 1
                if count > 50:
                    break

        doc_seed_phrases = []
        doc_seed = nlp(current_sentence)

        seed_verb_phrases = self.verb_phrase_proc.extract_verb_phrases(doc_seed)
        #for np in doc_seed.noun_chunks:
        #    doc_seed_phrases.append(clean_phrase(np.text))
        doc_seed_phrases = self.noun_phrase_proc.extract_complex_np(doc_seed)
        if  len(doc_seed_phrases)<4:
            for vp in seed_verb_phrases:
                doc_seed_phrases.append(clean_phrase(vp))

        doc_snippet_phrases = []
        doc_snippet = nlp(web_text)
        snippet_verb_phrases = self.verb_phrase_proc.extract_verb_phrases(doc_snippet)
        doc_snippet_phrases+= self.noun_phrase_proc.extract_complex_np(doc_snippet) + snippet_verb_phrases
        doc_snippet_phrases = clean_list(doc_snippet_phrases)


        doc_seed_phrases = clean_list(doc_seed_phrases)

        missing_in_seed = list(set(doc_snippet_phrases) - set(doc_seed_phrases))
        missing_in_snippet = list(set(doc_seed_phrases) - set(doc_snippet_phrases))

        conj_phrases_sub_sentence = extract_conj_triple_from_sentence(nlp(current_sentence))
        missing_in_snippet_altered = []
        if conj_phrases_sub_sentence:
            for m in missing_in_snippet:
                if conj_phrases_sub_sentence.find(m) > -1:
                    missing_in_snippet_altered.append(m)

        if len(missing_in_snippet_altered) < 1:
            missing_in_snippet_altered = missing_in_snippet

        map_snip_seed = {}
        map_seed_hit = {}

        # print("missing_in_seed:")
        # print(missing_in_seed)
        # print("missing_in_snippet:")
        # print(missing_in_snippet)
        web_text_lower = web_text.lower()
        missing_in_snippet_filtered = []
        for miss_snip in missing_in_snippet_altered:
            if self.not_acceptable_phrase_as_suspicious(miss_snip):
                continue
            if web_text_lower.find(miss_snip)>-1:
                continue
            missing_in_snippet_filtered.append(miss_snip)

        # find phrase in snippets closest to the wrong word in raw_text
        map_phrase_score, map_snip_seed, map_seed_hit = self.build_substitution_map(missing_in_snippet_filtered, missing_in_seed, snippet_verb_phrases,
                               seed_verb_phrases, web_pages)
        # first filter the map if candidate wrong phrase covers or is covered by the closest phrase in web_text
        prohib_miss_snip = []
        """ 
        for miss_snip in missing_in_snippet_filtered:
            closest_in_web_text = map_snip_seed[miss_snip]
            # if have the same head noun: prohibitive
            head_noun1 = miss_snip.split(' ')[-1]
            head_noun2 = closest_in_web_text.split(' ')[-1]
            if head_noun1 == head_noun2:
                pos1 = nlp(head_noun1)[0].pos
                pos2 = nlp(head_noun2)[0].pos
                if pos1 == pos2:
                    prohib_miss_snip.append(miss_snip)
        """


        # filter of 'not in snippet' phrases
        missing_in_snippet_filtered_score = []
        for m in missing_in_snippet_filtered:
            if m in prohib_miss_snip:
                continue
            #if m in map_phrase_score:
            #    if map_phrase_score[m] > truth_o_meter_THRESH:
            #        continue
            missing_in_snippet_filtered_score.append(m)

        missing_in_snippet_filtered_score_a, map_snip_seed_a = additional_filter(missing_in_snippet_filtered_score, map_snip_seed)

        page, sent_with_error = self.html_builder.insert_bookmarks_in_sentence(current_sentence, missing_in_snippet_filtered_score_a, web_pages, map_seed_hit, map_snip_seed_a)
        return page, sent_with_error

    # fact-check text
    def perform_and_report_fact_check_for_text(self, text:str)->str:
        raw_texts=[]
        text = adapt_chatgpt_format(text)
        doc = nlp(text)
        for sent in doc.sents:
            raw_texts.append(sent.text)

        content = ""
        for i in range(len(raw_texts)):
            if i>0:
                section, s = self.fact_check_sentence(raw_texts[i], raw_texts[i-1])
            else:
                section, s = self.fact_check_sentence(raw_texts[i], None)
            print(section)
            print()
            content += '\n' + section

        report_path = self.html_builder.write_html_page(text, content)
        return report_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_txt", type=str,
                        help='full name of TXT file to fact-check')
    text = ""
    try:
        args = parser.parse_args()
        text = args.input_text
    except Exception as ex:
        print("getting content from clipboard")

    if len(text)<3:
        text = clipboard_get()
    fact_checker = FactCheckerViaWeb()
    page_path = fact_checker.perform_and_report_fact_check_for_text(text)


