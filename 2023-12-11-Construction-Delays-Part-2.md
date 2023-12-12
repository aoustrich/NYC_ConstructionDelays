---
layout: post
title: "Unveiling the Construction Conundrum: Over-Promising, Under-Delivering, and the Data Behind Project Realities - Part 2"
date: 2023-12-11 09:30:00-0400
description: Exploratory Data Analysis and Conclusion
tags: links code eda
categories: Project 
giscus_comments: true
related_posts: true
datatable: true
thumbnail: assets/img/bigApple.png
---

> ##### Important Links
>
> Check out <a href="https://aoustrich.github.io/blog/2023/Construction-Delays-Part-1/">Part 1</a>! 
> Take a look at my <a href="https://github.com/aoustrich/NYC_ConstructionDelays">GitHub repo</a> with all my code.
{: .block-tip }

Right from the start I want to clarify that after looking into this data I’ve realized that my original question cannot be answered (at least right now). 

Perhaps the most important thing to recognize is that I know next to nothing about how government construction projects *actually* work. I don’t know how detailed project proposals are or the intricacies of the bidding process. 

I did find some answers about construction projects but the limitations of my own knowledge and the data prevent me from confidently saying construction companies over promise and then under deliver on projects. 

### Data Limitations
- All planned and actual dates for task completion are on the 1st day of the month so a project that started 1 day late and another that started 30 days late would both be considered to be 1 month late. 
- There is no way to know if government employees did the work or indepedenct contractors. My original suspicion was that independent contractors looking to win large projects and paydays would over promise their abilities because they knew some projects would have to be completed and the city would have no choice but to pay.
- There are some descriptions about why projects were delayed but there are only 12 different reasons and most are pretty vague. The two most common reasons for all the budget line items (not just the projects included in the Milestones data) are delays caused by budgetary constraints and changes in project scope/design. Changes to scope and design could be influenced by the company doing the work but also by the City and it wouldn’t be fair to blame a company’s project proposal for being way off if it was actually the City’s fault. 
- The city budget data I collected does not clearly define where the non city money comes from. We can’t readily tell if funds come from State or Federal coffers or if some money is donated by concerned citizens. 

Despite these shortcomings from my own knowledge and the data I collected, I still think this project was a success and is a step towards a final answer.

<!-- # Overview of the Data
<table
  id="table"
  data-click-to-select="true"
  data-toggle="table"
  data-height="460"
  data-pagination="true"
  data-url="{{ 'assets/json/nyc_construction/agencyDF_records.json' | relative_url }}">
  
  <thead>
    <tr>
      <!-- <th data-checkbox="true"></th> -->
      <th data-field="Managing Agency">Managing Agency</th>
      <th data-field="Count">Count</th>
    </tr>
  </thead>
</table> -->

# Over Promising and Under Delivering?

### Project Timeline  
My orinigal suspicion was that most construction projects would be finished late, but after looking into all the projects I was shocked to find out that only about 22% (1,987/8,966) projects were completed late.

As shown below, approximately 69% (6,203/8,966) projects were both started and finished on time. 

<div class="row justify-content-md-center">
    <div class="col-lg-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/nyc_construction/Project_Start_Finish_heatmap.png" title="Project Timeline Heatmap" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Source: <a href="https://data.cityofnewyork.us/City-Government/Capital-Project-Detail-Data-Milestones/s7yh-frbm">Capital Project Detail Data - Milestones</a>
</div>

It's important to remember that the dates are tracked on a monthly level so each project has a few week window in which it can be started or completed to be counted as "On Time." 

New York City is one of the busiest cities in the world but some borough are less busy than others so I wanted to see if there was a difference in project completions by Borough.

<div class="row justify-content-md-center">
    <div class="col-lg-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/nyc_construction/Project_Finish_Statuses_by_Boro.png" title="Project Finished by Borough" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Notes: "CITYWIDE" means projects took place in at least one Borough. <p>"RICHMOND" is the name of the Borough sometimes known as 'Staten Island'</p> <p>Source: <a href="https://data.cityofnewyork.us/City-Government/Capital-Project-Detail-Data-Milestones/s7yh-frbm">Capital Project Detail Data - Milestones</a> </p>
</div>


The timeline of a project is important but it's not the only factor that indicates if Construction companies over promise and under deliver on projects.  

### Project Budget

I originally thought that most projects would cost more than the original plan and I was counter-intuitively happy to learn that my theory was correct. As shown below, over half of the 8,578 construction projects were over budget. 

<div class="row justify-content-md-center">
    <div class="col-lg-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/nyc_construction/Project_Budget_Status_bar.png" title="Project Budget Statuses" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Source: <a href="https://data.cityofnewyork.us/City-Government/Capital-Project-Detail-Data-Dollars/wa2y-rh4b">Capital Project Detail Data - Dollars</a>
</div>

Again, I wanted to see if there was a difference between the Boroughs.

<div class="row justify-content-md-center">
    <div class="col-lg-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/nyc_construction/Project_Budget_Status_boro_bar.png" title="Project Budgets Statuses by Borough" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Source: <a href="https://data.cityofnewyork.us/City-Government/Capital-Project-Detail-Data-Dollars/wa2y-rh4b">Capital Project Detail Data - Dollars</a>
</div>

It's easy to imagine how some types of projects might be more expensive than others. Comparing a project to paint an entire bridge to one where bathroom sinks are replaced isn't exactly fair. Since the data don't have a manageable granularity for the scope of a project, one of the better ways of comparing different scopes is to look at the differences in the agency managing the project.

Since there were dozens of agencies in the dataset, I thought it was easiest to show the 5 agencies with the highest and lowest average cost delta (cost delta = total cost - original planned cost). 

Here are 5 Agencies with the highest average cost delta:

<div class="row justify-content-md-center">
    <div class="col-lg-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/nyc_construction/Top_5_Agencies_Highest_Average_Budget_Delta.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Notes: A positive cost delta indicates that projects cost more than anticipated. <p>All values are in the thousands so a value of 20,000 = $20,000,000</p>
    
    <p>Source: <a href="https://data.cityofnewyork.us/City-Government/Capital-Project-Detail-Data-Milestones/s7yh-frbm">Capital Project Detail Data - Milestones</a></p>
</div>

Here are the 5 Agencies with the lowest average cost delta:
<div class="row justify-content-md-center">
    <div class="col-lg-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/nyc_construction/Top_5_Agencies_Lowest_Budget_Delta_bar.png" title="5 Lowest Average Budget Deltas" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Notes: A negative cost delta indicates that projects cost less than anticipated. <p>All values are in the thousands so a value of 20,000 = $20,000,000</p>
    
    <p>Source: <a href="https://data.cityofnewyork.us/City-Government/Capital-Project-Detail-Data-Milestones/s7yh-frbm">Capital Project Detail Data - Milestones</a></p>
</div>

### Are Late Projects Over Budget?

Now let's see if projects finished late tend to cost more than anticipated.

<div class="row justify-content-md-center">
    <div class="col-lg-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/nyc_construction/Budget_Status_Late_Projects_heatmap.png" title="Finish and Budget Status Heatmap" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Source: <a href="https://data.cityofnewyork.us/City-Government/Capital-Project-Detail-Data-Milestones/s7yh-frbm">Capital Project Detail Data - Milestones</a>
</div>

It's important to note that projects finished later than planned will be somewhat correlated with being over budget since labor costs will increase.

# Conclusion and Future Analysis

> ##### TIP
>
> Want to explore the data on your own? 
> Checkout my streamlit app <a href="https://explore-nyc-construction-delays.streamlit.app/"> here.</a>
{: .block-tip }

I wasn't able to full answer my question but it does seem that the idea of construction projects over promising and under delivering might have some truth behind it. After analyzing the available data and reconsidering the problem, it seems that public construction projects in New York City are over promising on budgets but for the most part are accurately promising on project timelines.

Future anaylsis of the main question would be possible if the previously [limitations of the data](#data-limitations) were answered. 

Have any questions about my code or suggestions for what to do next? Make sure to comment below!