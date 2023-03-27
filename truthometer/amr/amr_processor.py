from typing import List

import amrlib
import spacy


class AmrProcessor:
    """
    Obtains AMR parse and extracts 'names' from it
    relies on parse_sents(self, sents, add_metadata=True, return_penman=False, disable_progress=True, pbar_desc=None):

    # https://github.com/bjascob/amrlib/blob/05e9b4380d99c8a98e6a214f1e952d704d70ac4c/amrlib/models/parse_spring/inference.py
    """

    def __init__(self):
        # Loads  AMR model and spacy
        self.stog = amrlib.load_stog_model()
        amrlib.setup_spacy_extension()
        self.nlp = spacy.load('en_core_web_sm')
        self.party_synonyms = ['party', 'customer', 'client', 'vendor', 'company']


    def amr_parse_penman(self, text: str) -> list:
        return self.stog.parse_sents([text], return_penman=True)

    def amr_parse(self, text: List[str]) -> list:
        graphs = self.stog.parse_sents([text])
        return graphs

    def amr_graph_parse(self, text: str) -> list:
        doc = self.nlp(text)
        graphs = doc._.to_amr()
        return graphs

    def extract_names(self, graphs: list) -> list:
        """
        Extracts names that should be removed from sentence for de-identification
        """
        identified_names = []
        for graph in graphs:
            terms = graph.split('\n')
            multiword_name = ""
            # we iterate through each node looking for node with 'names'. Once we find ':name' we iterate through
            # consecutive this is a typical case we then form a multi-word from all name tokens. Example is below:
            '''
                              :domain (z6 / company
                        :name (z7 / name
                              :op1 "Global"
                              :op2 "Media"
                              :op3 "Services"))
            '''
            for i in range(0, len(terms)):
                key_name = terms[i].find(':name')
                if key_name > 0:
                    # we start from the next node and extract name up to 4 tokens must. If name does not fit into 4
                    # tokens then we assume it is AMR error and still extract only 4
                    for j in range(i + 1, i + 5):
                        if j >= len(terms):
                            continue
                        if terms[j].find(':op') < 0:
                            continue

                        lookups = terms[j].split("\"")
                        if len(lookups) > 2:
                            name = lookups[1]
                            # it is AMR name but in allow_list
                            if self.allow_list.is_in_allow_list(name.capitalize()):
                                continue

                            if len(name) > 2:
                                multiword_name += " " + name

                if len(multiword_name) > 0:
                    identified_names.append(multiword_name.strip())
                    multiword_name = ""
            # Now we do atypical case, where AMT caanot extarct a single token which is a name
            # We extract 'segment' from node label:
            # :ARG0 (z1 / segment)
            # extract subject
            for i in range(1, 4):
                if i >= len(terms):
                    break
                pos_name = terms[i].find(':ARG0')
                pos_name_end = terms[i].find(')')
                if pos_name > -1 and pos_name_end > -1:
                    name = terms[i][pos_name + 12:pos_name_end]
                    if len(name) > 4:
                        # not a 'Party' and starts with capital
                        if not name in self.party_synonyms:
                            identified_names.append(name[0].upper() + name[1:])
                            break

            print(graph)

        print(identified_names)
        return identified_names

    """
    
(z0 / use-01
      :ARG0 (z1 / segment)
      :ARG1 (z2 / effort-01
            :ARG0 z1
            :ARG1-of (z3 / reasonable-02
                  :mod (z4 / commerce)))
      :ARG2 (z5 / minimize-01
            :ARG0 z1
            :ARG1 (z6 / disrupt-01
                  :mod (z7 / any)))
      :condition (z8 / out-02
            :ARG1-of (z9 / describe-01
                  :location (z10 / above))))
    """

    @staticmethod
    def find_between(s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def extract_names_with_spacy_extension(self, text) -> list:
        """
        Extracts names that should be removed from sentence for de-identification
        by using spacy extension
        """
        identified_names = []
        doc = self.nlp(text)
        graphs = doc._.to_amr()

        for graph in graphs:
            terms = graph.split('\n')
            for i in range(0, len(terms)):
                key_name = terms[i].find(':name')
                if key_name > 0:
                    for j in range(i + 1, i + 5):
                        if j >= len(terms):
                            continue
                        if terms[j].find(':op') < 0:
                            continue
                        lookups = terms[j].split("\"")
                        if len(lookups) > 2:
                            name = lookups[1]
                            identified_names.append(name)
            print(graph)
        return identified_names
