import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

# --------- Load Data ---------
projectCosts = pd.read_csv('data/projectCosts.csv')
deltasHeatMapDF = pd.read_csv('data/deltasHeatMapDF.csv',index_col=0)
costStatusHeatMapDF = pd.read_csv('data/costStatusHeatMapDF.csv',index_col=0)

boroNames = projectCosts.boro.unique().tolist()

##############################################################################
#                        --------- Sidebar ---------                         #
##############################################################################
st.set_page_config(page_title="Explore NYC Construction Delays and Costs")

st.sidebar.header("About",divider="red")

st.sidebar.markdown("""
                This dashboard is part of my final project for my STAT 386 class at BYU.
                The goal of the project was to see look at construction projects to see if 
                project proposals over promise and under deliver (i.e. projects were finished 
                later than planned and went over budget). The data used in this project was 
                collected from the [NYC Open Data Portal](https://data.cityofnewyork.us/).
                """)


st.sidebar.markdown("---")

st.sidebar.header("Helpful Links",divider="red")
st.sidebar.markdown(
            """
        - [Repo for this Project](https://github.com/aoustrich/NYC_ConstructionDelays)
        - [Data Collection and Cleaning](https://aoustrich.github.io/blog/2023/Construction-Delays-Part-1/)
        - [EDA and Conclusions](https://aoustrich.github.io/blog/2023/Construction-Delays-Part-2/)
        """
    )

st.sidebar.markdown("---")
st.sidebar.header("About Me",divider="red")
st.sidebar.info("Check out my [website](https://aoustrich.github.io/) to learn more about me and see other projects!", icon="ℹ️")


##############################################################################
#                        --------- Part 1 ---------                          #
##############################################################################

# st.markdown("## Compare Project Budget and Timeline Statuses Across Multiple Boroughs")
st.header("Compare Project Budget and Timeline Statuses Across Multiple Boroughs",divider="green")

filtered_boros = st.multiselect('What Boroughs do you want to see?',boroNames,
                                 default=boroNames)
df_filtered_boros = projectCosts[projectCosts['boro'].isin(filtered_boros)]

def createBorosBudgetStatusBar():
    fig = px.bar(df_filtered_boros,
             x='boro',
             color='costStatus',
             barmode='group',
             category_orders={'costStatus': ["Under Budget","On Target","Over Budget"]},
             title='Budget Status Across Boroughs'
            )
    fig.update_layout(
        xaxis=dict(title='Borough'),
        yaxis=dict(title='Count'),
        legend_title='Budget Status',
        height=500,
        width=500
        )
    return fig

def createBorosStartStatusBar():
    fig = px.bar(df_filtered_boros,
             x='boro',
             color='startStatus',
             barmode='group',
             category_orders={'startStatus': ["Early","On Time","Late"]},
             title='Start Status Across Boroughs'
            )
    fig.update_layout(
        xaxis=dict(title='Borough'),
        yaxis=dict(title='Count'),
        legend_title='Start Status',
        height=500,
        width=500
        )
    return fig

def createBorosEndStatusBar():
    fig = px.bar(df_filtered_boros,
             x='boro',
             color='endStatus',
             barmode='group',
             category_orders={'endStatus': ["Early","On Time","Late"]},
             title='End Status Across Boroughs'
            )
    fig.update_layout(
        xaxis=dict(title='Borough'),
        yaxis=dict(title='Count'),
        legend_title='End Status',
        height=500,
        width=500
        )
    return fig


plot1 = createBorosBudgetStatusBar()
plot2 = createBorosStartStatusBar()
plot2 = createBorosEndStatusBar()

#  if i'm using streamlit expanders how can I make it so when one is expanded all others collapse? 

st.write("Click on the expanders below to see the different plots.")

with st.expander("Project Budget Status Across Boroughs"):
    st.plotly_chart(plot1)

with st.expander("Project Start Status Across Boroughs"):
    st.plotly_chart(plot2)

with st.expander("Project End Status Across Boroughs"):
    st.plotly_chart(plot2)


##############################################################################
#                        --------- Part 2 ---------                          #
##############################################################################

st.header("Compare Project Stage Time Deltas for 2 Boroughs",divider="green")

stageCol1, stageCol2, stageCol3 = st.columns(3, gap="large")

with stageCol1:
    stageBoro1 = st.selectbox('Pick the 1st Borough',
                         options = boroNames,
                         index=None)

with stageCol2:
    secondBoroOptions = projectCosts[projectCosts['boro']!= stageBoro1]['boro'].unique().tolist()
    stageBoro2 = st.selectbox('Pick the 2nd Borough',
                        #  options = projectCosts[projectCosts['boro']!= stageBoro1]['boro'].unique().tolist())
                        options = secondBoroOptions,
                        index = None)
with stageCol3:
    projectStage_xAxis_Selector = st.selectbox('Pick a Project Stage to Visualize',
                                               options = ["Start","End"],
                                               index = None)

borosToCompare = [stageBoro1, stageBoro2]
projectStage_xAxis = ""
projectStage_xAxis_Filter = ""
projectStageTitle = ""

if stageBoro1 is not None and stageBoro2 is not None and projectStage_xAxis_Selector is not None:

    if projectStage_xAxis_Selector == 'Start':
        projectStage_xAxis = 'starting_delta'
        projectStage_xAxis_Filter = 'startStatus'
        projectStageTitle = 'Starting Delta'
    else:
        projectStage_xAxis = 'ending_delta'
        projectStage_xAxis_Filter = 'endStatus'
        projectStageTitle = 'Ending Delta'


    projectStageDF = projectCosts[projectCosts['boro'].isin(borosToCompare)]
    projectStageDF = projectStageDF[projectStageDF[projectStage_xAxis_Filter] != 'On Time']

    def generateBoroComparisonHistogram():
        fig = px.histogram(projectStageDF, 
                    x=projectStage_xAxis, 
                    color='boro', 
                    barmode='stack', 
                    nbins=200, 
                    title=f"Comparing {stageBoro1} & {stageBoro2} {projectStageTitle}s")
        fig.update_layout(xaxis=dict(range=[-250, 250]),
                        legend_title='Borough',
                        height=500,
                        width=500,
                        xaxis_title= projectStageTitle,
                        yaxis_title='Count'
                    )
        return fig


    st.plotly_chart(generateBoroComparisonHistogram())

else:
    st.write("Please select two boroughs and a project stage to compare.")

##############################################################################
#                        --------- Part 3 ---------                          #
##############################################################################

st.header("Compare Budget Status and Project Stage Status for 1 Borough",divider="green")

hMapCol1, hMapCol2 = st.columns(2, gap="large")

with hMapCol1:
    hMapBoro = st.selectbox('Pick a Borough',
                         options = boroNames,
                         index=None)

with hMapCol2:
    hMap_yAxis_Selector = st.selectbox('Pick a Project Stage for the Heatmap',
                                               options = ["Start","End"],
                                               index = None)
    


if hMapBoro is not None and hMap_yAxis_Selector is not None:
    if hMap_yAxis_Selector == 'Start':
        hMap_yAxis = 'startStatus'
        hMapTitle = 'Start Status'
    else:
        hMap_yAxis = 'endStatus'
        hMapTitle = 'End Status'

    budgetStageHMapDF = projectCosts[projectCosts['boro']==hMapBoro]\
                            .groupby(['costStatus', hMap_yAxis]).size().unstack()\
                            .reindex(columns=["Late", "On Time", "Early"],
                                      index=["Under Budget", "On Target", "Over Budget"]).T

    def generateBoroHeatMap():
        fig = px.imshow(deltasHeatMapDF,
                        labels=dict(x="Budget Status", y=hMapTitle), 
                        x=budgetStageHMapDF.columns,
                        y=budgetStageHMapDF.index,
                        color_continuous_scale="deep",
                        title=f"Project {hMapTitle} and Budget Heatmap for {hMapBoro}",
                        text_auto=True
                        )
        
        if hMapTitle == 'Start Status':
            fig.update_traces(hovertemplate="Budget Status: %{y}<br>Start Status: %{x}<br>Count: %{z}")
        else:
            fig.update_traces(hovertemplate="Budget Status: %{y}<br>End Status: %{x}<br>Count: %{z}")
        
        fig.update_layout(
                        xaxis_title='Budget Status',
                        yaxis_title=hMapTitle,
                        height=500,
                        width=500,
                        coloraxis_showscale=False
                    )
        return fig
    
    st.plotly_chart(generateBoroHeatMap())

else:
    st.write("Please select a Borough and a Project Stage.")
# deltasHeatMapDF = projectDeltas.groupby(['Start Status', 'End Status']).size().unstack().fillna(0)
# deltasHeatMapDF = deltasHeatMapDF.reindex(columns=["Early", "On Time", "Late"], index=["Late", "On Time", "Early"]).T
