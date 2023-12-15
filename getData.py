import pandas as pd
import requests
import json
import numpy as np
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from creds import * # import api key and secret

# ------------------------------------------------------------------
# Get the project milestone data from the NYC Open Data API
# ------------------------------------------------------------------

from requests.auth import HTTPBasicAuth
basic = HTTPBasicAuth(nyc_api_key, nyc_api_secret)
milestones_request = requests.get('https://data.cityofnewyork.us/resource/s7yh-frbm.json?$limit=497727', auth=basic)
milestones = pd.read_json(milestones_request.text)

# ------------------------------------------------------------------
# Start Cleaning the data
# ------------------------------------------------------------------

# Drop duplicates and rows with missing values
milestones = milestones.drop_duplicates(subset = ['project_id','seq_number'],keep='last').reset_index(drop=True)
milestones.dropna(axis = 0, subset=['orig_start_date','orig_end_date','task_start_date','task_end_date'],inplace=True)

# Convert date columns to datetime and drop unnecessary columns
milestones["orig_start_date"] = pd.to_datetime(milestones['orig_start_date'])
milestones["orig_end_date"] = pd.to_datetime(milestones['orig_end_date'])
milestones["task_start_date"] = pd.to_datetime(milestones['task_start_date'])
milestones["task_end_date"] = pd.to_datetime(milestones['task_end_date'])
milestones = milestones.drop(columns=['pub_date','managing_agcy_cd'], axis=1)

# Export to CSV (Warning: Large file!!!)
milestones.to_csv("data/nycMilestones.csv",index=False) 

# Create a new dataframe with the columns we need (This will be smaller and easier to work with)
projectSteps = pd.DataFrame()

# Create columns for project_id, managing_agency, boro, step, and task from the milestones dataset
projectSteps[["project_id","managing_agency","boro","step","task"]] = milestones[["project_id","managing_agcy","boro","seq_number","task_description"]]

# Create columns for the difference in months for the project start and end dates
projectSteps["starting_delta"]= ((milestones.task_start_date - milestones.orig_start_date)/np.timedelta64(1, 'M'))
projectSteps["ending_delta"]= ((milestones.task_end_date - milestones.orig_end_date)/np.timedelta64(1, 'M'))
    # NOTE: Negative starting and ending deltas mean the task was started earlier than scheduled!!!

# Convert the delta columns to integers (months)
projectSteps["starting_delta"] = projectSteps["starting_delta"].astype(int)
projectSteps["ending_delta"] = projectSteps["ending_delta"].astype(int)

# Export to CSV
projectSteps.to_csv("data/projectSteps.csv",index=False)

# ------------------------------------------------------------------
# Create and export a dataframe for a heatmap of project time deltas
# ------------------------------------------------------------------

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

# Prepare projectDeltas DataFrame from the starts and finishes dataframes
projectDeltas = pd.DataFrame()
projectDeltas['Project ID'] = projectStarts['project_id']
projectDeltas['Start Status'] = projectStarts['startStatus']
projectDeltas['End Status'] = projectFinishes['endStatus']

# Create a heatmap DataFrame and export to CSV
deltasHeatMapDF = projectDeltas.groupby(['Start Status', 'End Status']).size().unstack().fillna(0)
deltasHeatMapDF = deltasHeatMapDF.reindex(columns=["Early", "On Time", "Late"], index=["Late", "On Time", "Early"]).T
deltasHeatMapDF.to_csv('data/deltasHeatMapDF.csv', index=True, header=True)


# ------------------------------------------------------------------
# Get the project budget data from the NYC Open Data API
# ------------------------------------------------------------------
    # NOTE: This uses the same API key and secret as the milestones data
    #       and the same basic authentication method created earlier
budget_request = requests.get('https://data.cityofnewyork.us/resource/wa2y-rh4b.json?$limit=72437', auth=basic)
budget = pd.read_json(budget_request.text)

# Save the budget data to a CSV file
budget.to_csv('data/budget.csv', index=False)

# ------------------------------------------------------------------
# Cleaning the budget data
# ------------------------------------------------------------------

# Merge budget and project data on project_id - (inner join)
projectCosts = budget[['project_id','boro','managing_agcy',
                       'orig_bud_amt','city_plan_total','noncity_plan_total']]\
                    .merge(projectSteps[['project_id','starting_delta','ending_delta']],
                            on='project_id',
                            how='inner') \
                    .groupby('project_id')\
                        .agg({'boro':'first',
                            'managing_agcy': 'first',
                            'orig_bud_amt': 'first', 
                            'city_plan_total': 'max', 
                            'noncity_plan_total': 'max',
                            'starting_delta': 'first',
                            'ending_delta': 'first'})\
                    .reset_index()

# Create columns for total_cost and cost_delta
projectCosts['total_cost']= projectCosts['city_plan_total'] + projectCosts['noncity_plan_total']
projectCosts['cost_delta']= projectCosts['total_cost'] - projectCosts['orig_bud_amt']

# Create a column for costStatus 
projectCosts['costStatus'] = np.select([
                                        (projectCosts['cost_delta'] < 0),    # Condition for "Under Budget"
                                        (projectCosts['cost_delta'] > 0)],    # Condition for "Over Budget"
                                        ['Under Budget',
                                         'Over Budget'],
                                        default='On Target')  # Default value if none of the conditions is met
                                       
# Join on the projectStarts and projectFinishes dataframes to get the start and end status
projectCosts = projectCosts.merge(projectStarts[['project_id','startStatus']], 
                                    on='project_id', 
                                    how='inner') \
                            .merge(projectFinishes[['project_id','endStatus']], 
                                    on='project_id', 
                                    how='inner')

# Calculate columns for percent funded by city and non-city
projectCosts['city_pct'] = projectCosts['city_plan_total'] / projectCosts['total_cost']
projectCosts['noncity_pct'] = projectCosts['noncity_plan_total'] / projectCosts['total_cost']

# Create a categorical column for who funded the project
projectCosts['funded_by'] = np.select([
                                        (projectCosts['noncity_pct'] == 1.0) , # Condition for "Non-City"
                                        (   (projectCosts['city_pct']<1.0) & 
                                            (projectCosts['noncity_pct']>0)     )],  # Condition for "Both"
                                    ['Non City',
                                     'Both'],
                                default='City' ) # Default value if none of the conditions are met

# Create a categorical column for who funded the majority of the project                    
projectCosts['majority_funder'] = np.select([
                                            (projectCosts['city_pct'] <= .5)],   # Condition for "Non-City"
                                            ['non_city'],
                                            default='city')  # Default value if none of the conditions are met
 
# Calculate a column for budget usage
projectCosts["budget_usage"]=np.select([
                            ( projectCosts['costStatus'] == "On Target"),  # Condition for a non 0 budget
                            (projectCosts['orig_bud_amt'] == 0)], # Condition for a budget start value of 0
                            [1.0,
                            (projectCosts['cost_delta']/1)],
                            default= (projectCosts['cost_delta']/projectCosts['orig_bud_amt'])   # Default value if none of the conditions are met
                            )   

# Write to csv
projectCosts.to_csv('data/projectCosts.csv')

# --------------------------------------------------------------------
# Create and export a dataframe for a heatmap of project cost statuses
# --------------------------------------------------------------------
costStatusHeatMapDF = projectCosts.groupby(['costStatus','endStatus'])\
                                    .size().unstack()\
                                    .reindex(columns=["Late","On Time","Early"],
                                             index=["Under Budget","On Target","Over Budget"]).T
costStatusHeatMapDF.to_csv('data/costStatusHeatMapDF.csv', index=True, header=True)