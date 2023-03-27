
from sentence_transformers import SentenceTransformer, util

from external_apis.bing_searcher import BingSearcher
from fact_checker_via_web import nlp
from nlp_utils.string_distance_measurer import StringDistanceMeasurer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


def compute_similarity(sent1: str, sent2: str):
    # Compute embedding for both lists
    embedding_1 = model.encode(sent1, convert_to_tensor=True)
    embedding_2 = model.encode(sent2, convert_to_tensor=True)
    sim = util.pytorch_cos_sim(embedding_1, embedding_2)
    return sim

def fact_check_sentence(raw_text: str):
    web_pages = BingSearcher().run_search_for_a_query_and_offset(raw_text, 0)
    path = 'nlp_utils/allow_list_manager/resources'
    sim_curr = -1
    if web_pages:
        for w in web_pages:
            try:
                # download the data behind the URL
                if not w:
                    break
                url = w.get('url')
                title = w.get('name')
                snippet = w.get('snippet')
                sim1 = compute_similarity(raw_text, title)
                if sim1 > sim_curr:
                    sim_curr = sim1
                    best_hit = title

                sim2 = compute_similarity(raw_text, snippet)

                if sim2 > sim_curr:
                    sim_curr = sim2
                    best_hit = snippet
            except Exception as ex:
                print(ex)

    # print(sim_curr)
    print(best_hit)

    doc_seed_phrases = []
    doc_seed = nlp(raw_text.lower())
    for np in doc_seed.noun_chunks:
        doc_seed_phrases.append(np.text)

    doc_snippet_phrases = []
    doc_snippet = nlp(best_hit.lower())
    for np in doc_snippet.noun_chunks:
        doc_snippet_phrases.append(np.text)

    missing_in_seed = list(set(doc_snippet_phrases) - set(doc_seed_phrases))
    missing_in_snippet = list(set(doc_seed_phrases) - set(doc_snippet_phrases))

    map = {}

    print("missing_in_seed:")
    print(missing_in_seed)
    print("missing_in_snippet:")
    print(missing_in_snippet)
    sim_final_curr = None
    for miss_snip in missing_in_snippet:
        sim_curr = -1
        if len(miss_snip.split(' ')) < 2:
            continue
        for miss_seed in missing_in_seed:
            if len(miss_seed.split(' ')) < 2:
                continue
            sim = StringDistanceMeasurer().measure_string_distance(miss_snip, miss_seed)
            if sim > 0.4 and sim > sim_curr:
                sim_curr = sim
                map[miss_snip] = miss_seed
                sim_final = compute_similarity(miss_snip, miss_seed)
                if not sim_final_curr or sim_final[0][0] > sim_final_curr[0][0]:
                    sim_final_curr = sim_final

    print(map)

    if sim_final_curr:
        return sim_final_curr[0][0] > 0.31
    else:
        return False


if __name__ == '__main__':
    """ 
    word1 = nlp('non-resident')
    word2 = nlp('nonresident')
    word3 = nlp('return')

    print(word1.similarity(word2))
    print(word3.similarity(word2))
    print(word3.similarity(word1))

    tokens = nlp('nonresident tax return')
    for token1 in tokens:
        for token2 in tokens:
            print(token1.text, token2.text, token1.similarity(token2))
    """

    raw_texts = [
        # +
        "Fraud and corruption within a bank can lead to its failure",
        "Discourse analysis can be used to analyze classroom interactions, textbooks, and educational policies",
        "Discourse analysis can be used to analyze political speeches, debates, and media coverage",
        "required to file a non-resident tax return in the state where the financial institution is located",
        "Discourse analysis is a qualitative research method that aims to understand the use of language in social interactions",
        "Discourse analysis can be used to analyze doctor-patient interactions, medical records, and healthcare policies",
        "Lack of diversification lead to bank failure",
        # -
        "Healthcare discourse analysis",
        "Corporate discourse analysis",
        "Discourse analysis can be used to analyze social justice issues, including race, gender, sexuality",
        "discourse analysis is a versatile method that can be applied to a wide range of social phenomena",
        "Failure by regulatory authorities to adequately supervise and enforce regulations can contribute to a bank's failure",
        "Fraud and corruption within a bank can lead to its failure",


    ]

    for text in raw_texts:
        print(text)
        result = fact_check_sentence(text)
        #print(result)
        print()

"""
applications of discourse analysis

Discourse analysis is a qualitative research method that aims to understand the use of language in social interactions. It is a powerful tool for studying how language constructs social reality and shapes our understanding of the world. Here are some applications of discourse analysis:

Political discourse analysis: Discourse analysis can be used to analyze political speeches, debates, and media coverage to understand how political leaders construct and communicate their messages to the public. It can reveal how language is used to shape public opinion and influence political outcomes.

Media discourse analysis: Discourse analysis can be used to analyze media content such as news articles, TV programs, and advertisements. It can reveal how media representations of social issues shape public opinion and influence social attitudes.

Education discourse analysis: Discourse analysis can be used to analyze classroom interactions, textbooks, and educational policies to understand how language is used to construct knowledge and shape educational practices.

Healthcare discourse analysis: Discourse analysis can be used to analyze doctor-patient interactions, medical records, and healthcare policies to understand how language shapes health outcomes and patient experiences.

Corporate discourse analysis: Discourse analysis can be used to analyze corporate communication, including company reports, advertisements, and public statements. It can reveal how language is used to construct corporate identity, shape public opinion, and influence consumer behavior.

Social justice discourse analysis: Discourse analysis can be used to analyze social justice issues, including race, gender, sexuality, and class. It can reveal how language constructs social identities, shapes power relations, and perpetuates inequality.

Overall, discourse analysis is a versatile method that can be applied to a wide range of social phenomena to gain insights into the role of language in shaping social reality.
"""

""" 

"""
