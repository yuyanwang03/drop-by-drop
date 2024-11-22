import streamlit as st

from styles import inject_custom_css
from about_us import about_us
from project_description import project_description
from static_analysis import graph_display
from predict import predict

# Set the Streamlit configuration for the app
st.set_page_config(
    page_title="Drop by drop",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.sidebar.image("media/logo_sidebar.png", width =250)
st.sidebar.title("Navegació")
page = st.sidebar.radio("Ves a", 
                         ("Sobre el projecte", "Simulació", "Estudi estàtic", "Sobre nosaltres"))

# Display the selected page
if page == "Simulació":
    predict()
elif page == "Estudi estàtic":
    graph_display()
elif page == "Sobre nosaltres":
    about_us()
elif page == "Sobre el projecte":
    project_description()

