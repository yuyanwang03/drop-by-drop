import pandas as pd
from collections import Counter
import seaborn as sns
import os
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

# Get the directory of the current script
code_folder = os.path.dirname(os.path.abspath(__file__))

# Navigate up to the parent folder of `extracció_dades` and then into `data`
data_folder = os.path.join(code_folder, "..", "data")

# Normalize the path to resolve `..` properly
data_folder = os.path.abspath(data_folder)

# Construct the path to the CSV file
input_path = os.path.join(data_folder, "local_data", "daily_dataset.csv")


daily_aigues = pd.read_csv(input_path, encoding='latin1')

# Rename columns for clarity
daily_aigues = daily_aigues.rename(columns={
    daily_aigues.columns[0]: 'Census Section',
    daily_aigues.columns[1]: 'District',
    daily_aigues.columns[2]: 'Municipality',
    daily_aigues.columns[3]: 'Date',
    daily_aigues.columns[4]: 'Use',
    daily_aigues.columns[5]: 'Number of Meters',
    daily_aigues.columns[6]: 'Accumulated Consumption'
})

# Convert Date column to datetime
daily_aigues['Date'] = pd.to_datetime(daily_aigues['Date'])

# Replace values in the 'Use' column
daily_aigues['Use'] = daily_aigues['Use'].replace({
    'Comercial/Comercial/Commercial': 'Commercial',
    'DomÃ¨stic/DomÃ©stico/Domestic': 'Domestic',
    'Industrial/Industrial/Industrial': 'Industrial'
})

# Filter data for Barcelona
daily_aigues_bcn = daily_aigues[daily_aigues['Municipality'] == 'BARCELONA'].drop(columns=["Municipality"])

# Drop rows with invalid Census Section or District values
daily_aigues_bcn = daily_aigues_bcn[daily_aigues_bcn['Census Section'] != '<NULL>']
daily_aigues_bcn = daily_aigues_bcn[daily_aigues_bcn['District'] != '>']

# Remove rows with Accumulated Consumption values below 0
daily_aigues_bcn = daily_aigues_bcn[daily_aigues_bcn['Accumulated Consumption'] > 0]

input_path = os.path.join(data_folder, "temperature_precipitation.csv")

clima_df = pd.read_csv(input_path)

# Convert 'fecha' column to datetime and group by date
clima_df['fecha'] = pd.to_datetime(clima_df['fecha'])
clima_df = clima_df.groupby('fecha').agg({
    'temp_max': 'mean',
    'temp_min': 'mean',
    'precipitacion': 'mean'
}).round(2).reset_index()

# Merge meteorological data with water consumption data
merged_data = daily_aigues_bcn.merge(clima_df, left_on='Date', right_on='fecha', how='left').drop(columns=['fecha'])

# Load and prepare the data
input_path = os.path.join(data_folder, "dataset_targetes.csv")

targetes = pd.read_csv(input_path)

targetes = targetes.drop('Espanyola', axis=1)

# Convert the column to datetime format
targetes['Data'] = pd.to_datetime(targetes['Data'])

# Format the date as yyyy-mm-dd
targetes['Data'] = targetes['Data'].dt.strftime('%Y-%m-%d')

# Filter the DataFrame to include only dates from 2021 to 2023
targetes = targetes[(targetes['Data'] >= '2021-01-01') & (targetes['Data'] <= '2023-12-31')]

input_path = os.path.join(data_folder, "total_transactions.csv")
transactions = pd.read_csv(input_path)

# Convert the column to datetime format
transactions['Data'] = pd.to_datetime(transactions['Data'])

# Format the date as yyyy-mm-dd
transactions['Data'] = transactions['Data'].dt.strftime('%Y-%m-%d')

# Filter the DataFrame to include only dates from 2021 to 2023
transactions = transactions[(transactions['Data'] >= '2021-01-01') & (transactions['Data'] <= '2023-12-31')]

# Set the date column as the index for both DataFrames to align dates easily
transactions.set_index('Data', inplace=True)
targetes.set_index('Data', inplace=True)

# Create the total_tourist_transactions column by multiplying Series 1 in transactions by Estrangera in targetes
targetes['total_tourist_transactions'] = (targetes['Estrangera'] * transactions['Series 1'])/100
targetes.reset_index(inplace=True)
transactions = targetes.drop('Estrangera', axis=1)

# Load the datasets
input_path = os.path.join(data_folder, "pernoctacions_2019_2024.csv")
pernoctacions = pd.read_csv(input_path)

# Convert date columns to datetime
pernoctacions['Data'] = pd.to_datetime(pernoctacions['Data'], format='%m/%d/%Y')
transactions['Data'] = pd.to_datetime(transactions['Data'], format='%Y-%m-%d')

# Clean and convert the 'Pernoctacions' column to numeric
pernoctacions['Pernoctacions'] = pd.to_numeric(pernoctacions['Pernoctacions'].str.replace('.', ''), errors='coerce')

# Group transactions by month and calculate the total transactions per month
monthly_transactions = transactions.groupby(transactions['Data'].dt.to_period('M'))['total_tourist_transactions'].sum().reset_index()
monthly_transactions.columns = ['Month', 'Total Transactions']

# Merge monthly totals with daily transactions to calculate daily percentages
transactions = transactions.merge(monthly_transactions, left_on=transactions['Data'].dt.to_period('M'), right_on='Month', how='left')
transactions['Percentage of Transactions'] = transactions['total_tourist_transactions'] / transactions['Total Transactions']

# Remove unnecessary column
transactions.drop(columns=['Month'], inplace=True)

# Initialize the results list
resultados = []

# Loop through each row in pernoctacions to distribute monthly totals across days
for _, row in pernoctacions.iterrows():
    mes = row['Data'].month
    anyo = row['Data'].year
    pernoctaciones_mensuales = row['Pernoctacions']
    
    # Filter the transactions for the current month and year
    transactions_mes = transactions[(transactions['Data'].dt.month == mes) & (transactions['Data'].dt.year == anyo)]
    
    # Ensure the daily percentages add up to 1
    transactions_mes['Percentage of Transactions'] /= transactions_mes['Percentage of Transactions'].sum()
    
    # Distribute pernoctacions based on daily percentages
    for _, transaction in transactions_mes.iterrows():
        pernoctaciones_diarias = round(pernoctaciones_mensuales * transaction['Percentage of Transactions'])
        resultados.append({
            'Day': transaction['Data'],
            'tipus allotjament': row['Tipologia d\'allotjament'],
            'pernoctacions': pernoctaciones_diarias
        })

# Create the final DataFrame
resultado_df = pd.DataFrame(resultados)

# Display a sample of the final DataFrame

# Merge the water consumption data with the tourism data
final_data = merged_data.merge(resultado_df, left_on='Date', right_on='Day', how='left').drop(columns=['Day'])

# Grouping by all columns except 'tipus allotjament' and 'pernoctacions', and summing 'pernoctacions'
final_data = (
    final_data.groupby([
        "Census Section", "District", "Date", "Use", 
        "Number of Meters", "Accumulated Consumption", 
        "temp_max", "temp_min", "precipitacion"
    ], as_index=False)
    .agg({"pernoctacions": "sum"})
)


population_district_ds = pd.read_csv('data/population_barcelona_districts.csv')

population_district_ds = population_district_ds.rename(columns={
    'Tiempo': 'Date',
    'Ciutat Vella': 1,
    'Eixample': 2,
    'Sants-Montjuïc': 3,
    'Les Corts': 4,
    'Sarrià-Sant Gervasi': 5,
    'Gràcia': 6,
    'Horta-Guinardó': 6,
    'Nou Barris': 7,
    'Sant Andreu': 8,
    'Sant Martí': 10
})

# Spanish month mapping
month_mapping = {
    "ene": "01", "feb": "02", "mar": "03", "abr": "04",
    "may": "05", "jun": "06", "jul": "07", "ago": "08",
    "sep": "09", "oct": "10", "nov": "11", "dic": "12"
}

# Function to convert the date using regex
def reformat_date(date_str):
    match = re.match(r"(\d{2}) (\w{3}) (\d{4})", date_str)
    if match:
        day, month, year = match.groups()
        month_num = month_mapping[month]
        return f"{year}-{month_num}-{day}"
    return date_str  # Return the original if no match

# Apply the function to the 'Tiempo' column
population_district_ds["Date"] = population_district_ds["Date"].apply(reformat_date)

# Convert 'Date' columns to datetime
final_data["Date"] = pd.to_datetime(final_data["Date"])
population_district_ds["Date"] = pd.to_datetime(population_district_ds["Date"])

# Now merge the datasets by Date and District, bear in mind the date in the population dataset is the first day of the month. So we need to create a year-month auxiliary column
final_data["YearMonth"] = final_data["Date"].dt.to_period('M')
population_district_ds["YearMonth"] = population_district_ds["Date"].dt.to_period('M')

# Change the population barcelona dataset to have the districts rows. Cols: Date, District, Population
population_district_ds = population_district_ds.melt(id_vars=["YearMonth"], var_name="District", value_name="Population")

# Now merge the datasets
final_data = final_data.merge(population_district_ds, on=["YearMonth", "District"], how="left")

# Drop the auxiliary column
final_data.drop(columns=["YearMonth"], inplace=True)


#Step 4: Save the cleaned dataset
os.makedirs('../data/local_data/', exist_ok=True)
output_path = os.path.join(data_folder, "local_data", "merged_cleaned_data_NEW.csv")
final_data.to_csv(output_path, index=False)
print(f"The dataset contains {final_data.shape[0]} rows.")