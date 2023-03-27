

text1 =  """
Getting investment in the natural language processing (NLP) domain can be challenging for several reasons, including:

High level of technical complexity: NLP is a highly technical field that requires a deep understanding of linguistics, machine learning, and artificial intelligence. Investors may be hesitant to invest in NLP ventures because they lack the technical expertise to evaluate the potential of the technology.

Limited adoption: Despite significant advancements in NLP technology, adoption of NLP solutions has been relatively slow. This can make it difficult for investors to justify investing in NLP ventures that may not generate revenue in the short term.

Data privacy concerns: NLP involves the processing of vast amounts of textual data, which can raise concerns around data privacy and security. Investors may be hesitant to invest in NLP ventures that may face regulatory hurdles or public scrutiny around data privacy.

High research and development costs: Developing NLP solutions can be expensive and time-consuming, especially for startups that lack the resources of larger tech companies. Investors may be hesitant to invest in NLP ventures that require significant R&D costs without a clear path to profitability.

Limited talent pool: NLP is a specialized field that requires a unique skill set. Finding qualified NLP talent can be challenging, especially for startups that are competing with larger tech companies for talent.
"""



text2 = """
"""

def adapt_chatgpt_format(text):
    sections = text.split(':')
    if len(sections)>2:  ## >5
        header = sections[0]
        for_position = header.find(' for ')
        header = header[0:for_position]
        clauses = text.split("\n\n")
        if len(clauses)>1:
            clauses = clauses[1:1000]
            new_clauses = []
            for clause in clauses:
                pos_semicolon = clause.find(':')
                remainder = clause[pos_semicolon+2: len(clause)]
                clause = header + ": " + clause[0:pos_semicolon]  + '. ' + remainder
                new_clauses.append(clause)
            normalized_text = '\n'.join(new_clauses)
            return normalized_text

    return text

if __name__ == "__main__":
    print(adapt_chatgpt_format(text1))
    print(adapt_chatgpt_format(text2))

