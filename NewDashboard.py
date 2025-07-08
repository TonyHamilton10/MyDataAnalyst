import pandas as pd
import plotly.express as px
import streamlit as st
import warnings
import os
from PIL import Image

# Title
st.set_page_config(page_title = 'Loans_Dashboard' , page_icon = ":bar_chart:", layout = 'wide')
st.title(":bar_chart: LOANS EDA DASHBOARD")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>" , unsafe_allow_html = True)


# Uploading Data
f1 = st.file_uploader(":file_folder: Upload File" , type = (['txt' , 'csv' , 'xlsx' , 'xls']))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    loan_data = pd.read_csv(filename)
else:
    os.chdir(r"C:\Users\user\Data Analyst")
    loan_data = pd.read_csv('Loan.csv')



loan_data['ApplicationDate'] = pd.to_datetime(loan_data['ApplicationDate'])


col1 ,col2 = st.columns((2))
# Getting the Min and Max Date

startdate = loan_data['ApplicationDate'].min()
enddate = loan_data['ApplicationDate'].max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date' , startdate))

with col2:
    date2 = pd.to_datetime(st.date_input('End Date' , enddate))

loan_data = loan_data[(loan_data['ApplicationDate']>=startdate)&(loan_data['ApplicationDate']<=enddate)]

#Creating Filters
st.sidebar.header("Filters")
# Creating for Education Level
level =st.sidebar.multiselect('Education Level' , loan_data['EducationLevel'].unique())
if not level:
    loan_data1 = loan_data.copy()
else:
    loan_data1 = loan_data[loan_data['EducationLevel'].isin(level)]

#Creating for Employment Status
status = st.sidebar.multiselect('Employment Status' ,loan_data1['EmploymentStatus'].unique() )
if not status:
    loan_data2 = loan_data1.copy()
else:
    loan_data2 = loan_data1[loan_data1['EmploymentStatus'].isin(status)]

# Creating for Marital Status
marital = st.sidebar.multiselect('Marital Status' , loan_data2['MaritalStatus'].unique())
if not marital:
    loan_data3 = loan_data2.copy()
else:
    loan_data3= loan_data2[loan_data2['MaritalStatus'].isin(marital)]

# Creating for Loan Approved

approved = st.sidebar.multiselect('Loan Approved' , loan_data3['LoanApproved'].unique())
if not approved:
    loan_data4 = loan_data3.copy()
else:
    loan_data4 = loan_data3[loan_data3['LoanApproved'].isin(approved)]

# Uniting the Filters
if not level and not status and not marital and not approved:
    filtered_loan_data = loan_data
elif not status and not marital and not approved:
    filtered_loan_data = loan_data[loan_data['EducationLevel'].isin(level)]
elif not level and not marital and not approved:
    filtered_loan_data = loan_data[loan_data['EmploymentStatus'].isin(status)]
elif not level and not status and not approved:
    filtered_loan_data = loan_data[loan_data['MaritalStatus'].isin(marital)]
elif level and status:
    filtered_loan_data =loan_data4[loan_data['EducationLevel'].isin(level)& loan_data4['EmploymentStatus'].isin(status)]
elif level and marital:
    filtered_loan_data = loan_data4[loan_data['EducationLevel'].isin(level)& loan_data4['MaritalStatus'].isin(marital)]
elif level and approved:
    filtered_loan_data = loan_data4[loan_data['EducationLevel'].isin(level)&loan_data4['LoanApproved'].isin(approved)]
elif approved:
    filtered_loan_data = loan_data4[loan_data4['LoanApproved'].isin(approved)]
else:
    filtered_loan_data =loan_data4[loan_data4['EducationLevel'].isin(level)&loan_data4['EmploymentStatus'].isin(status)&
                                   loan_data4['MaritalStatus'].isin(marital)&loan_data4['LoanApproved'].isin(approved)]

   
# Graphs
grp1 = filtered_loan_data.groupby('EducationLevel')['AnnualIncome'].mean().reset_index()
with col1:
    st.subheader('Average Salary With Education Level')
    fig = px.bar(grp1 , y=  'EducationLevel' , x = 'AnnualIncome' , template='gridon' , 
            text = ['${:,.2f}'.format(x) for x in grp1['AnnualIncome']] , height=500)
    st.plotly_chart(fig , use_container_width=True )

with col2:
    st.subheader('Employment Status')
    fig = px.pie(filtered_loan_data , names='EmploymentStatus' , values='NetWorth' , hole = 0.5)
    st.plotly_chart(fig , use_container_width=True)

cl1 ,cl2 = st.columns([.9,.1])

grp1['AnnualIncome'] = grp1['AnnualIncome'].apply(lambda x: f"{x:,.2f}".format(x))

with cl1:
    with st.expander('View Table Data'):
        st.write(grp1)
        csv = grp1.to_csv(index = False).encode('utf-8')
        st.download_button('Download Data' , data=csv ,file_name='EducationLevelSal.csv' , mime='text/csv')
st.divider()

filtered_loan_data['Month'] = filtered_loan_data['ApplicationDate'].dt.month
filtered_loan_data['Year'] = filtered_loan_data['ApplicationDate'].dt.year
filtered_loan_data1 = filtered_loan_data[filtered_loan_data['Year'].between(2018 , 2025)]

grp2 = filtered_loan_data1.groupby(['Month' , 'EducationLevel'])['MonthlyIncome'].mean().reset_index()
grp2['MonthlyIncome'] = grp2['MonthlyIncome'].apply(lambda x: f"{x:,.2f}".format(x))

st.subheader('Monthly Income By Education Level')
fig2 = px.line( grp2,  x ='Month' , y ='MonthlyIncome'  ,   
                color='EducationLevel' , height =500 , width =1000 )
st.plotly_chart(fig2 , use_container_width=True)
with st.expander('View Data Monthly Income By Education Level'):
    st.write(grp2)
    csv =grp2.to_csv().encode('utf-8')
    st.download_button('Download Data' , data =csv , file_name = 'EducationByIncome.csv' , mime ='text/csv')


data1 = px.scatter(filtered_loan_data , x = 'Age' , y = 'MonthlyIncome' , size = 'Age', trendline='ols')
data1['layout'].update(title = 'Relationship Between Age and MonthlyIncome' , 
                       titlefont = dict(size =20) , xaxis = dict(title ='Age' , titlefont = dict(size =19)),
                       yaxis = dict(title = 'MonthlyIncome' , titlefont = dict(size =19)))
st.plotly_chart(data1   ,use_container_width=True)


st.subheader('Hierarchical Distributions')
fig3 = px.treemap(filtered_loan_data , path=['EducationLevel' , 'EmploymentStatus' , 'MaritalStatus' ],
                  values='NetWorth' , hover_data=['NetWorth'] , color = 'LoanApproved') 
fig3.update_layout(width =800 , height = 650)
st.plotly_chart(fig3 ,use_container_width=True)

st.divider()

col3 , col4 = st.columns(2)

with col3:
    st.subheader('Loan Approval')
    pie_data = filtered_loan_data.groupby('LoanApproved')['LoanApproved'].count().reset_index(name ='Count')
    fig4 = px.pie(pie_data, names='LoanApproved' , values ='Count' , template='seaborn', title = 'Count Of Loan Approved' )
    st.plotly_chart(fig4 , use_container_width=True)


with col4:
    st.subheader('Marital Status')
    pie_data1 = filtered_loan_data.groupby('MaritalStatus')['NetWorth'].sum().reset_index()
    fig5 = px.pie(pie_data1 , values='NetWorth' , names='MaritalStatus' , template='gridon'  , title='NetWorth By MaritalStatus')
    st.plotly_chart(fig5 , use_container_width=True)

vw , vw1 = st.columns([.5 , .5])

pie_data['Count'] =pie_data['Count'].apply(lambda x: f"{x:,}".format(x))
pie_data1['NetWorth'] =pie_data1['NetWorth'].apply(lambda x: f"{x:,}".format(x))


with vw:
     with st.expander('View Data'):
        st.write(pie_data)
        csv = pie_data.to_csv().encode('utf-8')
        st.download_button('Download Data' , data =csv , file_name='ApprovedLoans.csv' , mime = "text/csv")

with vw1:
     with st.expander('View Data'):
        st.write(pie_data1)
        csv = pie_data1.to_csv().encode('utf-8')
        st.download_button('Download Data' , data =csv , file_name='NetWorth.csv' , mime = "text/csv")

st.divider()

st.subheader('LinePlot')
grp3 = filtered_loan_data1.groupby('Year')['AnnualIncome'].mean().reset_index()
fig6 = px.line(grp3  ,x = 'Year' , y = 'AnnualIncome' , template='gridon' ,title ='Yearly Average Income')
st.plotly_chart(fig6 , use_container_width=True)

with st.expander('View Data'):
    st.write(filtered_loan_data.iloc[:500,0:20])

gr1 , gr2 = st.columns(2)

with gr1:
    st.subheader('Home Ownership')
    liab = filtered_loan_data.groupby('HomeOwnershipStatus')['TotalLiabilities'].sum().reset_index()
    fig7 = px.bar(liab , x ='HomeOwnershipStatus' , y = 'TotalLiabilities' , title = 'HomeOwnerShipStatus Total Liabilities' ,
                  template='gridon'  , text=[f'${x: ,}'.format(x) for x in liab['TotalLiabilities']])
    st.plotly_chart(fig7 , use_container_width=True)

with gr2:
    st.subheader('Relationship Of Savings and Riskscore')
    fig8 = px.scatter(filtered_loan_data , x = 'SavingsAccountBalance' , y = 'RiskScore' ,  size = 'SavingsAccountBalance' , 
                      title = 'Savings vs RiskScore' ,trendline = 'ols')
    st.plotly_chart(fig8 , use_container_width=True)


l1 ,_ = st.columns([.5 , .5])

liab['TotalLiabilities'] = liab['TotalLiabilities'].apply(lambda x: f'${x:,}')
with l1:
        with st.expander('View Data'):
    
             st.write(liab)
             csv = liab.to_csv().encode('utf-8')
             st.download_button('Download Data' , data =csv , file_name='Liabilities.csv' , mime = "text/csv")

st.divider()

st.subheader('Box Plot')
fig9 = px.box(filtered_loan_data , x ='RiskScore', color='EmploymentStatus'  ,title = 'Box Plot Of Age' , template = 'seaborn')
st.plotly_chart(fig9 , use_container_width=True)





#Down Load Data
csv =loan_data.to_csv(index = False).encode('utf-8')
st.download_button('Download Original Data' , data = csv , file_name = 'Original_Data.csv' , mime = 'text/csv')