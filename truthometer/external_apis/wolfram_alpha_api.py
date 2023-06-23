#https://api.wolframalpha.com/v1/result?i=what+is+distance+between+istanbul+and+Ankara%3F&appid=GG4LKE-XR4977667U
#https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/
import requests
from wolframalpha import Client

from truthometer.key_manager import provider_key

wolfram_key = provider_key['wolfram']

class WolframApi():
    def run_search_for_a_query(self, query: str):
        # Construct a request
        endpoint = f"https://api.wolframalpha.com/v1/result?i={query}%3F&appid={wolfram_key}"
        response = requests.get(endpoint)
        response.raise_for_status()
        return str(response.content)

    def run_via_wolfram(self, query):
        client = Client(wolfram_key)
        res = client.query('temperature in Washington, DC on October 3, 2012')
        for pod in res.pods:
            print(pod.texts)
            for sub in pod.subpods:
                print(sub.plaintext)



if __name__ == '__main__':
    answer = WolframApi().run_search_for_a_query('how tall Trump')
        #'distance istanbul and ankara')
    print(answer)
