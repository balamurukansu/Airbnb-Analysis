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
pd.set_option('display.max_columns', None)

# Setting up page configuration
icon = Image.open("image\\airbnb_logo.png")
st.set_page_config(page_title= "Airbnb Data Visualization | By ",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by **!
                                        Data has been gathered from mongodb atlas"""}
                  )

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://airbnbuser:Fiitjee123@airbnbcl.ys0kj.mongodb.net/?retryWrites=true&w=majority&appName=airbnbCL")
db = client.sample_airbnb
col = db.listingsAndReviews
# title and position
st.markdown(f'<h1 style="text-align: center;">Airbnb Analysis</h1>',
            unsafe_allow_html=True)

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("", ["Home","Overview","Explore"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0, styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", 
                                                                 "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                          )


df = pd.read_csv('airbnb.csv')

# HOME PAGE
if selected == "Home":
    # Title Image
    st.image("image\\airbnb.gif")
    st.markdown(" :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    col1,col2=st.columns(2)
    col1.markdown(" :blue[Domain] : Travel Industry, Property Management and Tourism")
    col2.markdown(" :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    
    st.markdown("   ")
    st.markdown("   ")
    

    # OVERVIEW PAGE
if selected == "Overview":
    tab1,tab2 = st.tabs([" 📝 *RAW DATA*", "🚀 *INSIGHTS*"])
    
    # RAW DATA TAB
    with tab1:
        # RAW DATA
        col1,col2 = st.columns(2)
        if col1.button("Click to view Raw data"):
            col1.write(col.find_one())
        # DATAFRAME FORMAT
        if col2.button("Click to view Dataframe"):
            col1.write(col.find_one())
            col2.write(df)
    
    # st.map(df, latitude="Latitude", longitude="Longitude")
        #    , size="col3", color="col4")