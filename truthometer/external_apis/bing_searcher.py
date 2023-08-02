from pprint import pprint

import requests
import time
import pickle
import pandas as pd

endpoint = "https://api.bing.microsoft.com/v7.0/search"
mkt = 'en-US'
count = 50

class BingSearcher():
    def __init__(self):
        from truthometer.key_manager import provider_key
        self.query_results_cache = {}
        self.phrase_snippets = []
        self.phrase_snippets_current = []
        self.MAX_RESULTS_PER_PHRASE = 5  # 500
        self.phrase_snippets_rpt = ''
        self.report_df = pd.DataFrame()
        self.collection_path = ""
        self.bing_key = provider_key['bing']

        self.download_only = False
        try:
            self.cache_file = 'bingSearchResultsCache.bin'
            infile = open(self.cache_file, 'rb')
            self.query_results_cache = pickle.load(infile)
            infile.close()
        except Exception as ex:
            print(ex)

    def extract_phrase_from_query(self, query):
        parts = query.split('"')
        if len(parts) > 2:
            return parts[1]
        else:
            return ""

    def run_search_for_a_query_and_offset(self, query: str, offset: int):
        # Construct a request
        params = {'q': query, 'mkt': mkt, 'count': 50, 'offset': offset}
        headers = {'Ocp-Apim-Subscription-Key': self.bing_key}

        # Call the API
        web_pages = None
        try:
            rjson = self.query_results_cache.get(query + " " + str(offset))
            if not rjson:
                response = requests.get(endpoint, headers=headers, params=params)
                response.raise_for_status()

                print("\nHeaders:\n")
                print(response.headers)

                print("\nJSON Response:\n")
                rjson = response.json()
                self.query_results_cache[query + " " + str(offset)] = rjson
                outfile = open(self.cache_file, 'wb')
                pickle.dump(self.query_results_cache, outfile)
                outfile.close()
                pprint(response.json())
            web_pages_for_value = rjson.get('webPages')
            if not web_pages_for_value:
                return 0
            web_pages = web_pages_for_value.get('value')
            if not web_pages:
                return 0
        except Exception as ex:
            print(ex)

        return web_pages


if __name__ == '__main__':
    import os
    os.chdir("..")
    web_pages = BingSearcher().run_search_for_a_query_and_offset('what is distance between istanbul and ankara', 0)
    path = 'resources'
    if not web_pages:
        exit(-1)
    web_pages = web_pages.get('value')
    if not web_pages:
        exit(-1)
    for w in web_pages:
        try:
            # download the data behind the URL
            if not w:
                break
            url = w.get('url')
            filename = url.split('/')[-1]
            print("downloading doc from " + url + " ...")
            resp = requests.get(url, timeout=10)  # 3. Open the response into a new file called instagram.ico
            full_filename_path = path + w.get('name') + '_' + filename
            if not full_filename_path.endswith('.pdf'):
                full_filename_path = full_filename_path + '.pdf'
            open(full_filename_path, "wb").write(resp.content)
            print("downloaded " + str(w))
        except Exception as ex:
            print(ex)
