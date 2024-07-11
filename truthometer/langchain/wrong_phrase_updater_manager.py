import os

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, ConfigurableField
import langchain
langchain.verbose = False
langchain.debug = False
langchain.llm_cache = False

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

class WrongPhraseUpdaterManager():
    def __init__(self):
        from truthometer.key_manager import provider_key
        langchain_key = provider_key['langchain']
        os.environ["LANGCHAIN_API_KEY"] = langchain_key
        os.environ["LANGCHAIN_TRACING_V2"] = "true"

        chat_openai = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key = os.environ["LANGCHAIN_API_KEY"])
        openai = OpenAI(model="gpt-3.5-turbo-instruct",  openai_api_key = os.environ["LANGCHAIN_API_KEY"])
        model = (
            chat_openai

            .configurable_alternatives(
                ConfigurableField(id="model"),
                default_key="chat_openai",
                openai=openai
            )
        )

        prompt = ChatPromptTemplate.from_template(
            "Substitute # with correct values in text: '{sentence}' "
        )

        prompt_higher_similarity_with_original = ChatPromptTemplate.from_template(
            "Substitute # with correct values in text: '{sentence}' making in similar to the original text '{sentence_orig}' and taking into "+
            "account that incorrect values in the original text should be corrected. " +
            "Put <i> and </i> tags around the corrected values"
        )

        prompt_phrase_similarity = ChatPromptTemplate.from_template(
            "Compare '{phrase1}' and '{phrase2}' with respect to semantic similarity. "+
            "Return 'yes' if similar and mean almost the same thing, and 'no' otherwise"
        )

        self.chain = (
            {"sentence": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        self.chain2 = (
            {"sentence": RunnablePassthrough(), "sentence_orig": RunnablePassthrough()}
            | prompt_higher_similarity_with_original
            | model
            | StrOutputParser()
        )

        self.update_chain = (
            {"phrase1": RunnablePassthrough(), "phrase2": RunnablePassthrough()}
            | prompt_phrase_similarity
            | model
            | StrOutputParser()
        )

    def perform_substitution(self, sentence):
        if sentence.find('#')<0:
            return sentence
        updated_sentence = self.chain.invoke(sentence)
        return updated_sentence

    #  now with original sentence, to stay as close to it as possible
    def perform_substitution(self, sentence, sentence_orig):
        if sentence.find('#')<0:
            return sentence
        updated_sentence = self.chain2.invoke("sentence:" + sentence + " sentence_orig:" + sentence_orig)

        return find_between(updated_sentence, "sentence:", " sentence_orig:")

    def update_based_on_llm_similarity(self, suspicious_phrases, map_seed_hit, map_snip_seed):
        to_remove = []
        keys = map_snip_seed.keys()
        for k in keys:
            value = map_snip_seed[k]
            if not value is None:
                is_similar_str = self.update_chain.invoke("phrase1:" + k + " phrase2:" + value)
                if is_similar_str.lower() == 'yes' or is_similar_str.lower() .find('the same')>-1 or is_similar_str.lower() .find("'yes'")>-1:
                    to_remove.append(k)

        new_map_snip_seed = dict(map_snip_seed)
        for d in to_remove:
            del new_map_snip_seed[d]

        new_map_seed_hit = dict(map_seed_hit)
        for d in to_remove:
            del new_map_seed_hit[d]

        new_suspicious_phrases = list(suspicious_phrases)
        for d in to_remove:
            if d in new_suspicious_phrases:
                new_suspicious_phrases.remove(d)

        return new_suspicious_phrases, new_map_seed_hit, new_map_snip_seed

if __name__ == '__main__':
    runner = WrongPhraseUpdaterManager()


    """ 
    suspicious_phrases=["albert einstein the physicist", "albert einstein"]
    map_seed_hit={}
    map_seed_hit["albert einstein the physicist"] = "scientist albert einstein"
    map_seed_hit["albert einstein"] = "scientist albert Ivanov"
    map_snip_seed={}
    map_snip_seed["albert einstein the physicist"] = "scientist albert einstein"
    map_snip_seed["albert einstein"] = "scientist albert Ivanov"

    new_suspicious_phrases, new_map_seed_hit, new_map_snip_seed = runner.update_based_on_llm_similarity(suspicious_phrases, map_seed_hit, map_snip_seed)

    print(new_suspicious_phrases, new_map_seed_hit, new_map_snip_seed)

    #result = runner.perform_substitution("# about Abram Gannibal's parents are particularly sparse, "
    #                                        "primarily because he was taken from Africa at # and brought to Russia")
    #print(result)
    """

    result = runner.perform_substitution( "Albert Einstein is # ", "Albert Einstein is a driver")
        #"Boris Galitsky is # ", "Boris Galitsky is a serial killer")
        #"Bill Gates  was a CEO of #", "Bill Gates  was a CEO of Google")
    print(result)