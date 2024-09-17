from PIL import Image
import pandas as pd
import numpy as np
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import io
import pybase64 
pd.set_option('display.max_columns', None)

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return pybase64.b64encode(data).decode()
# icon = get_img_as_base64("airbnb_logo.png")

# Setting up page configuration
# icon = Image.open("https://img.etimg.com/thumb/msid-55513295,width-300,height-225,imgsize-16809,resizemode-75/airbnb.jpg")
st.set_page_config(page_title= "Airbnb Data Visualization | By Balamurukan Subramanian",
                   # page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                  )

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://airbnbuser:Fiitjee123@airbnbcl.ys0kj.mongodb.net/?retryWrites=true&w=majority&appName=airbnbCL")
db = client.sample_airbnb
col = db.listingsAndReviews

# Creating option menu in the side bar

with st.sidebar:
    # side_banner = get_img_as_base64("airbnb_banner.jpg")
    st.image("airbnb_banner.jpg")
    st.markdown('Created by *Balamurukan Subramanian*')
    selected = st.radio("Menu", ["Home","Overview","Explore"],index=0)
    # st.markdown("[![Foo](images/in.png)](http://google.com.au/)")
    # st.markdown("[LinkedIn] (https://www.linkedin.com/in/balamurukansu/)")
    # st.markdown("[GitHub] (%s), % https://github.com/balamurukansu/Airbnb-Analysis)")
 
# title and position
st.markdown(f'<h1 style="text-align: center;">Airbnb Analysis</h1>',
            unsafe_allow_html=True)

df = pd.read_csv('airbnb.csv')

# HOME PAGE
if selected == "Home":
    
    # Title Image
    st.image("https://github.com/balamurukansu/Airbnb-Analysis/blob/main/image/airbnb.gif")
    st.markdown(" :blue[Overview] : To analyze Airbnb data with MongoDB Atlas, start by cleaning and preparing the data. Then, develop interactive visualizations and dynamic plots to uncover insights into pricing trends, availability patterns, and location-specific variations.")
    col3,col4=st.columns(2)
    col3.markdown(" :blue[Domain] : Travel Industry, Property Management and Tourism")
    col4.markdown(" :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")

    # OVERVIEW PAGE
if selected == "Overview":
    tab1,tab2 = st.tabs([" *BASE DATA*", "*OBSERVATIONS*"])
    
    # RAW DATA TAB
    with tab1:
        # RAW DATA
        col1,col2 = st.columns(2)
        with col1:
            col1.write(col.find_one())
        # DATAFRAME FORMAT
        with col2:
            col2.table(df.head(10))

    #INSIGHTS
    with tab2:
        # User inputs
        # st.write(sorted(df['Country'].unique()))
        col1,col2,col3,col4 = st.columns(4)
        st.write('# Choose inputs to view insights on map')
        with col1:
            country = st.selectbox('Select Country',sorted(df['Country'].unique()))
        with col2:
            property_type = st.selectbox('Select Property Type',sorted(df['Property_type'].unique()),index=1)
        with col3:
            room_type = st.selectbox('Select Room Type',sorted(df['Room_type'].unique()))
        with col4:
            price = st.slider('Select Price(in $)', min_value=int(df['Price'].min()), max_value=int(df['Price'].max()),
                              value=int(df["Price"].mean()),  
                              step=1)
        # st.write(country)
        # st.write(property_type)
        # st.write(room_type)
        # st.write(price)
        
        filtered_df = df[
            (df['Country'] == country) &
            (df['Room_type'] == room_type) &
            (df['Property_type'] == property_type) &
            (df['Price'] <= price)
        ]
        
        tcol1,tcol2 = st.columns(2)

        with tcol1:
             # Group by 'Property_type' and count the number of listings
             grouped_df = filtered_df.groupby(["Property_type"]).size().reset_index(name="Listings")
    
             # Sort the DataFrame by 'Listings' and take the top 10
             sorted_df = grouped_df.sort_values(by='Listings', ascending=False).head(10)
             fig = px.bar(sorted_df,
                         title='Top 10 Property Types',
                         x='Listings',
                         y='Property_type',
                         orientation='h',
                         color='Property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
             st.plotly_chart(fig,use_container_width=True)

             # Group by 'Property_type' and count the number of listings
             grouped_df = filtered_df.groupby(["Host_name"]).size().reset_index(name="Listings")
             
             # Sort the DataFrame by 'Listings' and take the top 10
             sorted_df = grouped_df.sort_values(by='Listings', ascending=False).head(10)

             fig = px.bar(sorted_df,
                        title='Top 10 Hosts with Highest number of Listings',
                        x='Listings',
                        y='Host_name',
                        orientation='h',
                        color='Host_name',
                        color_continuous_scale=px.colors.sequential.Agsunset)
             fig.update_layout(showlegend=False)
             st.plotly_chart(fig,use_container_width=True)         
        
        with tcol2:
             # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
             # Group by 'Property_type' and count the number of listings
             grouped_df = filtered_df.groupby(["Room_type"]).size().reset_index(name="counts")
             
             # Sort the DataFrame by 'Listings' and take the top 10
             sorted_df = grouped_df.sort_values(by='counts', ascending=False).head(10)
            
             fig = px.pie(sorted_df,
                         title='Total Listings in each Room_types',
                         names='Room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                        )
             fig.update_traces(textposition='outside', textinfo='value+label')
             st.plotly_chart(fig,use_container_width=True)

             # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
             # Group by 'Property_type' and count the number of listings
             grouped_df = filtered_df.groupby(['Country'], as_index=False)['Name'].count()

             country_df = grouped_df.rename(columns={'Name': 'Total_Listings'})

             fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                               )
             st.plotly_chart(fig,use_container_width=True)

        # EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Lets delve deep into Airbnb data")
    # User inputs
    # st.write(sorted(df['Country'].unique()))
    st.write('# Choose inputs to view insights on map')
    col1,col2,col3,col4 = st.columns(4)
    
    with col1:
        country = st.selectbox('Select Country',sorted(df['Country'].unique()))
    with col2:
        property_type = st.selectbox('Select Property Type',sorted(df['Property_type'].unique()),index=1)
    with col3:
        room_type = st.selectbox('Select Room Type',sorted(df['Room_type'].unique()))
    with col4:
        price = st.slider('Select Price(in $)', min_value=int(df['Price'].min()), max_value=int(df['Price'].max()),
                            value=int(df["Price"].mean()),  
                            step=1)
        
    filtered_df = df[
            (df['Country'] == country) &
            (df['Room_type'] == room_type) &
            (df['Property_type'] == property_type) &
            (df['Price'] <= price)
        ]

    st.markdown('# Price Analysis')
    
    col1,col2 = st.columns(2,gap='medium')

    with col1:
        # AVG PRICE BY ROOM TYPE BARCHART
        price_df = filtered_df.groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=price_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price per Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=filtered_df,
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    with col2:        
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = filtered_df.groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")
        
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = filtered_df.groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)
