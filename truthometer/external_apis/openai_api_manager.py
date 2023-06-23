import os
import openai

from truthometer.key_manager import provider_key

"""
curl https://api.openai.com/v1/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer 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" \
-d '{"model": "text-davinci-003", "prompt": "Peter is a security guard, and Mary is a spy. Mary wants to know what is in Peter bag. How can Peter learn if she knows what is in his bag?", "temperature": 0, "max_tokens": 7}'

"""

openai.api_key = provider_key['openai']


class OpenAI_Manager:

    def run(self, query):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            #temperature=0,
            max_tokens=300 #,
            #top_p=1,
            #frequency_penalty=0.0,
            #presence_penalty=0.0,
            #stop=["\n"]
        )
        return response["choices"][0]["text"]

if __name__ == "__main__":
    response = OpenAI_Manager().run("Sales tax rate in Virginia")
        #"Population of Jaipur in India is 3,046,163 (2020 India Census)")
        #"Population of the largest cities in India are")
        #"The difference in height between the current and previous US president is")
        #"Obama's height is")
        #"The driving distance between two largest cities in Turkey is")
    print(response)
