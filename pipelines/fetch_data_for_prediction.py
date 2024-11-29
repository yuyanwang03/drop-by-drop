import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def distribute_values_by_daily_transactions(start_date, end_date, transactions, pernoctacions):
    """
    Distributes monthly values (e.g., overnight stays) across days based on the daily proportion 
    of card transactions with respect to the total transactions for the month.

    Args:
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        transactions (pd.DataFrame): DataFrame with daily transactions data.
        pernoctacions (pd.DataFrame): DataFrame with monthly values to distribute.

    Returns:
        pd.DataFrame: DataFrame with daily distributed values.
    """
    # Filter transactions within the specified date range
    transactions['Data'] = pd.to_datetime(transactions['Data'])
    pernoctacions['Data'] = pd.to_datetime(pernoctacions['Data'])
    
    transactions = transactions[(transactions['Data'] >= start_date) & (transactions['Data'] <= end_date)]
    pernoctacions = pernoctacions[(pernoctacions['Data'] >= start_date) & (pernoctacions['Data'] <= end_date)]

    # Group transactions by month and calculate total transactions per month
    monthly_transactions = transactions.groupby(transactions['Data'].dt.to_period('M'))['total_tourist_transactions'].sum().reset_index()
    monthly_transactions.columns = ['Month', 'Total Transactions']

    # Merge monthly totals with daily transactions to calculate daily percentages
    transactions = transactions.merge(monthly_transactions, left_on=transactions['Data'].dt.to_period('M'), right_on='Month', how='left')
    transactions['Percentage of Transactions'] = transactions['total_tourist_transactions'] / transactions['Total Transactions']
    transactions.drop(columns=['Month'], inplace=True)

    # Initialize the results list
    results = []

    # Loop through pernoctacions rows to distribute values based on daily percentages
    for _, row in pernoctacions.iterrows():
        month = row['Data'].month
        year = row['Data'].year
        monthly_value = row['Pernoctacions']

        # Filter transactions for the current month and year
        transactions_month = transactions[(transactions['Data'].dt.month == month) & (transactions['Data'].dt.year == year)]

        # Normalize percentages to ensure they sum to 1
        transactions_month['Percentage of Transactions'] /= transactions_month['Percentage of Transactions'].sum()

        # Distribute monthly values based on daily percentages
        for _, transaction in transactions_month.iterrows():
            daily_value = round(monthly_value * transaction['Percentage of Transactions'])
            results.append({
                'Day': transaction['Data'],
                'Tipus Allotjament': row['Tipologia d\'allotjament'],
                'Distributed Value': daily_value
            })

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    return results_df


def prepare_dataset_for_prediction(pandas_dataset, prediction_final_day, pernoctation_mean, tourist_distribution):
    """
    Modify the dataset by adding rows for prediction days and filling weather columns.
    
    Args:
        pandas_dataset (pd.DataFrame): The original dataset.
        prediction_final_day (str): The last day of the prediction period in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: Modified dataset with additional rows and filled weather columns.
    """
    
    # Get the last date in the dataset
    last_date = pd.to_datetime(pandas_dataset['Date'].max())
    
    # Create a list of new dates
    new_dates = pd.date_range(start=last_date + timedelta(days=1), end=prediction_final_day)

    pandas_dataset = (
    pandas_dataset.groupby([
            "Census Section", "District", "Date", "temp_max", "temp_min", "precipitacion", "pernoctacions", "Population"
        ], as_index=False)
        .agg({
            "Number of Meters": "sum",
            "Accumulated Consumption": "sum"
        })
    )
    
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
    new_rows_df['Number of Meters'] = merged_df['Number of Meters']
    latest_population = pandas_dataset.groupby(['Census Section', 'District'])['Population'].last().reset_index()

    # Update the Population column in new_rows_df with the latest available value
    new_rows_df = pd.merge(
        new_rows_df,
        latest_population,
        on=['Census Section', 'District'],
        how='left',
        suffixes=('', '_latest')
    )

    # Rename the merged column to Population
    new_rows_df.rename(columns={'Population_latest': 'Population'}, inplace=True)
    
    # Drop the Previous Year Date column as it is no longer needed
    new_rows_df = new_rows_df.drop(columns=['Previous Year Date'])

    # Fill the population column with the values for the population by district and census section

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

    # # Now apply the distribution by the transactions
    # new_rows_df = distribute_values_by_daily_transactions(
    #     start_date=pandas_dataset['Date'].min(),
    #     end_date=pandas_dataset['Date'].max(),
    #     transactions=pandas_dataset,
    #     pernoctacions=new_rows_df
    # )
    # # save dataset newrows to csv
    # new_rows_df.to_csv('HAHAHAnew_rows.csv')

    # Order new rows by Census Section, District, and Date
    new_rows_df = new_rows_df.sort_values(by=['Census Section', 'District', 'Date']).reset_index(drop=True)

    # Append the new rows to the original dataset
    updated_dataset = pd.concat([pandas_dataset, new_rows_df], ignore_index=True)

    return updated_dataset