---
layout: post
title: "Unveiling the Construction Conundrum: Over-Promising, Under-Delivering, and the Data Behind Project Realities - Part 1"
date: 2023-11-29 09:30:00-0400
description: Defining the Research Question and Getting the Data
tags: links code api
categories: Project 
giscus_comments: true
related_posts: true
thumbnail: assets/img/bigApple.png
---

Have you ever heard the phrase "under promise and over deliver"? 

This adage is often hailed as a guiding principle for success in business because it advocates for setting conservative expectations and then surpassing them. The idea is that setting low expectations for a project's scope or timeline and then surpassing that expectation will leave the client "< a href="https://www.brainyquote.com/quotes/luvvie_ajayi_908808">pleasantly surprised</a>" by the delivered results. 

Maybe it's okay to "under promise and then over deliver"? It <a href="https://cedw.medium.com/maybe-its-time-to-stop-saying-under-commit-and-over-deliver-4e945e1b70f3">might not convey integrity or build trust</a>, but if the low bar we "under promise" to deliver is high enough for project stakeholders then even if we do not "over deliver" we can still be successful.

But what happens when this ethos clashes with the nature of the project and creates a sort of prisoner's dilemma?

Picture the scenario of multiple construction firms vying for a project bid. In an attempt to secure contracts, these companies often succumb to the pressure of over-promising swift project completion at minimal costs. It's a strategy that seemingly wins bids, yet the ultimate question remains unanswered: can they actually deliver on these ambitious promises?

This discrepancy between promised timelines and actual project completion has long been a thorn in the side of stakeholders. Clients eagerly award contracts to the lowest bidder with the fastest projected timeline, only to find themselves grappling with prolonged construction, unexpected delays, and budget overruns.

Intrigued by this dilemma, I embarked on a data-driven journey into the heart of construction project timelines to see just how often they are actually delayed and find an answer to the question

> Do construction projects "under promise and over deliver" or "over promise and under deliver"?

## Getting A Data-driven Answer
Finding data to answer this question is tricky and creates a few problems. 
1. It's easiest to find and access public records but from what I've seen, they are usually only for a particular city or state so it will be hard to make conclusions broadly. 
2. Each state and city will likely have different ways of storing the data so it's easiest to focus on one area first and then see if it's possible to add other areas later on. 
3. It's hard to tell if the local government did the project or if an outside company was hired.

#### The Data Source
For now, all the analysis is on data from the New York City's <a href="https://opendata.cityofnewyork.us/">Open Data</a> website. The main data set I'm pulling from is <a href="https://data.cityofnewyork.us/City-Government/Capital-Project-Detail-Data-Milestones/s7yh-frbm">Capital Project Detail Data - Milestones</a>. I chose this because it breaks up each project into different tasks or phases and has data on when each task was scheduled to start and end as well as when it *actually* started and ended. This data set is provided by the Mayor's Office of Management and Budget and was last updated just a little over a month before completing this project. 

All the code I used for this project is included in a GitHub Repository <a href="https://github.com/aoustrich/NYC_ConstructionDelays">here</a>.

The raw dataset is very large (almost 500k rows) so to avoid API limits I created an account with the NYC Open Data site and created an API Key and Secret. To maintain privacy, I stored these values in an untracked file within my repository and import the values in line 6 of the `getData.py` script.

#### Getting and Cleaning the Data
After reading the documentation, the API call was rather straightforward. Since this dataset uses the latest version of the API I was able to add the parameter `?$limit=497727` at the end of the url to get all the rows at once and avoid working with pagination. 

I created a pandas dataframe of the dataset in JSON format and then removed duplicate rows to decrease the size of the final dataset I used for my analysis called `nycMilestones.csv`. This final dataset has all 12 columns but only 59,554 rows instead of 497,727. 

Cleaning the data was relatively easy to do. The most important values are the original and actual start and end dates for the tasks of the projects so I converted them to pandas datetimes and then found the `time delta` values for each task.

## Next Step in the Project
After defining the research question, finding a data source, collecting, and cleaning the data it's time to dig in to the heart of the project and start some EDA. 

Stay tuned for Part 2!