import pandas

df = pandas.read_csv('api_keys/api_keys.csv')

provider_key = {}
for  _, row in df.iterrows():
    provider_key[row['provider']] = row['key']