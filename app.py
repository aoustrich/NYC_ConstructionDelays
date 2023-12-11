import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

# --------- Load Data ---------
projectCosts = pd.read_csv('data/projectCosts.csv')
deltasHeatMapDF = pd.read_csv('data/deltasHeatMapDF.csv',index_col=0)
costStatusHeatMapDF = pd.read_csv('data/costStatusHeatMapDF.csv',index_col=0)

# create 
boroNames = projectCosts.boro.unique().tolist()

# --------- Dashboard Layout ---------
st.title("Exploring NYC Construction Delays")

""" show project deltas heatmap plot?"""

    # ---- Select Borough ----
    
filtered_boros = st.multiselect('Select Boroughs',projectCosts['boro'].unique(), default=projectCosts['boro'].unique())
df_filtered_boros = projectCosts[projectCosts['boro'].isin(filtered_boros)]

fig1 = px.bar(df_filtered_boros,
             x='boro',
             color='costStatus',
             barmode='group',
             category_orders={'costStatus': ["Under Budget","On Target","Over Budget"]},
             title='Count of Cost Status Across Boroughs'
            )

fig1.update_layout(
    xaxis=dict(title='Borough'),
    yaxis=dict(title='Count'),
    legend_title='Cost Status'
)

st.plotly_chart(fig1)
    # ---- Select Project Type ----

st.markdown("---")

fig2 = px.bar(df_filtered_boros, x=filtered_boros, color='costStatus', barmode='group')
st.plotly_chart(fig2)


# # Allow the user to select the schools to display
# schools = st.multiselect('Select schools to display', df['School'].unique(), default=list(df['School'].unique())) 
# df_barplot = df[df['School'].isin(schools)]
# # Allow the user to select the years to display
# #years = st.multiselect('Select years to display', df['Year'].unique(), default=list(df['Year'].unique()))

# # Plot the data using the selected X axis on a bar plot
# fig = px.bar(df_barplot, x=x_axis, y='School', color='Year', orientation='h', barmode='group')
# st.plotly_chart(fig)
