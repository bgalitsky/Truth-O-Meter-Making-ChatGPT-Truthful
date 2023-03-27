from youtubesearchpython import VideosSearch

def videoSearch(query:str, count:int):
    videosSearch = VideosSearch(query, limit = count)
    results = videosSearch.result()
    r = results['result']
    return r

if __name__ == '__main__':
    results = videoSearch('sup board', 2)
    print(results)