# https://huggingface.co/mrm8488/t5-base-finetuned-question-generation-ap

from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

def generate_question( context, answer="",max_length=100):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = tokenizer([input_text], return_tensors='pt')

  output = model.generate(input_ids=features['input_ids'],
               attention_mask=features['attention_mask'],
               max_length=max_length)

  q_token =  tokenizer.decode(output[0])
  return q_token[16: -4]

""" 
context = "while the previous president, Donald Trump, is 6 feet, 2 inches tall."
answer = ""

q = get_question(context)
print(q)
"""
