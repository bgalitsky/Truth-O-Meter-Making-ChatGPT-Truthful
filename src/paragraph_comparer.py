from transformers import pipeline

class ParagraphComparer:

    """A transformer-based NLP system for generating reading comprehension-style questions from
    texts. It can generate full sentence questions, multiple choice questions, or a mix of the
    two styles.

    To filter out low quality questions, questions are assigned a score and ranked once they have
    been generated. Only the top k questions will be returned. This behaviour can be turned off
    by setting use_evaluator=False.
    """

    def __init__(self) :
        model_name = "deepset/roberta-base-squad2"

        self.qa = pipeline('question-answering', model=model_name, tokenizer=model_name)
        # todo : replace with T5 question generator
        #self.qg = QuestionGenerator()

    def generate_questions_for_text(self, text):
        return self.qg.generate(text, num_questions=20)

    def compute_questions_answers_canonical_answers_for_text(self, text):
        questions_answers_canonical_answers = []
        questions_canonical_answers = self.qg.generate(text, num_questions=10)
        for r in questions_canonical_answers:
            QA_input = {
                'question': r['question'],
                'context': text}
            qa_res = self.qa(QA_input)
            print(r['question'])
            print(qa_res['answer'])
            print("orig answer ='" + r['answer'])
            questions_answers_canonical_answers.append((r['question'], qa_res['answer'], r['answer']))
        return questions_answers_canonical_answers

    def answer_foreign_questions(self, text, questions_answers_canonical_answers_other_text):
        questions_answers_canonical_answers = []
        for r in questions_answers_canonical_answers_other_text:
            QA_input = {
                'question': r[0],
                'context': text}
            qa_res = self.qa(QA_input)
            print(r[0])
            print(qa_res['answer'])
            print("orig answer ='" + r[1])
            questions_answers_canonical_answers.append((r[0], qa_res['answer'], r[1]))
        return questions_answers_canonical_answers

if __name__ == "__main__":
    comparer = ParagraphComparer()
    text1 = "An ice cube will generally melt slower in oil compared to water. This is because the temperature of oil is higher than the melting point of ice, but oil is a poor conductor of heat compared to water. As a result, the ice cube will take longer to absorb enough heat from the oil to melt, compared to if it were in water. In water, the ice cube will absorb heat more quickly and melt faster due to the high heat conductivity of water."
    text2 = "After the ice cube melts completely in a glass containing both water and oil, the water level will indeed increase. The portion of the ice cube that was previously within the water will displace an equivalent volume of water, causing the water level to rise. The oil will still float on top of the water, and its level will remain unchanged."

    questions_answers_canonical_answers = comparer.compute_questions_answers_canonical_answers_for_text(text1)
    questions_answers_canonical_answers_other = comparer.answer_foreign_questions(text2,questions_answers_canonical_answers)
    print(questions_answers_canonical_answers_other)
