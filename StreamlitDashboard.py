import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import datetime
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
import streamlit as st

# Reading Data
mydata = pd.read_excel("C:/Users/user/Desktop/Machine Learning Full/data/archive (3)/SuperStore Sales DataSet.xlsx")
mydata['TotalSales'] = mydata['Sales']*mydata['Quantity']

#Styling 
st.set_page_config(page_title='Cut Sales Interactive Dashboard' , layout = 'wide')
st.markdown('<style>div.block-container{padding_top:1rem;}</style>' , unsafe_allow_html = True)
image = Image.open('cut.jpeg')
image2 = Image.open('hamilton.jpg')

col1 , col2 = st.columns([0.1 , 0.9])
with col1:
    st.image(image ,width = 100)

html_title = """
      <style>
      .title-test {
      font-weigth:bold;
      padding:5px;
      border-radius:6px}
      </style>
      <center><h1 class="title-test">CUT Retail Sales Dashboard</h1></center>"""
with col2:
    st.markdown(html_title , unsafe_allow_html = True)

col3 , col4 , col5 = st.columns([.1,.45,.45])
# Date Last Updated
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last Updated by: \n {box_date}")

with col4:
    fig = px.bar(mydata , x ='Segment' , y ='TotalSales' , title = 'Total Sale Per Segment' , labels={'TotalSales':'Total Sales {$}'} ,
                   template="gridon" , height=500 ) 
    st.plotly_chart(fig , use_container_width=True)

# Adding a drop down button to show the data in the Table
ten, view1 , dwn1, view2, dwn2 = st.columns([0.15 ,0.2 , 0.2 ,0.2 ,0.2])
with ten:
    st.image(image2 ,width = 500)

with view1:
    expander = st.expander('Segment Sale')
    data = mydata.groupby('Segment')['TotalSales'].sum()
    expander.write(data)
with dwn1:
    st.download_button('Get Sample Date' , data = data.to_csv().encode("utf-8") , 
                       file_name='SegmentData.csv' , mime="text/csv")

mydata['Ship Date'] = pd.to_datetime(mydata['Ship Date'])
mydata['Month'] = mydata['Ship Date'].dt.month
mydata['Year'] = mydata['Ship Date'].dt.year
mydata['Mon_Year'] = mydata['Ship Date'].dt.strftime("%b-%y")

result = mydata.groupby('Year')['TotalSales'].sum().reset_index()
result2 = mydata.groupby('Mon_Year')['TotalSales'].mean().reset_index()
# Plots
with col5:
    fig1 = px.line(result2 , x = 'Mon_Year' , y = 'TotalSales' , title = 'Average Total Sales' , template='gridon' , height=500)
    st.plotly_chart(fig1 , use_container_width=True)

with view2:
    expander =st.expander('Monthly Sales')
    data = result2
    expander.write(data)
with dwn2:
    st.download_button("Get Data" , data = result2.to_csv().encode("utf-8") , 
                       file_name="MonthlySale.csv" , mime="text/csv")
st.divider()

result1 = mydata.groupby('State')[['TotalSales' , 'Quantity']].sum().reset_index()


fig3 = go.Figure()

fig3.add_trace(go.Bar(x = result1['State'] , y = result1['TotalSales'] , name='Total Sale'))
fig3.add_trace(go.Scatter(x = result1['State'] , y = result1['Quantity'] , mode='lines' , 
                          name='Quantity Sold' , yaxis='y2'))
fig3.update_layout(
    title = 'Total Sale and Quantiy Sold by States' ,
    xaxis = dict(title = 'State') ,
    yaxis = dict(title = 'Total Sale' , showgrid = False),
    yaxis2 = dict(title = 'Quantity Sold' , overlaying = 'y' , side = 'right') , 
    template = 'gridon' ,
    legend = dict(x = 1 , y = 1.1)
)

_,col6 = st.columns([.1 ,  1])
with col6:
    st.plotly_chart(fig3 , use_container_width=True)

_,view3 , dwn3 = st.columns([.5 , .45 , .45])
with view3:
    expander = st.expander('View Data Of Quantity Sold')
    expander.write(result1)

with dwn3:
    st.download_button('Get Data'  , data = result1.to_csv().encode("utf_8") , file_name="Sales_by_Quantity.csv" , mime="text/csv")

st.divider()

_, col7 = st.columns([.1 ,1])
treemap = mydata.groupby(['Region' , 'City'])['TotalSales'].sum().reset_index()

#def format_value(value):
#    if value>=0:
#        return '{:.2f} '.format(value/1000)

#treemap['TotalSales(USD)'] = treemap['TotalSales'].apply(format_value)
fig4 = px.treemap(treemap , path=['Region' , 'City'] , values='TotalSales'  , hover_data=['TotalSales'] , 
                  color='City' ,  height=700 , width=600)
fig4.update_traces(textinfo = "label+value")
with col7:
    st.subheader(":point_right: Total Sales By Region and City")
    st.plotly_chart(fig4 ,use_container_width=True)

_, view4 , dwn4 =st.columns([.5,.45,.45])
with view4:
    result4 = mydata.groupby(['Region' , 'City'])['TotalSales'].sum().reset_index()
    expander = st.expander("View Data Of Total Sale by Region and City")
    expander.write(result4)
with dwn4:
    st.download_button("Get Data" , data = result4.to_csv().encode('utf-8') , 
                       file_name="Sales_by_Region.csv" , mime  = "text/csv")
    
_ , view5 , dwn5 = st.columns([.5 , .45 , .45])
with view5:
    expander = st.expander('View Raw Data')
    expander.write(mydata)
with dwn5:
    st.download_button('Get Raw Data' , data= mydata.to_csv().encode('utf-8') , 
                       file_name='SalesRawData.csv' , mime='text/csv')
    
st.divider()