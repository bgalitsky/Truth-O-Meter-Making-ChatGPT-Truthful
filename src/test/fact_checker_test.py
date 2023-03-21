import pytest

from fact_checker_via_web import FactCheckerViaWeb, nlp
from third_party_models.chat_gpt_answer_format_adapter import adapt_chatgpt_format


class TestFactChecker:
    @pytest.mark.parametrize(
        "text, expected_output",
        [
            ("Fraud and corruption within a bank can lead to its failure. "
             "Discourse analysis can be used to analyze classroom interactions, textbooks, and educational policies. "
             "Discourse analysis can be used to analyze political speeches, debates, and media coverage. "
             "required to file a non-resident tax return in the state where the financial institution is located. "
             "Discourse analysis is a qualitative research method that aims to understand the use of language in social interactions. "
             "Discourse analysis can be used to analyze doctor-patient interactions, medical records, and healthcare policies. "
             "Lack of diversification lead to bank failure"
             # -
             "Healthcare discourse analysis. "
             "Corporate discourse analysis. "
             "Discourse analysis can be used to analyze social justice issues, including race, gender, sexuality. "
             "discourse analysis is a versatile method that can be applied to a wide range of social phenomena. "
             "Failure by regulatory authorities to adequately supervise and enforce regulations can contribute to a bank's failure. "
             "Fraud and corruption within a bank can lead to its failure. "
             ,
             # expressions in <s>...</s> like <s>textbooks</s> are purhaps not truthful
             'Fraud and corruption within a bank can lead to its failure.'
             ' <br>Discourse analysis can be used to analyze classroom interactions, '
             '<s>textbooks</s>, and <s>educational policies</s>.'
             ' <br>Discourse analysis can be used to analyze political speeches, '
             '<s>debates</s>, and <s>media coverage</s>.'
             ' <br>required to file a non-resident tax return in the state where the '
             'financial institution is located.'
             ' <br>Discourse analysis is a qualitative research method that aims to '
             'understand the use of language in social interactions.'
             ' <br>Discourse analysis can be used to analyze doctor-patient interactions, '
             'medical records, and <s>healthcare policies</s>.'
             ' <br>Lack of diversification lead to bank failureHealthcare discourse '
             'analysis.'
             ' <br>Corporate discourse analysis.'
             ' <br>Discourse analysis can be used to analyze social justice issues, '
             'including race, gender, sexuality.'
             ' <br>discourse analysis is a versatile method that can be applied to a wide '
             'range of social phenomena.'
             ' <br>Failure by regulatory authorities to adequately supervise and enforce '
             "regulations can contribute to a bank's failure."
             ' <br>Fraud and corruption within a bank can lead to its failure.'
             ' <br>'
             ),
            (
                    "The reason of bank failure is Fraud and misconduct. If a bank engages in fraudulent or unethical practices, it can suffer reputational damage, legal liabilities, and loss of customers. "
                    "That  can lead to financial distress and potentially cause the bank to fail."
                    "A bank can fail in the US, even in the recent economy due to a Lack of diversification. "
                    "If a bank's lending and investment portfolios are concentrated in a particular sector or geography, "
                    " it can increase the bank's vulnerability to economic shocks or downturns in that sector or region."
                    ,
                    'The reason of bank failure is Fraud and misconduct. <br>If a bank engages in '
                    'fraudulent or unethical practices, it can suffer reputational damage, '
                    '<s>legal liabilities</s>, and loss of customers. <br>That  can lead to '
                    'financial distress and potentially cause the bank to fail. <br>A bank can '
                    'fail in the US, even in the recent economy due to a Lack of '
                    "<s>diversification</s>. <br>If a bank's lending and investment portfolios "
                    'are concentrated in a particular sector or <s>geography</s>,  it can '
                    "increase the bank's vulnerability to economic shocks or <s>downturns</s> in "
                    'that sector or <s>region</s>. <br>'
            ),
            (
                    "Local cuisine: Anamur is known for its delicious local cuisine, which includes dishes such as stuffed mussels, grilled octopus, and goat meat. Visitors can sample these dishes at local restaurants and cafes throughout the district."
                    ,
                    # the whole thing is a lie. No such dishes and neither they are availbale in local restaurants in this location
                    'Local cuisine: Anamur is known for its delicious local cuisine, which '
                    'includes dishes such as <s>stuffed mussels</s>, <s>grilled octopus</s>, and '
                    '<s>goat meat</s>. <br>Visitors can sample these dishes at <s>local '
                    'restaurants</s> and cafes throughout the district. <br>'
            ),
            (
            "Florida real estate is relatively inexpensive compared to some other popular states for several reasons: \n"
            "Abundant land: Florida is a large state with a lot of available land for development. This means that there is less competition for land and housing compared to other states where land is scarce, which can help keep prices relatively low. \n"
            "Lower taxes: Florida has no state income tax, which can make it a more attractive place to live and work for people looking to save money. Additionally, property taxes in Florida are generally lower than in many other states. \n"
            "Climate: While Florida is known for its warm and sunny weather, it is also prone to hurricanes and other natural disasters. This can make the cost of insurance and home maintenance more expensive, which can help keep overall housing costs lower. \n"
            "Demographics: Florida has a large retirement community, which tends to be more price-sensitive and focused on finding affordable homes. Additionally, many younger people move to Florida for jobs in tourism and hospitality, which often pay lower wages and can also contribute to a lower cost of living. \n"
            "Housing inventory: Florida has a relatively high housing inventory, meaning there are more homes for sale than in some other states. This can help keep prices down as sellers compete for buyers.",
            # Truth-O-meter is unable to confirm relationship between <s>insurance and home maintenance</s> and
            #           '<s>overall housing costs</s> to keep the real estate prices lower
            'Florida real estate is relatively inexpensive compared to some other popular '
            'states: Florida real estate is relatively inexpensive compared to some other '
            'popular states. <br>Lower taxes. <br>Florida has no state income tax, which '
            'can make it a more attractive place to live and work for people looking to '
            'save money. <br>Additionally, property taxes in Florida are generally lower '
            'than in many other states.  <br>Florida real estate is relatively '
            'inexpensive compared to some other popular states: Florida real estate is '
            'relatively inexpensive compared to some other popular states. <br>Climate. '
            '<br>While Florida is known for its warm and sunny weather, it is also prone '
            'to hurricanes and other natural disasters. <br>This can make the cost of '
            '<s>insurance and home maintenance</s> more expensive, which can help keep '
            '<s>overall housing costs</s> lower.  <br>Florida real estate is relatively '
            'inexpensive compared to some other popular states: Florida real estate is '
            'relatively inexpensive compared to some other popular states. '
            '<br>Demographics. <br>Florida has a large retirement community, which tends '
            'to be more price-sensitive and focused on finding affordable homes. '
            '<br>Additionally, many younger people move to Florida for jobs in tourism '
            'and hospitality, which often pay <s>lower wages</s> and can also contribute '
            'to a lower cost of living.  <br>Florida real estate is relatively '
            'inexpensive compared to some other popular states: Florida real estate is '
            'relatively inexpensive compared to some other popular states. <br>Housing '
            'inventory. <br>Florida has a relatively high housing inventory, meaning '
            'there are more homes for sale than in some other states. <br>This can help '
            'keep prices down as sellers compete for buyers. <br>'
            )

        ]
    )
    def test_fact_checker(self, text, expected_output):
        fact_checker = FactCheckerViaWeb()
        text_adapted = adapt_chatgpt_format(text)  # poi_text)
        fact_checker.perform_and_report_fact_check_for_text(text_adapted)
        assert fact_checker.html_builder.verif_page_content.replace("\n", '') == expected_output
