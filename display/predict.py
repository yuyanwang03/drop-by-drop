import streamlit as st
from styles import inject_custom_css, display_text
from static_graphs import plot_common
import pandas as pd
from datetime import datetime, timedelta
import os
import sys
import io
# Set the path one level higher
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipelines.fetch_data_for_prediction import prepare_dataset_for_prediction
from models.lstm import inference_per_district
from models.regressor import LSTMRegressor

models_path = "../../models/"


def calculate_distribution(num_days, total_tourists, start_date, concentration_periods=None):
    tourists = [0] * num_days  # Initialize all days to 0 tourists
    days_used = set()  # Track days covered by concentrated periods
    
    # If there are concentration periods, calculate their total tourists
    total_concentrated_tourists = 0
    if concentration_periods:
        for start_conc, end_conc, num_conc_tourists in concentration_periods:
            total_concentrated_tourists += num_conc_tourists
            # Mark days used by the concentration period
            for day in range((start_conc - start_date).days, (end_conc - start_date).days + 1):
                days_used.add(day)
    
    # Calculate remaining tourists to distribute on non-concentration days
    remaining_tourists = total_tourists - total_concentrated_tourists
    if remaining_tourists < 0:
        raise ValueError("The total number of concentrated tourists exceeds the total tourists available.")
    
    # Identify days not covered by any concentration period
    free_days = [i for i in range(num_days) if i not in days_used]
    
    # Distribute tourists evenly across free days
    tourists_per_day = remaining_tourists // len(free_days) if free_days else 0
    leftover_tourists = remaining_tourists % len(free_days) if free_days else 0
    
    for i in free_days:
        tourists[i] = tourists_per_day
        # if leftover_tourists > 0:
        #     tourists[i] += 1
        #     leftover_tourists -= 1
    
    # Apply the concentrated periods
    if concentration_periods:
        for start_conc, end_conc, num_conc_tourists in concentration_periods:
            start_idx = (start_conc - start_date).days
            end_idx = (end_conc - start_date).days
            
            # Distribute the concentrated tourists evenly across the selected period
            tourists_per_day_conc = num_conc_tourists // (end_idx - start_idx + 1)
            #remaining_conc_tourists = num_conc_tourists % (end_idx - start_idx + 1)
            
            for i in range(start_idx, end_idx + 1):
                # Override the default tourists for concentrated days
                tourists[i] = tourists_per_day_conc #+ (1 if remaining_conc_tourists > 0 else 0)
                #remaining_conc_tourists -= 1
    
    return tourists

def calculate_distribution_w_noice_from_transactions(num_days, total_tourists, start_date, concentration_periods=None, transactions=None, constant_ratio=0.90):
    """
    Calculate daily distribution of tourists with a constant baseline and variability based on transaction data.

    Args:
        num_days (int): Number of days to distribute tourists over.
        total_tourists (int): Total number of tourists.
        start_date (datetime.date): Start date for the distribution.
        transactions (pd.DataFrame): DataFrame with columns ['Data', 'Series 1'].
        concentration_periods (list of tuples): List of (start_date, end_date, num_tourists) for concentrated periods.
        constant_ratio (float): Proportion of tourists to assign as constant across all days (default: 70%).

    Returns:
        list: Daily distribution of tourists.
    """
    # Validate constant_ratio
    if not (0 <= constant_ratio <= 1):
        raise ValueError("constant_ratio must be between 0 and 1.")

    # WARN: This is actually hardcoding...
    transactions = pd.read_csv("../data/total_transactions.csv")
    transactions['Date'] = pd.to_datetime(transactions['Data']).dt.date

    # Filter transactions within the specified date range
    transactions = transactions[
        (transactions['Date'] >= start_date) &
        (transactions['Date'] < start_date + pd.Timedelta(days=num_days))
    ]

    # Add a column for the daily transaction proportion
    total_transactions = transactions['Series 1'].sum()
    if total_transactions == 0:
        raise ValueError("Total transactions in the period cannot be zero.")
    transactions['Transaction Proportion'] = (
        transactions['Series 1'] / total_transactions
    )

    days_used = set()  # Track days covered by concentrated periods
    # If there are concentration periods, calculate their total tourists
    total_concentrated_tourists = 0
    if concentration_periods:
        for start_conc, end_conc, num_conc_tourists in concentration_periods:
            total_concentrated_tourists += num_conc_tourists
            # Mark days used by the concentration period
            for day in range((start_conc - start_date).days, (end_conc - start_date).days + 1):
                days_used.add(day)

    total_tourists -= total_concentrated_tourists
    if total_tourists < 0:
        raise ValueError("The total number of concentrated tourists exceeds the total tourists available.")
    
    # Split tourists into constant and variable components
    constant_tourists = int(total_tourists * constant_ratio)
    variable_tourists = total_tourists - constant_tourists

    # Assign constant tourists evenly across all days
    constant_per_day = constant_tourists // num_days
    tourists = [constant_per_day] * num_days
    leftover_constant = constant_tourists % num_days

    # Distribute leftover constant tourists
    for i in range(leftover_constant):
        tourists[i] += 1

    # Distribute variable tourists based on transaction proportions
    for i, row in transactions.iterrows():
        day_index = (row['Date'] - start_date).days
        if 0 <= day_index < num_days:
            tourists[day_index] += int(variable_tourists * row['Transaction Proportion'])

    # Apply the concentrated periods
    if concentration_periods:
        for start_conc, end_conc, num_conc_tourists in concentration_periods:
            start_idx = (start_conc - start_date).days
            end_idx = (end_conc - start_date).days
            
            # Distribute the concentrated tourists evenly across the selected period
            tourists_per_day_conc = num_conc_tourists // (end_idx - start_idx + 1)
            #remaining_conc_tourists = num_conc_tourists % (end_idx - start_idx + 1)
            
            for i in range(start_idx, end_idx + 1):
                # Override the default tourists for concentrated days
                tourists[i] = tourists_per_day_conc #+ (1 if remaining_conc_tourists > 0 else 0)
    
    # # Normalize the distribution to ensure the total matches the input total_tourists
    # adjustment_factor = total_tourists / sum(tourists) if sum(tourists) > 0 else 1
    # tourists = [int(t * adjustment_factor) for t in tourists]

    return tourists


def display_tourist_distribution(start_date, end_day_num, total_tourists, start_day_num, concentration_periods=None):
    # If concentration periods are provided, calculate using them
    if concentration_periods:
        try:
            pernoctation_distribution = calculate_distribution_w_noice_from_transactions(
            num_days=(end_day_num - start_day_num + 1),
            total_tourists=total_tourists,
            start_date=start_date,
            concentration_periods=concentration_periods
            )
        except:
            pernoctation_distribution = calculate_distribution(
                num_days=(end_day_num - start_day_num + 1),
                total_tourists=total_tourists,
                start_date=start_date,
                concentration_periods=concentration_periods
            )
    else:
        # If no concentration periods, calculate the distribution with smooth option
        try:
            pernoctation_distribution = calculate_distribution_w_noice_from_transactions(
                num_days=(end_day_num - start_day_num + 1),
                total_tourists=total_tourists,
                start_date=start_date
            )
        except:
            pernoctation_distribution = calculate_distribution(
            num_days=(end_day_num - start_day_num + 1),
            total_tourists=total_tourists,
            start_date=start_date
            )  
    
    # Prepare the DataFrame for display
    df = pd.DataFrame({
        'Date': [start_date + timedelta(days=i) for i in range(end_day_num)],
        'Tourists': pernoctation_distribution
    })
    
    return df


def reset_state():
    st.session_state.concentration_option = 'Regular'
    st.session_state.concentration_periods = []


def predict(data, census):

    col1, _, col2 = st.columns([3,1,1])

    with col1:
        st.image("media/header1.png", width=600)
    
    with col2:
        st.image("media/header2.png", width = 240)

    # Custom HTML with text-shadow effect
    display_text("Predicció del consum d'aigua", font_size="80px", text_color="rgb(56, 182, 255)", shadow_offset= "4px 4px")

    text = "Aquesta pàgina permet veure una simulació a futur del consum d'aigua a Barcelona segons el número de turistes."
    display_text(text)

    if 'concentration_option' not in st.session_state:
        st.session_state['concentration_option'] = 'Regular'

    if 'concentration_periods' not in st.session_state:
        st.session_state['concentration_periods'] = []

    # Load the model
    #model = load_model()

    # Set the start date as 31/4/2024
    start_date = datetime(2024, 1, 1).date()
    min_date = start_date + timedelta(days=30)
    
    # Set the max end date to 90 days after the start date
    end_date_max = start_date + timedelta(days=89)

    # User selects the number of days using the date input widget
    end_day_input = st.date_input('Selecciona una data final (mínim requerit 30 dies)', value=end_date_max, min_value=min_date, max_value=end_date_max)

    # Convert the selected start and end dates to day numbers relative to the start date
    start_day_num = (start_date - start_date).days + 1
    end_day_num = (end_day_input - start_date).days + 1


    tourist_col, avg_pernoctation_col = st.columns(2)

    with tourist_col:
        # Input: Total number of tourists
        total_tourists = st.number_input('Introdueix el número de turistes', min_value=1, value=10000)

    with avg_pernoctation_col:
        avg_pernoctation_col = st.number_input("Introdueix l'estada mitjana dels turistes (en dies)",value= 1.0,min_value=1.0, max_value=90.0, step=0.1)

    # Option to smooth or concentrate
    concentration_option = st.selectbox('Vols que els turistes estiguin concentrarts de manera regular, o vols concentrar turistes en un períod determinat?',
            ['Regular', 'Concentrar turistes'],
            key='concentration_option')

    # Initialize a list to store concentration periods
    if 'concentration_periods' not in st.session_state:
        st.session_state['concentration_periods'] = []

    overlapping = False
    # Add concentration button
    if concentration_option == 'Concentrar turistes':

        st.session_state['concentration_periods'] = st.session_state.get('concentration_periods', [])

        text = "A continuació, selecciona quants turistes vols que arribin a la ciutat de Barcelona en els dies seleccionats. Nosaltres ens encarregarem de distribuir els turistes de manera correcte."

        display_text(text)

        # Function to add new concentration period
        def add_concentration_period():
            st.session_state['concentration_periods'].append({
                'start_concentration_day': start_date + timedelta(days=1),  # Default start is after 1 days
                'end_concentration_day': start_date + timedelta(days=2),   # Default end is after 2 days
                'tourists_concentrated': 1  # Default concentrated tourists
            })

        # Display the button to add a concentration period
        st.button('Afegir un nou període de concentració', on_click=add_concentration_period)

        # Loop through existing concentration periods and display inputs
        for idx, period in enumerate(st.session_state['concentration_periods']):

            col1, col2 = st.columns(2)

            with col1:
                start_concentration_day = st.date_input(
                    f"Seleccioneu l'inici del període {idx + 1}",
                    value=period['start_concentration_day'],
                    min_value=start_date,
                    max_value=end_day_input
                )

            if period['end_concentration_day'] < start_concentration_day:
                period['end_concentration_day'] = start_concentration_day + timedelta(days=1)

            with col2:

                end_concentration_day = st.date_input(
                    f'Seleccioneu el final del període {idx + 1}',
                    value=period['end_concentration_day'],
                    min_value=start_concentration_day,
                    max_value=end_day_input
                )

            tourists_concentrated = st.number_input(
                f'Quants turístes arriben a Barcelona durant aquest període? {idx + 1}',
                min_value=1,
                max_value=total_tourists,
                value=period['tourists_concentrated']
            )

            # Update the session state with the new values
            st.session_state['concentration_periods'][idx] = {
                'start_concentration_day': start_concentration_day,
                'end_concentration_day': end_concentration_day,
                'tourists_concentrated': tourists_concentrated
            }

            # Add a horizontal line after each concentration period
            st.markdown("---")

            # Check for overlapping dates
            overlapping = False
            for i, other_period in enumerate(st.session_state['concentration_periods']):
                if i != idx:
                    # Check if the new concentration period overlaps with any existing ones
                    if not (end_concentration_day < other_period['start_concentration_day'] or start_concentration_day > other_period['end_concentration_day']):
                        overlapping = True
                        break

        if overlapping:
            st.error(f"Error: El període seleccionat {idx + 1} coincideix amb un altre període. Siusplau, seleccioneu un període correcte.")

    # Button to trigger the calculation
    if st.button('Calcular Distribució'):
        # Error handling for invalid inputs
        if concentration_option == 'Concentrar turistes':
            if total_tourists < sum([period['tourists_concentrated'] for period in st.session_state['concentration_periods']]):
                st.error('Error: Total tourists cannot be less than the sum of tourists in all concentration periods.')
            else:
                # If inputs are valid, calculate and show the distribution
                concentration_periods = [
                    (period['start_concentration_day'], period['end_concentration_day'], period['tourists_concentrated'])
                    for period in st.session_state['concentration_periods']
                ]
                # Call the function to display the distribution
                df = display_tourist_distribution(start_date, end_day_num, total_tourists, start_day_num, concentration_periods)
        else:
            # If "Smooth" option is selected, calculate and show the distribution
            df = display_tourist_distribution(start_date, end_day_num, total_tourists, start_day_num)
        

        df_predict = prepare_dataset_for_prediction(data, end_day_input, avg_pernoctation_col, df)

        results = inference_per_district(df_predict, end_day_num)

        final_results = results.merge(df_predict, on=['Date', 'District'], how='left')
        print(final_results.columns)

        final_results.drop(['Accumulated Consumption_y'], axis=1, inplace=True)
        final_results = final_results.rename(columns={
            'Accumulated Consumption_x': 'Accumulated Consumption'})

        st.write(final_results.head(15))
        
        
        # Convert DataFrame to CSV and create a download link
        csv = final_results.to_csv(index=False)
        st.download_button(
            label="Descarrega el resultat complet en format CSV",
            data=csv,
            file_name='prediccio_resultats.csv',
            mime='text/csv'
        )

        plot_common(final_results, census, group_by='Dia', static=False)

    st.button('Restart', on_click=reset_state)