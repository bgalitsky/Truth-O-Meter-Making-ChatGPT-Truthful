from fact_checker_via_web import FactCheckerViaWeb
from html.verification_page_builder import VerificationPageBuilder

from third_party_models.chat_gpt_answer_format_adapter import adapt_chatgpt_format

html_builder = VerificationPageBuilder()

if __name__ == '__main__':
    text_plus_minus =""" 
        # +
        "Fraud and corruption within a bank can lead to its failure. "
        "Discourse analysis can be used to analyze classroom interactions, textbooks, and educational policies. "
        "Discourse analysis can be used to analyze political speeches, debates, and media coverage. ",
        "required to file a non-resident tax return in the state where the financial institution is located. "
        "Discourse analysis is a qualitative research method that aims to understand the use of language in social interactions. ",
        "Discourse analysis can be used to analyze doctor-patient interactions, medical records, and healthcare policies. ",
        "Lack of diversification lead to bank failure",
        # -
        "Healthcare discourse analysis. ",
        "Corporate discourse analysis. ",
        "Discourse analysis can be used to analyze social justice issues, including race, gender, sexuality. ",
        "discourse analysis is a versatile method that can be applied to a wide range of social phenomena. ",
        "Failure by regulatory authorities to adequately supervise and enforce regulations can contribute to a bank's failure. ",
        "Fraud and corruption within a bank can lead to its failure. ",
        """


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

    poi_text = "Local cuisine: Anamur is known for its delicious local cuisine, which includes dishes such as stuffed mussels, grilled octopus, and goat meat. Visitors can sample these dishes at local restaurants and cafes throughout the district."

    text = adapt_chatgpt_format( text2chat_gpt) #poi_text

    fact_checker.perform_and_report_fact_check_for_text(text)
    result = fact_checker.html_builder.verif_page_content
    print(result)
    """ 
    assert (
                result == "Local cuisine: Anamur is known for its delicious local cuisine, which includes dishes such as <s>stuffed mussels</s>, <s>grilled octopus</s>, and <s>goat meat</s>.\n"
                          "<br>Visitors can sample these dishes at <s>local restaurants</s> and cafes throughout the district.\n"
                          "<br>")
    """
disc_an_txt= """
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

