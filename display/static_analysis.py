import streamlit as st
from styles import inject_custom_css
from static_graphs import plot_common

# Define the dynamic_grouping_plot function
def dynamic_grouping_plot(data, census):
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
        # Determine the appropriate plot grouping based on user selection
        if year_selection == 'Tots els anys':
            plot_common(data, census, group_by='Mes')  # Grouping by month across all years
        elif month_selection == 'Tots els mesos':
            plot_common(data, census, year=year_selection, group_by='Setmana')  # Grouping by week for selected year
        elif month_selection:
            month_number = {'Gener': 1, 'Febrer': 2, 'Març': 3, 'Abril': 4, 'Maig': 5, 'Juny': 6, 'Juliol': 7, 'Agost': 8, 'Setembre': 9, 'Octubre': 10, 'Novembre': 11, 'Desembre': 12}
            plot_common(data, census, year=year_selection, month=month_number[month_selection], group_by='Dia')  # Grouping by day for selected year and month
        else:
            st.warning("Please make valid selections to generate the plots.")

            


def graph_display(data, census):
    # Inject custom CSS (if needed)
    inject_custom_css()

    col1, _, col2 = st.columns([3,1,1])

    with col1:
        st.image("media/header1.png", width=600)
    
    with col2:
        st.image("media/header2.png", width = 240)

    st.image("media/estudi_estàtic.png")

    dynamic_grouping_plot(data, census)