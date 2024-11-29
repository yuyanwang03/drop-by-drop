import streamlit as st
import geopandas as gpd
import pandas as pd
from styles import inject_custom_css, display_text
from about_us import about_us
from project_description import project_description
from static_analysis import graph_display
from predict import predict
import torch.nn as nn
from models.lstm import inference_per_district
from models.regressor import LSTMRegressor
import os


# Set the Streamlit configuration for the app
st.set_page_config(
    page_title="Drop by drop",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache the data loading function to avoid reloading the CSV every time
@st.cache_data
def load_data():
    path = "..\data\local_data\merged_cleaned_data_NEW.csv"
    # Convert Windows-style path to Unix-style path for Mac
    if os.name == "posix": path = path.replace("\\", "/") 
    # Load the CSV file once and cache it
    data = pd.read_csv(path)
    # Strip any extra spaces in the column names
    data.columns = data.columns.str.strip()
    # Convert 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])
    # Extract month and year for grouping
    data['Month'] = data['Date'].dt.to_period('M')

    census = gpd.read_file('../data/census_geo.geojson')
    
    return data, census

st.sidebar.title("Navegació")
page = st.sidebar.selectbox("Vés a", 
                         ("Sobre el projecte", "Simulació", "Estudi estàtic", "Sobre nosaltres"))

data, census = load_data()
inject_custom_css()

# Display the selected page
if page == "Simulació":
    predict(data, census)
elif page == "Estudi estàtic":
    graph_display(data, census)
elif page == "Sobre nosaltres":
    about_us()
elif page == "Sobre el projecte":
    project_description()

