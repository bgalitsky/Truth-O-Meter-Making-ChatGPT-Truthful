from src.fact_checker_via_web import FactCheckerViaWeb, nlp
from src.correction_in_web_browser_opener import html_builder
from src.html.verification_page_builder import VerificationPageBuilder
from src.phrase_enumeration_manager import extract_conj_triple_from_text
from src.third_party_models.chat_gpt_answer_format_adapter import adapt_chatgpt_format

if __name__ == '__main__':
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
    raw_texts = []
    text = "The reason of bank failure is Fraud and misconduct. If a bank engages in fraudulent or unethical practices, it can suffer reputational damage, legal liabilities, and loss of customers. That  can lead to financial distress and potentially cause the bank to fail."
    """ 
        "A bank can fail in the US, even in the recent economy due to a Lack of diversification. " \
           "If a bank's lending and investment portfolios are concentrated in a particular sector or geography, 
           it can increase the bank's vulnerability to economic shocks or downturns in that sector or region."
    """
    text2chat_gpt = """
    Florida real estate is relatively inexpensive compared to some other popular states for several reasons:

    Abundant land: Florida is a large state with a lot of available land for development. This means that there is less competition for land and housing compared to other states where land is scarce, which can help keep prices relatively low.

    Lower taxes: Florida has no state income tax, which can make it a more attractive place to live and work for people looking to save money. Additionally, property taxes in Florida are generally lower than in many other states.
    
    Climate: While Florida is known for its warm and sunny weather, it is also prone to hurricanes and other natural disasters. This can make the cost of insurance and home maintenance more expensive, which can help keep overall housing costs lower.

    Demographics: Florida has a large retirement community, which tends to be more price-sensitive and focused on finding affordable homes. Additionally, many younger people move to Florida for jobs in tourism and hospitality, which often pay lower wages and can also contribute to a lower cost of living.

    Housing inventory: Florida has a relatively high housing inventory, meaning there are more homes for sale than in some other states. This can help keep prices down as sellers compete for buyers.

    """
    fact_checker = FactCheckerViaWeb()


    text = adapt_chatgpt_format(text2chat_gpt)
    doc = nlp(text)
    for sent in doc.sents:
        raw_texts.append(sent.text)

    content = ""
    for text in raw_texts:
        print(text)
        section = fact_checker.fact_check_sentence(text)
        print(section)
        print()
        content += '\n' + section

    html_builder.write_html_page(text, content)

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
