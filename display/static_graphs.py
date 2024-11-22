import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyBboxPatch



def plot_accumulated_consumption_per_use(data, year=None, month=None):
    if year:
        data = data[data['Date'].dt.year == int(year)]
    if month:
        data = data[data['Date'].dt.month == int(month)]

    """Gràfic Consum Acumulat per Ús"""
    consumption_per_use = data.groupby('Use', as_index=False)['Accumulated Consumption'].sum()
    fig1, ax1 = plt.subplots(figsize=(8, 3))
    sns.barplot(x="Use", y="Accumulated Consumption", data=consumption_per_use, ax=ax1)
    ax1.set_xlabel("Ús")
    ax1.set_ylabel("Consum Acumulat (L/dia)")

    # Crear un recuadro redondeado de fondo que cubra todo el gráfico, incluidos los ejes
    bbox = FancyBboxPatch(
        (0, 0), 1, 1,  # Coordenadas y tamaño
        boxstyle="round,pad=0.07,rounding_size=0.15",  # Bordes redondeados
        edgecolor="black",
        facecolor=(1, 1, 1, 0.85),
        transform=fig1.transFigure,  # Transformar para que ocupe el área de la figura completa
        zorder=-1  # Colocar en el fondo
    )
    fig1.patches.append(bbox)

    # Eliminar fondo de los ejes y de la figura para evitar bordes adicionales
    ax1.set_facecolor("none")  # Sin fondo en el área de los ejes
    fig1.patch.set_alpha(0)    # Sin fondo en la figura completa
    st.pyplot(fig1)


def plot_accumulated_consumption_per_district(data, year=None, month=None):
    if year:
        data = data[data['Date'].dt.year == int(year)]
    if month:
        data = data[data['Date'].dt.month == int(month)]

    """Gràfic Consum Acumulat per Districte"""
    consumption_per_district = data.groupby('District', as_index=False)['Accumulated Consumption'].sum()
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    sns.barplot(x="District", y="Accumulated Consumption", data=consumption_per_district, ax=ax2)
    ax2.set_xlabel("Districte")
    ax2.set_ylabel("Consum Acumulat (L/dia)")
    # Crear un recuadro redondeado de fondo que cubra todo el gráfico, incluidos los ejes
    bbox = FancyBboxPatch(
        (0, 0), 1, 1,  # Coordenadas y tamaño
        boxstyle="round,pad=0.07,rounding_size=0.15",  # Bordes redondeados
        edgecolor="black",
        facecolor=(1, 1, 1, 0.85),
        transform=fig2.transFigure,  # Transformar para que ocupe el área de la figura completa
        zorder=-1  # Colocar en el fondo
    )
    fig2.patches.append(bbox)

    # Eliminar fondo de los ejes y de la figura para evitar bordes adicionales
    ax2.set_facecolor("none")  # Sin fondo en el área de los ejes
    fig2.patch.set_alpha(0)    # Sin fondo en la figura completa
    st.pyplot(fig2)


def plot_accumulated_consumption_per_use_and_district(data, year=None, month=None):
    if year:
        data = data[data['Date'].dt.year == int(year)]
    if month:
        data = data[data['Date'].dt.month == int(month)]

    """Gràfic Consum Acumulat per Ús i Districte"""
    consumption_per_use = data.groupby(['District', 'Use'], as_index=False)['Accumulated Consumption'].sum()
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x="District", y="Accumulated Consumption", hue="Use", data=consumption_per_use, ax=ax)
    ax.set_xlabel("Districte")
    ax.set_ylabel("Consum Acumulat (L/dia)")
    ax.legend(title="Ús")
    # Crear un recuadro redondeado de fondo que cubra todo el gráfico, incluidos los ejes
    bbox = FancyBboxPatch(
        (0, 0), 1, 1,  # Coordenadas y tamaño
        boxstyle="round,pad=0.07,rounding_size=0.15",  # Bordes redondeados
        edgecolor="black",
        facecolor=(1, 1, 1, 0.85),
        transform=fig.transFigure,  # Transformar para que ocupe el área de la figura completa
        zorder=-1  # Colocar en el fondo
    )
    fig.patches.append(bbox)

    # Eliminar fondo de los ejes y de la figura para evitar bordes adicionales
    ax.set_facecolor("none")  # Sin fondo en el área de los ejes
    fig.patch.set_alpha(0)    # Sin fondo en la figura completa
    st.pyplot(fig)


def plot_consumption_vs_accommodations(data, year=None, month=None, group_by='Mes'):
    if year:
        data = data[data['Date'].dt.year == int(year)]
    if month:
        data = data[data['Date'].dt.month == int(month)]

    if group_by == 'Mes':
        data['Period'] = data['Date'].dt.to_period('M')
    elif group_by == 'Dia':
        data['Period'] = data['Date'].dt.date
    elif group_by == 'Setmana':
        data['Period'] = data['Date'].dt.isocalendar().week

    consumption_by_period = data.groupby('Period', as_index=False)['Accumulated Consumption'].sum()
    accomodations_by_period = data.groupby('Period', as_index=False)['pernoctacions'].sum()

    merged_data = pd.merge(consumption_by_period, accomodations_by_period, on='Period')

    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.bar(merged_data['Period'].astype(str), merged_data['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by)
    ax1.set_ylabel('Consum Acumulat (L/dia)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.plot(merged_data['Period'].astype(str), merged_data['pernoctacions'], color='red', marker='o', linestyle='-', label='Allotjaments Totals')
    ax2.set_ylabel('Allotjaments Totals', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    x_ticks = range(0, len(merged_data['Period']), 5)
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(merged_data['Period'].astype(str).iloc[x_ticks], rotation=45)

    ax2.legend(loc="upper left")

    # Crear un recuadro redondeado de fondo que cubra todo el gráfico, incluidos los ejes
    bbox = FancyBboxPatch(
        (0, 0), 1, 1,  # Coordenadas y tamaño
        boxstyle="round,pad=0.07,rounding_size=0.15",  # Bordes redondeados
        edgecolor="black",
        facecolor=(1, 1, 1, 0.85),
        transform=fig.transFigure,  # Transformar para que ocupe el área de la figura completa
        zorder=-1  # Colocar en el fondo
    )
    fig.patches.append(bbox)

    # Eliminar fondo de los ejes y de la figura para evitar bordes adicionales
    ax1.set_facecolor("none")  # Sin fondo en el área de los ejes
    fig.patch.set_alpha(0)    # Sin fondo en la figura completa

    st.markdown(f'<p class="custom-subheader-plot">Consum i Pernoctacions per {group_by}</p>', unsafe_allow_html=True)
    st.pyplot(fig)


def plot_consumption_vs_precipitation(data, year=None, month=None, group_by='Mes'):
    if year:
        data = data[data['Date'].dt.year == int(year)]
    if month:
        data = data[data['Date'].dt.month == int(month)]

    if group_by == 'Mes':
        data['Period'] = data['Date'].dt.to_period('M')
    elif group_by == 'Dia':
        data['Period'] = data['Date'].dt.date
    elif group_by == 'Setmana':
        data['Period'] = data['Date'].dt.isocalendar().week

    consumption_by_period = data.groupby('Period', as_index=False)['Accumulated Consumption'].sum()
    precipitation_by_period = data.groupby('Period', as_index=False)['precipitacion'].sum()

    merged_data = pd.merge(consumption_by_period, precipitation_by_period, on='Period')

    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.bar(merged_data['Period'].astype(str), merged_data['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by)
    ax1.set_ylabel('Consum Acumulat (L/dia)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    ax2.plot(merged_data['Period'].astype(str), merged_data['precipitacion'], color='darkblue', marker='o', linestyle='-', label='Precipitació')
    ax2.set_ylabel('Precipitació', color='darkblue')
    ax2.tick_params(axis='y', labelcolor='darkblue')

    x_ticks = range(0, len(merged_data['Period']), 5)
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(merged_data['Period'].astype(str).iloc[x_ticks], rotation=45)

    ax2.legend(loc="upper left")
    st.markdown(f'<p class="custom-subheader-plot">Consum i Precipitació per {group_by}</p>', unsafe_allow_html=True)

    # Crear un recuadro redondeado de fondo que cubra todo el gráfico, incluidos los ejes
    bbox = FancyBboxPatch(
        (0, 0), 1, 1,  # Coordenadas y tamaño
        boxstyle="round,pad=0.07,rounding_size=0.15",  # Bordes redondeados
        edgecolor="black",
        facecolor=(1, 1, 1, 0.85),
        transform=fig.transFigure,  # Transformar para que ocupe el área de la figura completa
        zorder=-1  # Colocar en el fondo
    )
    fig.patches.append(bbox)

    # Eliminar fondo de los ejes y de la figura para evitar bordes adicionales
    ax1.set_facecolor("none")  # Sin fondo en el área de los ejes
    fig.patch.set_alpha(0)    # Sin fondo en la figura completa
    st.pyplot(fig)

def plot_consumption_vs_temperature(data, year=None, month=None, group_by='Mes'):

     # Filter by year if a year is selected
    if year:
        data = data[data['Date'].dt.year == int(year)]

    # Filter by month if a month is selected
    if month:
        data = data[data['Date'].dt.month == int(month)]

    # Ensure correct groupings based on the parameter
    if group_by == 'Mes':
        data['Period'] = data['Date'].dt.to_period('M')
    elif group_by == 'Dia':
        data['Period'] = data['Date'].dt.date
    elif group_by == 'Setmana':
        data['Period'] = data['Date'].dt.isocalendar().week  # Get the week number

    # Group by the selected period and calculate averages
    monthly_temps = data.groupby('Period').agg({
        'Accumulated Consumption': 'sum',  # Sum for consumption
        'temp_max': 'mean',         # Average for max temperature
        'temp_min': 'mean'          # Average for min temperature
    }).reset_index()

    # Plot
    fig, ax1 = plt.subplots(figsize=(10, 4))

    # Bar chart for Accumulated Consumption
    ax1.bar(monthly_temps['Period'].astype(str), monthly_temps['Accumulated Consumption'], color='skyblue', width=0.5)
    ax1.set_xlabel(group_by)
    ax1.set_ylabel('Consum Acumulat (L/day)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Line chart for Max Temperature
    ax2 = ax1.twinx()
    ax2.plot(monthly_temps['Period'].astype(str), monthly_temps['temp_max'], color='green', marker='o', linestyle='-', label='Max Temperature')
    ax2.set_ylabel('Temperatura (°C)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Line chart for Min Temperature
    ax2.plot(monthly_temps['Period'].astype(str), monthly_temps['temp_min'], color='red', marker='o', linestyle='-', label='Min Temperature')
    ax2.set_ylabel('Temperatura (°C)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax2.legend(loc="upper left")
    # Set x-axis labels every 5 steps
    x_ticks = range(0, len(monthly_temps['Period']), 5)  # Take every 5th index
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(monthly_temps['Period'].astype(str).iloc[x_ticks])
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

    # Crear un recuadro redondeado de fondo que cubra todo el gráfico, incluidos los ejes
    bbox = FancyBboxPatch(
        (0, 0), 1, 1,  # Coordenadas y tamaño
        boxstyle="round,pad=0.07,rounding_size=0.15",  # Bordes redondeados
        edgecolor="black",
        facecolor=(1, 1, 1, 0.85),
        transform=fig.transFigure,  # Transformar para que ocupe el área de la figura completa
        zorder=-1  # Colocar en el fondo
    )
    fig.patches.append(bbox)

    # Eliminar fondo de los ejes y de la figura para evitar bordes adicionales
    ax1.set_facecolor("none")  # Sin fondo en el área de los ejes
    fig.patch.set_alpha(0)    # Sin fondo en la figura completa

    st.markdown(f'<p class="custom-subheader-plot">Consum i Temperatura per {group_by}</p>', unsafe_allow_html=True)
    st.pyplot(fig)

# Define the common plot function outside dynamic_grouping_plot
def plot_common(data, col1, col2, year=None, month=None, group_by='Mes'):
    # Plot 1: Accumulated Consumption per Use (First Column)
    with col1:
        st.markdown('<p class="custom-subheader-plot">Consum acomulat per ús</p>', unsafe_allow_html=True)
        plot_accumulated_consumption_per_use(data, year=year, month=month)

    # Plot 2: Accumulated Consumption per District (Second Column)
    with col2:
        st.markdown('<p class="custom-subheader-plot">Consum acomulat per districte</p>', unsafe_allow_html=True)
        plot_accumulated_consumption_per_district(data, year=year, month=month)

    # Plot 3: Accumulated Consumption per Use, per District
    st.markdown('<p class="custom-subheader-plot">Consum acomulat per ús i districte</p>', unsafe_allow_html=True)
    plot_accumulated_consumption_per_use_and_district(data, year=year, month=month)

    # Plot by consumption, precipitation, and temperature based on grouping
    plot_consumption_vs_accommodations(data, group_by=group_by, year=year, month=month)
    plot_consumption_vs_precipitation(data, group_by=group_by, year=year, month=month)
    plot_consumption_vs_temperature(data, group_by=group_by, year=year, month=month)