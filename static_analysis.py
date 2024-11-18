import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from styles import inject_custom_css
from static_graphs import plot_common


# Define the dynamic_grouping_plot function
def dynamic_grouping_plot(data):
    # Let the user select a year or 'Tots els anys' (All Years)
    year_selection = st.selectbox(
        'Seleccionar any',
        ['Tots els anys', '2021', '2022', '2023']
    )

    # If a specific year is selected, show the month selection
    if year_selection != 'Tots els anys':
        month_selection = st.selectbox(
            'Seleccionar mes',
            ['Tots els mesos', 'Gener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Desembre']
        )
    else:
        month_selection = None  # If 'Tots els anys' is selected, no month selection is needed

    # Add a button to execute the plot generation
    if st.button('Executa'):
        # Create a column layout for the final plot
        col1, col2 = st.columns(2)
        # Determine the appropriate plot grouping based on user selection
        if year_selection == 'Tots els anys':
            plot_common(data, col1, col2, group_by='Mes')  # Grouping by month across all years
        elif month_selection == 'Tots els mesos':
            plot_common(data, col1, col2, year=year_selection, group_by='Setmana')  # Grouping by week for selected year
        elif month_selection:
            month_number = {'Gener': 1, 'Febrer': 2, 'Març': 3, 'Abril': 4, 'Maig': 5, 'Juny': 6, 'Juliol': 7, 'Agost': 8, 'Setembre': 9, 'Octubre': 10, 'Novembre': 11, 'Desembre': 12}
            plot_common(data, col1, col2, year=year_selection, month=month_number[month_selection], group_by='Dia')  # Grouping by day for selected year and month
        else:
            st.warning("Please make valid selections to generate the plots.")

            

# Cache the data loading function to avoid reloading the CSV every time
@st.cache_data
def load_data():
    # Load the CSV file once and cache it
    data = pd.read_csv("../data/local_data/merged_cleaned_data.csv")
    # Strip any extra spaces in the column names
    data.columns = data.columns.str.strip()
    # Convert 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])
    # Extract month and year for grouping
    data['Month'] = data['Date'].dt.to_period('M')
    return data



def graph_display():
    # Inject custom CSS (if needed)
    inject_custom_css()

    # Set the title of the page
    st.title("Estudi estàtic")

    # Load the cached data
    data = load_data()

    dynamic_grouping_plot(data)