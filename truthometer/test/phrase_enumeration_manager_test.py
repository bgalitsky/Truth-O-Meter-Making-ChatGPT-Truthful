from fact_checker_via_web import nlp
from phrase_enumeration_manager import extract_conj_triple_from_text

if __name__ == '__main__':
    """ 
    text = "Fraud and misconduct: If a bank engages in fraudulent or unethical practices, it can suffer reputational damage, legal liabilities, and loss of customers, which can lead to financial distress and potentially cause the bank to fail."
    # Process the document
    doc = nlp(text)
    phrase = extract_conj_triple_from_sentence(doc)
    print(phrase)
    phrase_str = ""
    for p in phrase:
        phrase_str += p + " "
    phrase_str.strip().rstrip()
    print( phrase_str)
    """
    text = """
    why can banks fail in current economy?
Banks can fail in the current economy for several reasons, including:
Economic downturns: When the economy experiences a recession or downturn, people and businesses may struggle to repay loans, which can result in increased loan defaults and ultimately cause banks to suffer losses.
Asset quality deterioration: If a bank's loans and investments perform poorly, the bank's assets can decrease in value, which can lead to a decline in the bank's financial health.
Liquidity issues: Banks require a steady flow of cash to meet the demands of customers, such as withdrawals, loans, and investments. 
If a bank lacks sufficient liquidity, it may struggle to meet these demands, which can result in a loss of confidence and potentially cause the bank to fail.
Regulatory violations: Banks are subject to numerous regulations, and violations of these regulations can result in fines, penalties, and even closure.
Fraud and misconduct: If a bank engages in fraudulent or unethical practices, it can suffer reputational damage, legal liabilities, and loss of customers, 
which can lead to financial distress and potentially cause the bank to fail.
    """
    doc = nlp(text)
    extract_conj_triple_from_text(doc)

