import pandas as pd
import requests
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from creds import *

from requests.auth import HTTPBasicAuth
basic = HTTPBasicAuth(nyc_api_key, nyc_api_secret)
r = requests.get('https://data.cityofnewyork.us/resource/s7yh-frbm.json?$limit=497727', auth=basic)
df = pd.read_json(r.text)

df = df.drop_duplicates(subset = ['project_id','seq_number'],keep='last').reset_index(drop=True)
# print(df.shape)
df.dropna(axis = 0, subset=['orig_start_date','orig_end_date','task_start_date','task_end_date'],inplace=True)
df.to_csv("data/nycMilestones.csv",index=False) 