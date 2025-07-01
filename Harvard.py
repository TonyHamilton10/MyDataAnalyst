import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit_jupyter import StreamlitPatcher,tqdm
import warnings
warnings.filterwarnings("ignore" , category=RuntimeWarning)


st.set_page_config(page_title ='Actuarial Dashboard' , layout ='wide')

#Importing Data
actuary_data = pd.read_excel("C:/Users/user/Desktop/New folder (2)/Actuarial_Task_2.xlsx")

# Creating Filters
st.sidebar.title('Filters')
claim_type = st.sidebar.multiselect('Select Claim', actuary_data['Type_of_Claim'].unique() , default=actuary_data['Type_of_Claim'].unique())
Cause_of_Loss = st.sidebar.multiselect('Cause Of Loss' , actuary_data['Cause_of_Loss'].unique() , default=actuary_data['Cause_of_Loss'].unique() )

# Displaying Metrics
col1, col2 , col3 = st.columns(3)
col1.metric('Total Claims' , f"${actuary_data['Claim_Incurred_($)'].sum():,}")
col2.metric('Gross Claims Amount' , f"${actuary_data['Gross_claim_amount'].sum(): ,}")
col3.metric('Total Number Of Claims' , f"{actuary_data['Type_of_Claim'].count(): ,}")

# Charts

col1 , col2 = st.columns(2)

with col1:
    time_data = actuary_data.groupby('Year')['Claim_Incurred_($)'].mean().reset_index()
    fig_line = px.line(time_data , x = 'Year' , y ='Claim_Incurred_($)' , title='Claims Incurred')
    st.plotly_chart(fig_line , use_container_width=True)

with col2:
    cause_count = actuary_data.groupby('Cause_of_Loss')['Net_inflation_adjusted_claim'].sum().reset_index(name='Total')
    fig_bar = px.bar(cause_count , x ='Cause_of_Loss' , y ='Total' , title = 'Total Causes Of Loss' )
    st.plotly_chart(fig_bar , use_container_width=True)