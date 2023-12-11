import pandas as pd
import requests
import json
import numpy as np
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

milestones["orig_start_date"] = pd.to_datetime(milestones['orig_start_date'])
milestones["orig_end_date"] = pd.to_datetime(milestones['orig_end_date'])
milestones["task_start_date"] = pd.to_datetime(milestones['task_start_date'])
milestones["task_end_date"] = pd.to_datetime(milestones['task_end_date'])
milestones = milestones.drop(columns=['pub_date','managing_agcy_cd'], axis=1)

milestones.to_csv("data/nycMilestones.csv",index=False) 

# preprocess the prooject steps
projectSteps = pd.DataFrame()
projectSteps[["project_id","managing_agency","boro","step","task"]] = milestones[["project_id","managing_agcy","boro","seq_number","task_description"]]

projectSteps["starting_delta"]= ((milestones.task_start_date - milestones.orig_start_date)/np.timedelta64(1, 'M'))
projectSteps["ending_delta"]= ((milestones.task_end_date - milestones.orig_end_date)/np.timedelta64(1, 'M'))

""" Negative starting and ending deltas mean the task was started earlier than scheduled!!! """
projectSteps["starting_delta"] = projectSteps["starting_delta"].astype(int)
projectSteps["ending_delta"] = projectSteps["ending_delta"].astype(int)

projectSteps.to_csv("data/projectSteps.csv",index=False)

# ---------------------------------------------
# Group by 'project_id' to get the min and max values for 'step' and 'starting_delta' columns
projectStarts = projectSteps.groupby('project_id').agg({'step': 'min', 'starting_delta': 'first'}).reset_index()
projectFinishes = projectSteps.groupby('project_id').agg({'step': 'max', 'ending_delta': 'first'}).reset_index()

# Define a function to determine status based on delta values
def get_status(delta):
    if delta < 0:
        return 'Early'
    elif delta > 0:
        return 'Late'
    else:
        return 'On Time'

# Create columns for start and end status based on delta values
projectStarts['startStatus'] = projectStarts['starting_delta'].apply(get_status)
projectFinishes['endStatus'] = projectFinishes['ending_delta'].apply(get_status)

# Prepare projectDeltas DataFrame
projectDeltas = pd.DataFrame()
projectDeltas['Project ID'] = projectStarts['project_id']
projectDeltas['Start Status'] = projectStarts['startStatus']
projectDeltas['End Status'] = projectFinishes['endStatus']

# Create a heatmap DataFrame and export to CSV
deltasHeatMapDF = projectDeltas.groupby(['Start Status', 'End Status']).size().unstack().fillna(0)
deltasHeatMapDF = deltasHeatMapDF.reindex(columns=["Early", "On Time", "Late"], index=["Late", "On Time", "Early"]).T
deltasHeatMapDF.to_csv('data/deltasHeatMapDF.csv', index=True, header=True)


# ---------------------------------------------
# Do the same for the budget dataset
budget_request = requests.get('https://data.cityofnewyork.us/resource/wa2y-rh4b.json?$limit=72437', auth=basic)
budget = pd.read_json(budget_request.text)

budget.to_csv('data/budget.csv', index=False)

# ---------------------------------------------
# merge budget and projectSteps on project_id (inner join)
costs = budget[['project_id','boro','managing_agcy','orig_bud_amt','city_plan_total','noncity_plan_total']]\
    .merge(projectSteps[['project_id','starting_delta','ending_delta']], on='project_id', how='inner')

projectCosts = costs.groupby('project_id').agg({'boro':'first',
                                 'managing_agcy': 'first',
                                 'orig_bud_amt': 'first', 
                                 'city_plan_total': 'max', 
                                 'noncity_plan_total': 'sum',
                                 'starting_delta': 'first',
                                 'ending_delta': 'first'}).reset_index()

projectCosts['total_cost']= projectCosts['city_plan_total'] + projectCosts['noncity_plan_total']
projectCosts['cost_delta']= projectCosts['total_cost'] - projectCosts['orig_bud_amt']
projectCosts['costStatus'] = np.select([
                                    (projectCosts['cost_delta'] < 0),    # Condition for "Under Budget"
                                    (projectCosts['cost_delta'] > 0)     # Condition for "Over Budget"
                                ],
                                [
                                    'Under Budget',
                                    'Over Budget'
                                ],
                                default='On Target'  # Default value if none of the conditions is met
                            )   
projectCosts = projectCosts.merge(projectStarts[['project_id','startStatus']], 
                                    on='project_id', 
                                    how='inner')        \
                .merge(projectFinishes[['project_id','endStatus']], 
                                    on='project_id', 
                                    how='inner')
projectCosts['city_pct'] = projectCosts['city_plan_total'] / projectCosts['total_cost']
projectCosts['noncity_pct'] = projectCosts['noncity_plan_total'] / projectCosts['total_cost']
projectCosts['majority_funder'] = np.select([
                                    (projectCosts['city_pct'] <= .5)   # Condition for "Non-City"
                                ],
                                [
                                    'non_city'
                                ],
                                default='city'  # Default value if none of the conditions are met
                            )  
projectCosts["budget_usage"]=np.select([
                            ( projectCosts['costStatus'] == "On Target"),  # Condition for a non 0 budget
                            (projectCosts['orig_bud_amt'] == 0)
                            ],
                            [
                                1.0,
                                (projectCosts['cost_delta']/1) 
                            ],
                            default= (projectCosts['cost_delta']/projectCosts['orig_bud_amt'])   # Default value if none of the conditions are met
                        )   

projectCosts.to_csv('data/projectCosts.csv')

# ---------------------------------------------
costStatusHeatMapDF = projectCosts.groupby(['costStatus','endStatus']).size().unstack()
costStatusHeatMapDF  = costStatusHeatMapDF.reindex(columns=["Late","On Time","Early"],index=["Under Budget","On Target","Over Budget"]).T

costStatusHeatMapDF.to_csv('data/costStatusHeatMapDF.csv', index=True, header=True)