import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LogNorm
from styles import display_text

# Function to filter data by year and/or month
def filter_by_date(data, year=None, month=None):
    if year:
        data = data[data['Date'].dt.year == int(year)]
    if month:
        data = data[data['Date'].dt.month == int(month)]
    return data

# Function to group data by the desired period (Mes, Dia, or Setmana)
def group_by_period(data, group_by='Mes'):
    if group_by == 'Mes':
        data['Period'] = data['Date'].dt.to_period('M')
    elif group_by == 'Dia':
        data['Period'] = data['Date'].dt.date
    elif group_by == 'Setmana':
        data['Period'] = data['Date'].dt.isocalendar().week
    return data

# Function to apply the custom style to the plot
def apply_custom_style(ax):
    # Set the color of the spines (axes borders)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    
    # Set the background color of the plot area
    ax.set_facecolor("none") 
    
    # Remove the figure background
    ax.figure.patch.set_alpha(0)

    # Set the color of the ticks and labels to white
    ax.tick_params(axis='both', colors='white')


# Plot for accumulated consumption per use
def plot_accumulated_consumption_per_use(data, year=None, month=None):
    data = filter_by_date(data, year, month)
    
    # Group by 'Use' and sum the 'Accumulated Consumption'
    consumption_per_use = data.groupby('Use', as_index=False)['Accumulated Consumption'].sum()

    fig, ax = plt.subplots(figsize=(8, 3))
    sns.barplot(x="Use", y="Accumulated Consumption", data=consumption_per_use, ax=ax)
    ax.set_xlabel("Ús",color= 'white')
    ax.set_ylabel("Consum Acumulat (L/dia)",color= 'white')
    
    apply_custom_style(ax)

    st.pyplot(fig)


# Plot for accumulated consumption per district
def plot_accumulated_consumption_per_district(data, year=None, month=None):
    data = filter_by_date(data, year, month)
    
    # Group by 'District' and sum the 'Accumulated Consumption'
    consumption_per_district = data.groupby('District', as_index=False)['Accumulated Consumption'].sum()

    fig, ax = plt.subplots(figsize=(8, 3))
    sns.barplot(x="District", y="Accumulated Consumption", data=consumption_per_district, ax=ax)
    ax.set_xlabel("Districte", color= 'white')
    ax.set_ylabel("Consum Acumulat (L/dia)", color= 'white')
    
    apply_custom_style(ax)

    st.pyplot(fig)

# Plot for accumulated consumption per use and district
def plot_accumulated_consumption_per_use_and_district(data, year=None, month=None):
    data = filter_by_date(data, year, month)
    
    # Group by 'District' and 'Use', and sum the 'Accumulated Consumption'
    consumption_per_use_and_district = data.groupby(['District', 'Use'], as_index=False)['Accumulated Consumption'].sum()

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x="District", y="Accumulated Consumption", hue="Use", data=consumption_per_use_and_district, ax=ax)
    ax.set_xlabel("Districte",color= 'white')
    ax.set_ylabel("Consum Acumulat (L/dia)",color= 'white')
    ax.legend(title="Ús")
    
    apply_custom_style(ax)

    st.pyplot(fig)

def plot_accumulated_domestic_consumption_and_district(data, year=None, month=None):

    data = filter_by_date(data, year, month)
    data = data[data['Use'] =='Domestic']
    
    # Group by 'District' and 'Use', and sum the 'Accumulated Consumption'
    consumption_per_district = data.groupby(['District'], as_index=False)['Accumulated Consumption'].sum()
    population_per_district = data.groupby(['District'], as_index=False)['Population'].mean()

    # Merge the two DataFrames to align population and consumption data by 'District'
    merged_data = pd.merge(consumption_per_district, population_per_district, on='District')

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 4))

    # Barplot for 'Accumulated Consumption'
    sns.barplot(x="District", y="Accumulated Consumption", data=merged_data, ax=ax1)
    ax1.set_xlabel("Districte", color='white')
    ax1.set_ylabel("Consum Acumulat (L/dia)", color='white')
    apply_custom_style(ax1)

    # Twin axis for Population
    ax2 = ax1.twinx()
    ax1.set_xticks(range(len(merged_data)))  # Explicitly set x-ticks for ax1 (bar plot)
    ax1.set_xticklabels(merged_data['District'])  # Set correct labels and rotation

    # Plot Population on ax2 (right axis)
    ax2.plot(range(len(merged_data)), merged_data['Population'], color='white', marker='o', linestyle='-')
    ax2.set_ylabel('Habitants', color='white')
    ax2.tick_params(axis='y', labelcolor='white')

    ax1.set_xticks(ax2.get_xticks())

    apply_custom_style(ax2)

    st.pyplot(fig)


def plot_consumption_vs_accommodations(data, year=None, month=None, group_by='Mes'):

    # Filter the data based on year and month
    data = filter_by_date(data, year, month)
    
    # Group data based on the 'group_by' parameter (Month, Day, or Week)
    data = group_by_period(data, group_by)

    # Group by 'Period' and sum the values for 'Accumulated Consumption' and 'pernoctacions'
    consumption_by_period = data.groupby('Period', as_index=False)['Accumulated Consumption'].sum()
    accomodations_by_period = data.groupby('Period', as_index=False)['pernoctacions'].sum()

    # Merge the grouped dataframes on 'Period'
    merged_data = pd.merge(consumption_by_period, accomodations_by_period, on='Period')

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(10, 4))
    
    # Bar plot for 'Accumulated Consumption'
    ax1.bar(merged_data['Period'].astype(str), merged_data['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by, color='white')
    ax1.set_ylabel('Consum Acumulat (L/dia)', color='white')
    ax1.tick_params(axis='y', labelcolor='white')
    ax1.tick_params(axis='x', colors='white')

    # Apply the custom style
    apply_custom_style(ax1)

    # Line plot for 'pernoctacions'
    ax2 = ax1.twinx()
    ax2.plot(merged_data['Period'].astype(str), merged_data['pernoctacions'], color='red', marker='o', linestyle='-', label='Allotjaments Totals')
    ax2.set_ylabel('Allotjaments Totals', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Apply the custom style to ax2 as well
    apply_custom_style(ax2)

    # Set x-ticks
    x_ticks = range(0, len(merged_data['Period']), 5)
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(merged_data['Period'].astype(str).iloc[x_ticks], rotation=45, color='white')

    # Add legend
    ax2.legend(loc="upper left")

    # Set the figure background to be transparent
    fig.patch.set_alpha(0)
    ax1.set_facecolor("none")

    text = "Consum i Pernoctacions per " + group_by

    # Add title and plot
    display_text(text, shadow_offset= "2px 2px")
    st.pyplot(fig)


def plot_consumption_vs_precipitation(data, year=None, month=None, group_by='Mes'):

    # Filter the data based on year and month
    data = filter_by_date(data, year, month)
    
    # Group data based on the 'group_by' parameter (Month, Day, or Week)
    data = group_by_period(data, group_by)

    # Aggregate consumption and precipitation by period
    consumption_by_period = data.groupby('Period', as_index=False)['Accumulated Consumption'].sum()
    precipitation_by_period = data.groupby('Period', as_index=False)['precipitacion'].sum()

    # Merge the consumption and precipitation data
    merged_data = pd.merge(consumption_by_period, precipitation_by_period, on='Period')

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(10, 4))
    
    # Bar plot for 'Accumulated Consumption'
    ax1.bar(merged_data['Period'].astype(str), merged_data['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by, color='white')
    ax1.set_ylabel('Consum Acumulat (L/dia)', color='white')
    ax1.tick_params(axis='y', labelcolor='white')
    ax1.tick_params(axis='x', colors='white')


    # Apply the custom style to ax1
    apply_custom_style(ax1)

    # Line plot for 'precipitacion'
    ax2 = ax1.twinx()
    ax2.plot(merged_data['Period'].astype(str), merged_data['precipitacion'], color='yellow', marker='o', linestyle='-', label='Precipitació')
    ax2.set_ylabel('Precipitació', color='yellow')
    ax2.tick_params(axis='y', labelcolor='yellow')

    # Apply the custom style to ax2
    apply_custom_style(ax2)

    # Set x-ticks
    x_ticks = range(0, len(merged_data['Period']), 5)
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(merged_data['Period'].astype(str).iloc[x_ticks], rotation=45, color='white')

    # Add legend
    ax2.legend(loc="upper left")

    # Set figure transparency
    fig.patch.set_alpha(0)
    ax1.set_facecolor("none")

    text = "Consum i Precipitació per " + group_by

    # Add title and plot
    display_text(text, shadow_offset= "2px 2px")
    st.pyplot(fig)

def plot_consumption_vs_temperature(data, year=None, month=None, group_by='Mes'):
    # Filter the data based on year and month
    data = filter_by_date(data, year, month)
    
    # Group data based on the 'group_by' parameter (Month, Day, or Week)
    data = group_by_period(data, group_by)

    # Group by the selected period and calculate the sum of consumption and average temperatures
    monthly_temps = data.groupby('Period').agg({
        'Accumulated Consumption': 'sum',  # Sum for consumption
        'temp_max': 'mean',         # Average for max temperature
        'temp_min': 'mean'          # Average for min temperature
    }).reset_index()

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(10, 4))

    # Bar chart for 'Accumulated Consumption'
    ax1.bar(monthly_temps['Period'].astype(str), monthly_temps['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by, color='white')
    ax1.set_ylabel('Consum Acumulat (L/day)', color='white')
    ax1.tick_params(axis='y', labelcolor='white')

    # Apply the custom style to ax1
    apply_custom_style(ax1)

    # Line chart for 'temp_max' (Max Temperature)
    ax2 = ax1.twinx()
    ax2.plot(monthly_temps['Period'].astype(str), monthly_temps['temp_max'], color='green', marker='o', linestyle='-', label='Max Temperature')
    ax2.set_ylabel('Temperatura(°C)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Line chart for 'temp_min' (Min Temperature)
    ax2.plot(monthly_temps['Period'].astype(str), monthly_temps['temp_min'], color='red', marker='o', linestyle='-', label='Min Temperature')
    ax2.set_ylabel('Temperatura (°C)', color='white')
    ax2.tick_params(axis='y', labelcolor='red')

    # Apply the custom style to ax2
    apply_custom_style(ax2)

    # Set x-ticks and labels for every 5th period
    x_ticks = range(0, len(monthly_temps['Period']), 5)
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(monthly_temps['Period'].astype(str).iloc[x_ticks], rotation=45, color='white')

    # Add the legend for temperature lines
    ax2.legend(loc="upper left")

    # Set figure transparency
    fig.patch.set_alpha(0)
    ax1.set_facecolor("none")

    text = "Consum i Temperatura per " + group_by

    # Add title and plot
    display_text(text, shadow_offset= "2px 2px")
    st.pyplot(fig)

def census_consumption(df, census, join_on='Census'):

    def prepare_data(df, group_by_col, merge_col, geo_col):
        """
        Prepares and merges the data with the geospatial census data.
        """
        # Group data
        df_grouped = df.groupby(group_by_col).agg({
            'Accumulated Consumption': 'sum',
        }).reset_index()

        # Merge with census data
        merged_data = census.merge(df_grouped, left_on=merge_col, right_on=group_by_col)
        
        # Convert to GeoDataFrame and handle zero consumption
        geo_df = gpd.GeoDataFrame(merged_data)
        geo_df['Accumulated Consumption'] = geo_df['Accumulated Consumption'].replace(0, 0.00001)
        return geo_df

    def plot_geodataframe(geo_df, title):
        """
        Plots the GeoDataFrame with a logarithmic color scale.
        """
        # Display title
        display_text(title, shadow_offset="2px 2px")

        # Plot map
        fig, ax = plt.subplots(figsize=(5, 3))
        geo_df.plot(
            column='Accumulated Consumption',
            cmap='viridis',
            legend=True,
            legend_kwds={
                'orientation': "horizontal",
                'shrink': 0.8
            },
            ax=ax,
            norm=LogNorm(vmin=geo_df['Accumulated Consumption'].min(), vmax=geo_df['Accumulated Consumption'].max())
        )

        ax.axis('off')
        ax.set_facecolor("none")
        fig.patch.set_alpha(0)

        # Display map in Streamlit
        st.pyplot(fig)

    if join_on == 'Census':
        # Preprocess 'Census Section' column
        df['Census Section'] = df['Census Section'].astype(str).str[-3:]
        
        # Prepare data and plot
        geo_df = prepare_data(df, group_by_col='Census Section', merge_col='SEC_CENS', geo_col='Census Section')
        plot_geodataframe(geo_df, title="Consum per Secció Censal")

    elif join_on == 'District':
        # Preprocess 'District' column
        df['District'] = df['District'].apply(lambda x: f"{int(x):02d}")
        
        # Prepare data and plot
        geo_df = prepare_data(df, group_by_col='District', merge_col='DISTRICTE', geo_col='District')
        plot_geodataframe(geo_df, title="Consum per Districte")





# Define the common plot function outside dynamic_grouping_plot
def plot_common(data, census, year=None, month=None, group_by='Mes', static=True):

    join_on = 'District'
    _, midcol, _ = st.columns([1, 11 , 1])
    with midcol:

        col1, col2 = st.columns(2)

        if static:

            join_on = 'Census'
            # Plot 1: Accumulated Consumption per Use (First Column)
            with col1:
                display_text("Consum acomulat per Ús", shadow_offset= "2px 2px")
                plot_accumulated_consumption_per_use(data, year=year, month=month)

            # Plot 2: Accumulated Consumption per District (Second Column)
            with col2:
                display_text("Consum acomulat per Districte", shadow_offset= "2px 2px")
                plot_accumulated_consumption_per_district(data, year=year, month=month)

            display_text("Consum acomulat per Ús i Districte", shadow_offset= "2px 2px")
            plot_accumulated_consumption_per_use_and_district(data, year=year, month=month)

            display_text("Consum Domèstic acomulat per Districte i Habitants", shadow_offset= "2px 2px")
            plot_accumulated_domestic_consumption_and_district(data, year=year, month=month)

        # Plot by consumption, precipitation, and temperature based on grouping
        plot_consumption_vs_accommodations(data, group_by=group_by, year=year, month=month)
        plot_consumption_vs_precipitation(data, group_by=group_by, year=year, month=month)
        plot_consumption_vs_temperature(data, group_by=group_by, year=year, month=month)
        census_consumption(data, census, join_on=join_on)