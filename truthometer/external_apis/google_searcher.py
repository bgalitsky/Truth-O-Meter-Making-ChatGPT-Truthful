import requests

from truthometer.key_manager import provider_key

google_key = provider_key['google']
cx = provider_key['cx']
# Set the API endpoint and search parameters
url = "https://www.googleapis.com/customsearch/v1"
params = {
    "key": google_key,
    "cx": "b0bb8317b601f4286",
    "q": 'a nonresident state tax return',
    "num": 10,  # Number of search results to return
    "alt": "json"  # Request JSON format
}

# Send the API request and get the response
response = requests.get(url, params=params)

# Extract the JSON data from the response
json_data = response.json()

# Process the JSON data as needed
# For example, you can print the search results:
for result in json_data['items']:
    print(result['title'])
    print(result['link'])

"""
<script async truthometer="https://cse.google.com/cse.js?cx=b0bb8317b601f4286">
</script>
<div class="gcse-search"></div>
"""