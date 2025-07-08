
# Importing Pacakges
import pandas as pd
import plotly.express as px
import streamlit as st
import os
import warnings
from PIL import Image

# Set Initial Page Configuration

st.set_page_config(page_title ="Health Insurance Dashboard" ,  page_icon=':bar_chart:' , layout='wide')
st.title(":bar_chart: HEALTH INSURANCE DASHBOARD")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>" , unsafe_allow_html=True)

# Setting button to Import Data

data = st.file_uploader(":file_folder: Upload file" , type = (['txt' , 'csv' , 'xlsx' , 'xls']))
if data is not None:
    filename = data.name
    st.write(filename)
    insure_data = pd.read_csv(filename)
else:
    os.chdir(r"C:\Users\user\Data Analyst")
    insure_data = pd.read_csv('Enhanced_health_insurance_claims.csv')

# Converting date to datetime object

insure_data['ClaimDate'] = pd.to_datetime(insure_data['ClaimDate'])

# Create Date filters

col1 , col2 = st.columns((2))

startdate = insure_data['ClaimDate'].min()
enddate = insure_data['ClaimDate'].max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date' , startdate))

with col2:
    date2 = pd.to_datetime(st.date_input('Start Date' , enddate))
    
insure_data = insure_data[(insure_data['ClaimDate']>=startdate )& (insure_data['ClaimDate']<=enddate )]

st.divider()


# Creating Filters

st.sidebar.header('FILTERS')
# Patient Gender
gender =st.sidebar.multiselect('PatientGender' , insure_data['PatientGender'].unique())
if not gender:
    insure_data1 = insure_data.copy()
else:
    insure_data1 = insure_data[insure_data['PatientGender'].isin(gender)]

# Claim Status
status = st.sidebar.multiselect('Claim Status' ,insure_data1['ClaimStatus'].unique() )
if not status:
    insure_data2 = insure_data1.copy()
else:
    insure_data2 = insure_data1[insure_data1['ClaimStatus'].isin(status)]

# Patient Marital Status
marital = st.sidebar.multiselect('Patient Marital Status' , insure_data2['PatientMaritalStatus'].unique())
if not marital:
    insure_data3 = insure_data2.copy()
else:
    insure_data3= insure_data2[insure_data2['PatientMaritalStatus'].isin(marital)]

# Patient Employment Status
employ = st.sidebar.multiselect('Patient Employment Status' , insure_data3['PatientEmploymentStatus'].unique())
if not employ:
    insure_data4 = insure_data3.copy()
else:
    insure_data4 = insure_data3[insure_data3['PatientEmploymentStatus'].isin(employ)]

# Create A Link in the Filter

if not gender  and not status and not marital and not employ:
    filtered_insure_data = insure_data
elif not status and not marital and not employ:
    filtered_insure_data = insure_data[insure_data['PatientGender'].isin(gender )]
elif not gender  and not marital and not employ:
    filtered_insure_data = insure_data[insure_data['ClaimStatus'].isin(status)]
elif not gender  and not status and not employ:
    filtered_insure_data = insure_data[insure_data['PatientMaritalStatus'].isin(marital)]
elif gender  and status:
    filtered_insure_data =insure_data4[insure_data['PatientGender'].isin(gender )& insure_data4['ClaimStatus'].isin(status)]
elif gender  and marital:
    filtered_insure_data = insure_data4[insure_data['PatientGender'].isin(gender )& insure_data4['PatientMaritalStatus'].isin(marital)]
elif gender  and employ:
    filtered_insure_data = insure_data4[insure_data['PatientGender'].isin(gender )&insure_data4['PatientEmploymentStatus'].isin(employ)]
elif employ:
    filtered_insure_data = insure_data4[insure_data4['PatientEmploymentStatus'].isin(employ)]
else:
    filtered_insure_data =insure_data4[insure_data4['PatientGender'].isin(gender )&insure_data4['ClaimStatus'].isin(status)&
                                   insure_data4['PatientMaritalStatus'].isin(marital)&insure_data4['PatientEmploymentStatus'].isin(employ)]
    

# Download but and preview of Data
with  st.expander('View Data'):
      st.write(insure_data)
      csv = filtered_insure_data.to_csv().encode('utf-8')
      st.download_button('Download Data' , data = csv, file_name='Insurance_Data.csv' , mime='txt/csv')
        
   
st.divider()


# Displaying Metrics
c1, c2 , c3 = st.columns(3)
c1.metric('Total Claims' , f"${insure_data['ClaimAmount'].sum():,.2f}")
c2.metric('Average Patient Income' , f"${insure_data['PatientIncome'].mean(): ,.2f}")
c3.metric('Total Number Of Claims' , f"{insure_data['ClaimID'].nunique(): ,}")



c1 , c2 = st.columns(2)
# Pie Charts
with c1:
    st.subheader("Patient Gender")
    grp = filtered_insure_data.groupby('PatientGender')['PatientGender'].count().reset_index(name = 'Count')
    fig = px.pie(grp , names='PatientGender' ,values='Count' ,title = 'Count Of Patient Gender' , 
                 template = 'gridon' )
    st.plotly_chart(fig , use_container_width=True)

with c2:
    st.subheader('Claim Status')
    grp1 = filtered_insure_data.groupby('ClaimStatus')['ClaimStatus'].count().reset_index(name = 'Count')
    fig2 = px.pie(grp1 , names='ClaimStatus' , values='Count' , title='Count Of Claim Status' , 
                  template='gridon')
    st.plotly_chart(fig2 , use_container_width=True)

# Creating View Data Dropdowns and Download Buttons
cl1 , cl2 = st.columns((2))
with cl1:
    with st.expander('Patient Gender'):
        grp['Count'] = grp['Count'].apply(lambda x: f'{x: ,}')
        st.write(grp)
        csv = grp.to_csv(index = False).encode('utf-8')
        st.download_button('View Gender Data' , data = csv , file_name='PatientGender.csv' , mime='txt/csv')
with cl2:
    with st.expander('Claim Status'):
        grp1['Count'] = grp1['Count'].apply(lambda x: f'{x: ,}')
        st.write(grp1)
        csv = grp1.to_csv(index = False).encode('utf-8')
        st.download_button('View Claim Status Data' , data = csv , file_name='ClaimStatus.csv' , mime='txt/csv')
st.divider()

col3 , col4 = st.columns(2)

with col3:
    st.header('Claim Status Amount')
    grp2 = filtered_insure_data.groupby('ClaimStatus')['ClaimAmount'].sum().reset_index()
    fig3 = px.bar(grp2 , x = 'ClaimStatus' , y = 'ClaimAmount' , title = 'Total Claim Ammount' , template='gridon',
                  text = [f'${x:,}'.format(x) for x in grp2['ClaimAmount'] ])
    st.plotly_chart(fig3 , use_container_width=True)

with col4:
    st.header('Claims Per Specialist')
    grp3 = filtered_insure_data.groupby('ProviderSpecialty')['ClaimAmount'].sum().reset_index()
    fig4 = px.bar(grp3 , y = 'ProviderSpecialty' , x = 'ClaimAmount' , title = 'Claims Per Specialist' ,
                  text =[f'${x :,.2f}'.format(x) for x in grp3['ClaimAmount']] , template='gridon' )
    st.plotly_chart(fig4 , use_container_width=True)

cl3, cl4 = st.columns((2))

with cl3:
     with st.expander('Claim Amount'):
        grp2['ClaimAmount'] =  grp2['ClaimAmount'].apply(lambda x: f"{x: ,.2f}")
        st.write(grp2)
        csv = grp2.to_csv(index = False).encode('utf-8')
        st.download_button('Download' , data =csv , file_name='ClaimAmmount.csv' , mime='txt/csv')

with cl4:
     with st.expander('Specialist Amount'):
        grp3['ClaimAmount'] =  grp3['ClaimAmount'].apply(lambda x: f"{x: ,.2f}")
        st.write(grp3)
        csv = grp3.to_csv(index = False).encode('utf-8')
        st.download_button('Download' , data =csv , file_name='Specialist.csv' , mime='txt/csv')
st.divider()

# Time Series Data

filtered_insure_data['ClaimDate'] = pd.to_datetime(filtered_insure_data['ClaimDate'])
filtered_insure_data['Month_year'] = filtered_insure_data['ClaimDate'].dt.strftime('%b-%y')
filtered_insure_data['Year'] = filtered_insure_data['ClaimDate'].dt.year
filtered_insure_data['Quarter'] = filtered_insure_data['ClaimDate'].dt.quarter

grp4 = filtered_insure_data.groupby('Month_year')[['ClaimAmount' , 'PatientIncome']].sum().reset_index()

st.header('Time Series Analysis')
fig5 = px.line(grp4 ,x ='Month_year'   , y = 'ClaimAmount' , title ='Monthly Claims' , height=400 )
st.plotly_chart(fig5 , use_container_width=True)


fig6 = px.line(grp4 ,x ='Month_year'   , y = 'PatientIncome' , title ='Patience Income' , height=400 )
st.plotly_chart(fig6 , use_container_width=True)


grp5 = filtered_insure_data.groupby('Quarter')[['PatientIncome','ClaimAmount']].sum().reset_index()
fig7 = px.line(grp5 ,x ='Quarter'   , y = 'PatientIncome' , title ='Patience Income' , height=400 )
st.plotly_chart(fig7 , use_container_width=True)

cl5 , cl6  = st.columns((2))

with cl5:
    with st.expander('Claim and Income Data'):
        grp4['ClaimAmount' ] = grp4['ClaimAmount' ].apply(lambda x: f'{x: ,.2f}')
        grp4['PatientIncome' ] = grp4['PatientIncome' ].apply(lambda x: f'{x: ,.2f}')
        st.write(grp4)
        csv = grp4.to_csv(index = False).encode('utf-8')
        st.download_button('Download' , data = csv , file_name='Claim_Income.csv' , mime = 'txt/csv')

with cl6:
    with st.expander('Quarter'):
        grp5['ClaimAmount' ] =grp5['ClaimAmount' ].apply(lambda x: f'{x: ,.2f}')
        grp5['PatientIncome' ] =grp5['PatientIncome' ].apply(lambda x: f'{x: ,.2f}')
        st.write(grp5)
        csv = grp5.to_csv(index = False).encode('utf-8')
        st.download_button('Download' , data = csv , file_name='Quarter.csv' , mime = 'txt/csv')


st.subheader('Relationship Analyst')
fig8 = px.scatter(insure_data , x = 'PatientAge' , y = 'ClaimAmount' , title='Age vs Income' , template='gridon' , 
                  trendline ='ols')
st.plotly_chart(fig8 , use_container_width=True)



column  ,column1 = st.columns(2)
grp6 = filtered_insure_data.groupby('ClaimType')['ClaimAmount'].sum().reset_index()
new =grp6.copy()
new['ClaimAmount'] = new['ClaimAmount'].apply(lambda x: f"${x: ,}").copy()

# Creating a Table
import plotly.figure_factory as ff
st.subheader(":point_right: Claim Amount")
   
tab = ff.create_table(new , colorscale='Blues')
st.plotly_chart(tab , use_container_width=True)


st.divider()

column , column1 = st.columns(2)

with column:
    fig9 =px.bar(grp6 , x = 'ClaimType' , y = 'ClaimAmount' , title = 'Claim Type Amount' ,template='gridon',
                 text =[f"${x:,.2f}".format(x) for x in grp6['ClaimAmount']])
    st.plotly_chart(fig9 , use_container_width=True)

grp7 = filtered_insure_data.groupby('ClaimSubmissionMethod')['ClaimSubmissionMethod'].count().reset_index(name ='Count')

with column1:
    fig10 = px.pie(grp7 , names='ClaimSubmissionMethod' , values='Count' , title='Most Used Submission Method',
                   template='gridon' , hole=.4)
    st.plotly_chart(fig10 , use_container_width=True)


