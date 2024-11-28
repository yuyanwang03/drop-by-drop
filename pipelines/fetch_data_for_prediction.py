import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def prepare_dataset_for_prediction(pandas_dataset, prediction_final_day, pernoctation_mean, tourist_distribution):
    """
    Modify the dataset by adding rows for prediction days and filling weather columns.
    
    Args:
        pandas_dataset (pd.DataFrame): The original dataset.
        prediction_final_day (str): The last day of the prediction period in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: Modified dataset with additional rows and filled weather columns.
    """
    # Convert prediction_final_day to datetime
    prediction_final_day = datetime.strptime(prediction_final_day, "%Y-%m-%d")
    
    # Get the last date in the dataset
    last_date = pd.to_datetime(pandas_dataset['Date'].max())
    
    # Create a list of new dates
    new_dates = pd.date_range(start=last_date + timedelta(days=1), end=prediction_final_day)

    # Drop columns Use, Number of Meters
    pandas_dataset = pandas_dataset.drop(columns=['Use', 'Number of Meters'])
    
    # Create an empty list to store new rows
    new_rows = []
    
    # Loop through each unique census section and district
    unique_combinations = pandas_dataset[['Census Section', 'District']].drop_duplicates()
    for date in new_dates:
        for _, row in unique_combinations.iterrows():
            new_row = row.to_dict()  # Convert row to dictionary
            new_row['Date'] = date.strftime('%Y-%m-%d')
            new_rows.append(new_row)
    
    # Convert new rows into a DataFrame
    new_rows_df = pd.DataFrame(new_rows)
    
    # Add previous year date column to new rows
    new_rows_df['Previous Year Date'] = pd.to_datetime(new_rows_df['Date']) - timedelta(days=365)
    
    # Ensure the Date column in the original dataset is datetime format is YYY-MM-DD
    pandas_dataset['Date'] = pd.to_datetime(pandas_dataset['Date'], format='%Y-%m-%d')

    
    # Merge new rows with the original dataset on Census Section, District, and Previous Year Date
    merged_df = pd.merge(
        new_rows_df,
        pandas_dataset,
        left_on=['Census Section', 'District', 'Previous Year Date'],
        right_on=['Census Section', 'District', 'Date'],
        suffixes=('', '_previous_year'),
        how='left'
    )
    
    # Fill weather columns from the previous year
    new_rows_df['temp_max'] = merged_df['temp_max']
    new_rows_df['temp_min'] = merged_df['temp_min']
    new_rows_df['precipitacion'] = merged_df['precipitacion']
    
    # Drop the Previous Year Date column as it is no longer needed
    new_rows_df = new_rows_df.drop(columns=['Previous Year Date'])

    # Fill the population column with the last value of the original dataset without iloc
    new_rows_df['Population'] = pandas_dataset['Population'].iat[-1]

    new_rows_df['Date'] = pd.to_datetime(new_rows_df['Date'], format='%Y-%m-%d')
    tourist_distribution['Date'] = pd.to_datetime(tourist_distribution['Date'], format='%Y-%m-%d')
    
    # Ensure Date columns are in datetime format for merging
    new_rows_df['Date'] = pd.to_datetime(new_rows_df['Date'], format='%Y-%m-%d')
    tourist_distribution['Date'] = pd.to_datetime(tourist_distribution['Date'], format='%Y-%m-%d')
    # Now add to a column named tourists with the number of tourists for each date (for each census section and district) simply when you find a date fill it with the number of tourists
    new_rows_df = pd.merge(new_rows_df, tourist_distribution, on=['Date'], how='left')
    
    # Compute pernoctacions using the Tourists column and cast to integer
    new_rows_df['pernoctacions'] = np.floor(new_rows_df['Tourists'] * pernoctation_mean).astype(int)

    # Drop the Tourists column as it is no longer needed
    new_rows_df = new_rows_df.drop(columns=['Tourists'])

    # Fill NaN values with 0
    new_rows_df = new_rows_df.fillna(0)

    # Order new rows by Census Section, District, and Date
    new_rows_df = new_rows_df.sort_values(by=['Census Section', 'District', 'Date']).reset_index(drop=True)

    # Append the new rows to the original dataset
    updated_dataset = pd.concat([pandas_dataset, new_rows_df], ignore_index=True)

    return updated_dataset



# Load the dataset
dataset = pd.read_csv('../data/local_data/merged_cleaned_data_NEW.csv')


# Prepare the dataset for prediction (IVAN ESTO SUSTITUYELO POR LOS DATOS DE STREAMLIT)
prediction_final_day = '2024-02-14'
pernoctation_mean = 2.5
tourist_distribution = pd.read_csv('martigay.csv')
# Drop all rows except Tourists
tourist_distribution = tourist_distribution.drop(columns=['Id'])

updated_dataset = prepare_dataset_for_prediction(dataset, prediction_final_day, pernoctation_mean, tourist_distribution)

# Save the updated dataset
updated_dataset.to_csv('../data/local_data/updated_dataset_for_prediction.csv', index=False)