import http.client
import json


class GoogleSerpSearcher():
    def __init__(self, api_key=None):
        from truthometer.key_manager import provider_key
        try:
            self.google_serp_key = provider_key['google_serp']
        except:
            assert api_key, "you should use your own google serp api key"
            self.google_serp_key = api_key
        self.headers =  {
          'X-API-KEY': self.google_serp_key,
          'Content-Type': 'application/json'
        }
        self.conn = http.client.HTTPSConnection("google.serper.dev")
        if api_key:
            self.google_serp_key = api_key

    def run_search_for_a_query(self, query: str):
        payload = json.dumps({
          "q": query,
          'num': 100
        })

        self.conn.request("POST", "/search", payload, self.headers)
        res = self.conn.getresponse()
        data = res.read()
        # to match tags of Bing
        data_str = data.decode("utf-8").replace('\"title\"', '\"name\"')
        json_object = json.loads(data_str)
        return json_object.get("organic")

    
if __name__ == '__main__':
    import os
    os.chdir("..")

    web_pages = GoogleSerpSearcher().run_search_for_a_query('what is distance between istanbul and ankara')
    if not web_pages:
        exit(-1)

    for w in web_pages:
        try:
            # download the data behind the URL
            if not w:
                break
            print(w.get("name"))
            print(w.get("link"))
            print(w.get("snippet"))
        except Exception as ex:
            print(ex)

# "title":"Apple Inc. - Wikipedia","link":"https://en.wikipedia.org/wiki/Apple_Inc.","snippet":"