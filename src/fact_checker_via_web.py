import spacy
import argparse

from external_apis.bing_searcher import BingSearcher
from src.html.verification_page_builder import VerificationPageBuilder
from phrase_enumeration_manager import extract_conj_triple_from_text
from third_party_models.chat_gpt_answer_format_adapter import adapt_chatgpt_format
from pandas.io.clipboard import clipboard_get

#spacy nlp
nlp = spacy.load("en_core_web_lg")



truth_o_meter_THRESH = 0.91

def compute_similarity(sent1: str, sent2: str):
    sim = nlp(sent1).similarity(nlp(sent2))
    return sim

def clean_list(list):
    cleaned = []
    for l in list:
        is_alpha_or_space = all(c.isalpha() or c.isspace() for c in l)
        if is_alpha_or_space:
            cleaned.append(l)
    return cleaned


def clean_phrase(phrase):
    phrase_clean = phrase.replace('\n','').replace('  ',' ').strip().rstrip()
    if phrase_clean.startswith('a '):
        phrase_clean = phrase_clean[2:1000]
    if phrase_clean.startswith('the '):
        phrase_clean = phrase_clean[4:1000]
    return phrase_clean.lower()

class FactCheckerViaWeb():
    def __init__(self):
        self.html_builder = VerificationPageBuilder()

    def fact_check_sentence(self, raw_text: str):
        web_pages = BingSearcher().run_search_for_a_query_and_offset(raw_text, 0)
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
        doc_seed = nlp(raw_text.lower())
        for np in doc_seed.noun_chunks:
            doc_seed_phrases.append(clean_phrase(np.text))

        doc_snippet_phrases = []
        doc_snippet = nlp(web_text.lower())
        for np in doc_snippet.noun_chunks:
            doc_snippet_phrases.append(clean_phrase(np.text))

        doc_snippet_phrases = clean_list(doc_snippet_phrases)
        doc_seed_phrases = clean_list(doc_seed_phrases)

        missing_in_seed = list(set(doc_snippet_phrases) - set(doc_seed_phrases))
        missing_in_snippet = list(set(doc_seed_phrases) - set(doc_snippet_phrases))

        conj_phrases = extract_conj_triple_from_text(nlp(raw_text))
        missing_in_snippet_filtered = []
        if conj_phrases:
            for m in missing_in_snippet:
                if conj_phrases.find(m) > -1:
                    missing_in_snippet_filtered.append(m)

        if len(missing_in_snippet_filtered) < 1:
            missing_in_snippet_filtered = missing_in_snippet

        map_snip_seed = {}
        map_seed_hit = {}

        # print("missing_in_seed:")
        # print(missing_in_seed)
        # print("missing_in_snippet:")
        # print(missing_in_snippet)

        # find phrase in snippets closest to the wrong word in raw_text
        map_phrase_score = {}
        for miss_snip in missing_in_snippet:
            sim_curr = -1

            for miss_seed in missing_in_seed:
                if len(miss_seed.split(' ')) < 2:
                    continue
                sim = nlp(miss_snip).similarity(nlp(miss_seed))
                if sim> sim_curr:
                    sim_curr = sim
                    map_snip_seed[miss_snip] = miss_seed
                    map_phrase_score[miss_snip] = sim
                    count = 0
                    for w in web_pages:
                        try:
                            if not w:
                                break

                            title = w.get('name')
                            snippet = w.get('snippet')
                            web_text += " " + title + ". " + snippet
                            if web_text.find(miss_seed)>-1:
                                map_seed_hit[miss_snip] = count
                                break

                        except Exception as ex:
                            print(ex)
                        count += 1
                        if count > 50:
                            break
        missing_in_snippet_filtered_score = []
        for m in missing_in_snippet_filtered:
            if m in map_phrase_score:
                if map_phrase_score[m] > truth_o_meter_THRESH:
                    continue
            missing_in_snippet_filtered_score.append(m)

        page = self.html_builder.insert_bookmarks_in_sentence(raw_text, missing_in_snippet_filtered, web_pages, map_seed_hit, map_snip_seed)
        return page

    # fact-check text
    def perform_and_report_fact_check_for_text(self, text:str)->str:
        raw_texts=[]
        text = adapt_chatgpt_format(text)
        doc = nlp(text)
        for sent in doc.sents:
            raw_texts.append(sent.text)

        content = ""
        for text in raw_texts:
            print(text)
            section = self.fact_check_sentence(text)
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


