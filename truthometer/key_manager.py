import pandas
import os

curr_dir = os.getcwd()

print("curr_dir = " + curr_dir)

if curr_dir.endswith("Truthful"):
    path_to_config = "truthometer/api_keys/api_keys.csv"
elif not curr_dir.endswith('truthometer'):
    path_to_config = "../api_keys/api_keys.csv"
else:
    path_to_config = "api_keys/api_keys.csv"
df = pandas.read_csv(path_to_config)

provider_key = {}
for  _, row in df.iterrows():
    provider_key[row['provider']] = row['key']