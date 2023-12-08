import pandas as pd
import requests
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from creds import *

from requests.auth import HTTPBasicAuth
basic = HTTPBasicAuth(nyc_api_key, nyc_api_secret)
milestones_request = requests.get('https://data.cityofnewyork.us/resource/s7yh-frbm.json?$limit=497727', auth=basic)
milestones = pd.read_json(milestones_request.text)

milestones = milestones.drop_duplicates(subset = ['project_id','seq_number'],keep='last').reset_index(drop=True)
# print(df.shape)
milestones.dropna(axis = 0, subset=['orig_start_date','orig_end_date','task_start_date','task_end_date'],inplace=True)
milestones.to_csv("data/nycMilestones.csv",index=False) 


# Do the same for the budget dataset
budget_request = requests.get('https://data.cityofnewyork.us/resource/wa2y-rh4b.json?$limit=72437', auth=basic)
budget = pd.read_json(budget_request.text)

budget.to_csv('data/budget.csv', index=False)