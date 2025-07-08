import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Page Name
st.set_page_config(page_title ='Loan Dashboard' , layout ='wide')

#Import Data 
loan_data = pd.read_csv("C:/Users/user/Desktop/New folder (2)/Loan.csv")

# Text
st.header('Loan Data Analysis')



# Creating Filters
st.sidebar.title('Filters')
Loans_Name = st.sidebar.multiselect('Education Level', loan_data['EducationLevel'].unique() , default=loan_data['EducationLevel'].unique())
Loans = st.sidebar.multiselect('Employment Status' , loan_data['EmploymentStatus'].unique() , default=loan_data['EmploymentStatus'].unique() )
Loans_status = st.sidebar.multiselect('Marital Status' , loan_data['MaritalStatus'].unique() , default=loan_data['MaritalStatus'].unique() )

#Buttons
st.button('Loan Application')


# Displaying Metrics
col1, col2 , col3 , col4 = st.columns(4)
col1.metric('Total Assets' , f"${loan_data['TotalAssets'].sum():,}")
col2.metric('Total Liabilities' , f"${loan_data['TotalLiabilities'].sum(): ,}")
col3.metric('Average Annual Income' , f"{loan_data['AnnualIncome'].mean(): .2f}")
col4.metric('Total Data' , f"{loan_data['EmploymentStatus'].count(): ,}")

col1 , col2,col3 = st.columns(3)

with col1:
    loan = loan_data.groupby('EmploymentStatus')['AnnualIncome'].mean().reset_index()
    fig_bar = px.bar(loan , x = 'EmploymentStatus' , y ='AnnualIncome' , title='Average Income by Employment Status')
    st.plotly_chart(fig_bar , use_container_width=True)

with col2:
    cause_count = loan_data.groupby('MaritalStatus')['MaritalStatus'].count().reset_index(name = 'Count')
    fig_bar1 = px.bar(cause_count , x ='MaritalStatus' , y ='Count' , title = 'Count of Marital Status' )
    st.plotly_chart(fig_bar1 , use_container_width=True)

with col3:
    accept = loan_data.groupby('LoanApproved')['LoanApproved'].count().reset_index(name = 'Count')
    fig_pie = px.pie(accept , names ='LoanApproved' , values ='Count' , title = 'Loan Aproved' )
    st.plotly_chart(fig_pie , use_container_width=True)

col4 , col5 , col6 = st.columns(3)

with col4:
    loan_data['ApplicationDate'] = pd.to_datetime(loan_data['ApplicationDate'])
    loan_data['Year'] = loan_data['ApplicationDate'].dt.year
    loan_data20 = loan_data[loan_data['Year'].between(2020 , 2024)]
    fig_net = px.line(loan_data20 , x = 'Year',  y = 'MonthlyIncome' , title = 'Monthly Income')
    st.plotly_chart(fig_net , use_container_width=True)

with col5:
    fig_hist = px.histogram(loan_data , x = 'RiskScore'  , title = 'Distribution of Riskscore')
    st.plotly_chart(fig_hist , use_container_width=True)

with col6:
    fig_scat = px.scatter(loan_data  , x = 'Age' , y = 'Experience' , trendline='ols' , title = 'Age vs Experience')
    st.plotly_chart(fig_scat , use_container_width=True)


# Displaying Data
st.table(loan)


