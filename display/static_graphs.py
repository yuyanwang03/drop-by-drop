import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_accumulated_consumption_per_use(data, year=None, month=None):

    # Filter by year if a year is selected
    if year:
        data = data[data['Date'].dt.year == int(year)]

    # Filter by month if a month is selected
    if month:
        data = data[data['Date'].dt.month == int(month)]

    """Plot Accumulated Consumption per Use"""
    consumption_per_use = data.groupby('Use', as_index=False)['Accumulated Consumption'].sum()
    fig1, ax1 = plt.subplots(figsize=(8, 3))
    sns.barplot(x="Use", y="Accumulated Consumption", data=consumption_per_use, ax=ax1)
    ax1.set_xlabel("Use")
    ax1.set_ylabel("Accumulated Consumption (L/day)")
    st.pyplot(fig1)


def plot_accumulated_consumption_per_district(data, year=None, month=None):

    # Filter by year if a year is selected
    if year:
        data = data[data['Date'].dt.year == int(year)]

    # Filter by month if a month is selected
    if month:
        data = data[data['Date'].dt.month == int(month)]

    """Plot Accumulated Consumption per District"""
    consumption_per_district = data.groupby('District', as_index=False)['Accumulated Consumption'].sum()
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    sns.barplot(x="District", y="Accumulated Consumption", data=consumption_per_district, ax=ax2)
    ax2.set_xlabel("District")
    ax2.set_ylabel("Accumulated Consumption (L/day)")
    st.pyplot(fig2)


def plot_accumulated_consumption_per_use_and_district(data, year=None, month=None):

    # Filter by year if a year is selected
    if year:
        data = data[data['Date'].dt.year == int(year)]

    # Filter by month if a month is selected
    if month:
        data = data[data['Date'].dt.month == int(month)]

    """Plot Accumulated Consumption per Use and District"""
    consumption_per_use = data.groupby(['District', 'Use'], as_index=False)['Accumulated Consumption'].sum()
    fig, ax = plt.subplots(figsize=(8, 2))
    sns.barplot(x="District", y="Accumulated Consumption", hue="Use", data=consumption_per_use, ax=ax)
    ax.set_xlabel("District")
    ax.set_ylabel("Accumulated Consumption (L/day)")
    ax.legend(title="Use")
    st.pyplot(fig)


def plot_consumption_vs_accommodations(data, year=None, month=None, group_by='Month'):

    # Filter by year if a year is selected
    if year:
        data = data[data['Date'].dt.year == int(year)]

    # Filter by month if a month is selected
    if month:
        data = data[data['Date'].dt.month == int(month)]

    # Ensure correct groupings based on the parameter
    if group_by == 'Month':
        data['Period'] = data['Date'].dt.to_period('M')
    elif group_by == 'Day':
        data['Period'] = data['Date'].dt.date
    elif group_by == 'Week':
        # Use pd.Grouper to group by week (weeks starting on Monday)
        data['Period'] = data['Date'].dt.isocalendar().week  # Get the week number

    # Group by the selected period
    consumption_by_period = data.groupby('Period', as_index=False)['Accumulated Consumption'].sum()
    accommodations_by_period = data.groupby('Period', as_index=False)['Tourist Accommodations'].sum()
    hotel_overnight_by_period = data.groupby('Period', as_index=False)['Hotel Overnight Stays'].sum()

    # Merge the dataframes
    merged_data = pd.merge(consumption_by_period, accommodations_by_period, on='Period')
    merged_data = pd.merge(merged_data, hotel_overnight_by_period, on='Period')
    merged_data['Total Accommodations'] = merged_data['Tourist Accommodations'] + merged_data['Hotel Overnight Stays']

    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 4))

    # Bar chart for Accumulated Consumption
    ax1.bar(merged_data['Period'].astype(str), merged_data['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by)
    ax1.set_ylabel('Accumulated Consumption (L/day)', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')

    # Line chart for Total Accommodations
    ax2 = ax1.twinx()
    ax2.plot(merged_data['Period'].astype(str), merged_data['Total Accommodations'], color='red', marker='o', linestyle='-', label='Total Accommodations')
    ax2.set_ylabel('Total Accommodations', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    x_ticks = range(0, len(merged_data['Period']), 5)  # Take every 5th index
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(merged_data['Period'].astype(str).iloc[x_ticks])
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

    ax2.legend(loc="upper left")
    st.markdown(f'<p class="custom-subheader-plot">Consumption per {group_by} with Tourist Accommodations and Hotel Overnight Stays</p>', unsafe_allow_html=True)
    st.pyplot(fig)


def plot_consumption_vs_precipitation(data, year=None, month=None, group_by='Month'):

    # Filter by year if a year is selected
    if year:
        data = data[data['Date'].dt.year == int(year)]

    # Filter by month if a month is selected
    if month:
        data = data[data['Date'].dt.month == int(month)]

    # Ensure correct groupings based on the parameter
    if group_by == 'Month':
        data['Period'] = data['Date'].dt.to_period('M')
    elif group_by == 'Day':
        data['Period'] = data['Date'].dt.date
    elif group_by == 'Week':
        data['Period'] = data['Date'].dt.isocalendar().week  # Get the week number

    # Group by the selected period
    consumption_by_period = data.groupby('Period', as_index=False)['Accumulated Consumption'].sum()
    precipitation_by_period = data.groupby('Period', as_index=False)['Precipitation'].sum()

    # Merge the dataframes
    merged_data = pd.merge(consumption_by_period, precipitation_by_period, on='Period')

    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 4))

    # Bar chart for Accumulated Consumption
    ax1.bar(merged_data['Period'].astype(str), merged_data['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by)
    ax1.set_ylabel('Accumulated Consumption (L/day)', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')

    # Line chart for Precipitation
    ax2 = ax1.twinx()
    ax2.plot(merged_data['Period'].astype(str), merged_data['Precipitation'], color='darkblue', marker='o', linestyle='-', label='Precipitation')
    ax2.set_ylabel('Precipitation', color='darkblue')
    ax2.tick_params(axis='y', labelcolor='darkblue')

    x_ticks = range(0, len(merged_data['Period']), 5)  # Take every 5th index
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(merged_data['Period'].astype(str).iloc[x_ticks])
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

    ax2.legend(loc="upper left")
    st.markdown(f'<p class="custom-subheader-plot">Consumption and Precipitation per {group_by}</p>', unsafe_allow_html=True)
    st.pyplot(fig)


def plot_consumption_vs_temperature(data, year=None, month=None, group_by='Month'):

     # Filter by year if a year is selected
    if year:
        data = data[data['Date'].dt.year == int(year)]

    # Filter by month if a month is selected
    if month:
        data = data[data['Date'].dt.month == int(month)]

    # Ensure correct groupings based on the parameter
    if group_by == 'Month':
        data['Period'] = data['Date'].dt.to_period('M')
    elif group_by == 'Day':
        data['Period'] = data['Date'].dt.date
    elif group_by == 'Week':
        data['Period'] = data['Date'].dt.isocalendar().week  # Get the week number

    # Group by the selected period and calculate averages
    monthly_temps = data.groupby('Period').agg({
        'Accumulated Consumption': 'sum',  # Sum for consumption
        'Max Temperature': 'mean',         # Average for max temperature
        'Min Temperature': 'mean'          # Average for min temperature
    }).reset_index()

    # Plot
    fig, ax1 = plt.subplots(figsize=(12, 4))

    # Bar chart for Accumulated Consumption
    ax1.bar(monthly_temps['Period'].astype(str), monthly_temps['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by)
    ax1.set_ylabel('Accumulated Consumption (L/day)', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')

    # Line chart for Max Temperature
    ax2 = ax1.twinx()
    ax2.plot(monthly_temps['Period'].astype(str), monthly_temps['Max Temperature'], color='green', marker='o', linestyle='-', label='Max Temperature')
    ax2.set_ylabel('Temperature (°C)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Line chart for Min Temperature
    ax2.plot(monthly_temps['Period'].astype(str), monthly_temps['Min Temperature'], color='red', marker='o', linestyle='-', label='Min Temperature')
    ax2.set_ylabel('Temperature (°C)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax2.legend(loc="upper left")
    # Set x-axis labels every 5 steps
    x_ticks = range(0, len(monthly_temps['Period']), 5)  # Take every 5th index
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(monthly_temps['Period'].astype(str).iloc[x_ticks])
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

    st.markdown(f'<p class="custom-subheader-plot">Consumption and Temperature per {group_by}</p>', unsafe_allow_html=True)
    st.pyplot(fig)


# Define the common plot function outside dynamic_grouping_plot
def plot_common(data, col1, col2, year=None, month=None, group_by='Month'):
    # Plot 1: Accumulated Consumption per Use (First Column)
    with col1:
        st.markdown('<p class="custom-subheader-plot">Accumulated Consumption per Use</p>', unsafe_allow_html=True)
        plot_accumulated_consumption_per_use(data, year=year, month=month)

    # Plot 2: Accumulated Consumption per District (Second Column)
    with col2:
        st.markdown('<p class="custom-subheader-plot">Accumulated Consumption District</p>', unsafe_allow_html=True)
        plot_accumulated_consumption_per_district(data, year=year, month=month)

    # Plot 3: Accumulated Consumption per Use, per District
    st.markdown('<p class="custom-subheader-plot">Accumulated Consumption per Use and District</p>', unsafe_allow_html=True)
    plot_accumulated_consumption_per_use_and_district(data, year=year, month=month)

    # Plot by consumption, precipitation, and temperature based on grouping
    plot_consumption_vs_accommodations(data, group_by=group_by, year=year, month=month)
    plot_consumption_vs_precipitation(data, group_by=group_by, year=year, month=month)
    plot_consumption_vs_temperature(data, group_by=group_by, year=year, month=month)