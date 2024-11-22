import requests
import pandas as pd
from datetime import datetime, timedelta

"""
Aquest és el codi utlitzat per treure les dades meteorològiques i de precipitació del últims 3 anys utilitzades pel nostre projecte.
El codi utilitza la API d'AEMET per extreure les dades. La gràcia d'aquesta API és que permet treure informació a temps real.
L'API no permet extreure informació d'un període més gran que 6 mesos, és per això que hem decidit dividir en períodes de 4 mesos, per poder
extreure tota la informació del últims 3 anys.

També hem aplicat una funció per tractar els possibles errors de les estacions meteorològiques d'AEMET. Algunes vegades, hi ha alguna dada buida,
ja que el sensor pot haver fallat. Per arreglar aquestes situacions, hem decidit obtar per omplir aquests buits, assignant el valor més proper. (que
en la gran majoria de casos és el dia anterior o posterior)
"""

# Col·loca la teva API key aquí (després de registrar-te a AEMET OpenData)
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYXJ0aS5vbXMwMUBlc3R1ZGlhbnQudXBmLmVkdSIsImp0aSI6ImFiN2Q1MWI4LWIwYjAtNDg3OS04NzdhLTYwMWIyMWIxMmQyNyIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzI5NTE4OTUxLCJ1c2VySWQiOiJhYjdkNTFiOC1iMGIwLTQ4NzktODc3YS02MDFiMjFiMTJkMjciLCJyb2xlIjoiIn0.ecFODP9Cq360LTcvM2lHSBlIs9Gre54YKsd4aMS61-M"

# Definir els codis de les estacions de Barcelona
ESTACIONES = {
    "Barcelona El Prat": "0076",
    "Barcelona Drassanes": "0201X",
    "Barcelona, Port Olímpic": "0201D"
}

# Dates inicial i final
fecha_inicio = datetime(2021, 1, 1)
fecha_fin = datetime(2023, 12, 31)

# Funció per dividir el rang de dates en períodes de 4 mesos
def obtenir_periodes(fecha_inicio, fecha_fin, mesos=4):
    periodes = []
    while fecha_inicio < fecha_fin:
        periode_fi = fecha_inicio + timedelta(days=mesos*30)  # Aproximadament 4 mesos
        if periode_fi > fecha_fin:
            periode_fi = fecha_fin
        periodes.append((fecha_inicio, periode_fi))
        fecha_inicio = periode_fi + timedelta(days=1)
    return periodes

# Funció per obtenir les dades d'una estació i període de temps
def obtenir_dades(estacio_id, fecha_inicio, fecha_fin):
    # Formatjar dates
    fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%dT00:00:00UTC")
    fecha_fin_str = fecha_fin.strftime("%Y-%m-%dT23:59:59UTC")

    # URL de la sol·licitud a l'API d'AEMET
    url = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_inicio_str}/fechafin/{fecha_fin_str}/estacion/{estacio_id}/?api_key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if 'datos' in data:
        # URL amb les dades reals
        dades_url = data['datos']
        dades_response = requests.get(dades_url)
        return dades_response.json()
    else:
        print(f"Error en obtenir les dades per a l'estació {estacio_id}: {data}")
        return []

def emplenar_mes_proper(series):
    series = series.str.replace(',', '.', regex=False)
    # Convertir valors no numèrics a NaN
    series = pd.to_numeric(series, errors='coerce')
    # Emplenar NaN utilitzant els valors vàlids més propers
    return series.interpolate(method='nearest', limit_direction='both')

# Funció principal per obtenir les dades de totes les estacions i guardar-les en un CSV
def generar_csv():
    # Inicialitzar una llista per emmagatzemar les dades de totes les estacions
    registres = []

    # Obtenir els períodes de 4 mesos
    periodes = obtenir_periodes(fecha_inicio, fecha_fin)

    # Processar les dades per a cada estació i període
    for nom_estacio, estacio_id in ESTACIONES.items():
        for periode in periodes:
            inici, fi = periode
            print(f"Obtenint dades de {nom_estacio} des de {inici} fins a {fi}...")
            dades = obtenir_dades(estacio_id, inici, fi)

            # Extreure les dades rellevants (temperatura i precipitació)
            for entry in dades:
                fecha = entry.get('fecha')
                temp_max = entry.get('tmax', None)
                temp_min = entry.get('tmin', None)
                precipitacio = entry.get('prec', None)

                # Afegir les dades al registre
                registres.append({
                    'estacio': nom_estacio,
                    'fecha': fecha,
                    'temp_max': temp_max,
                    'temp_min': temp_min,
                    'precipitacion': precipitacio
                })

    # Convertir els registres en un DataFrame de pandas
    df = pd.DataFrame(registres)

    # Convertir la columna de dates al format datetime
    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

    # Aplicar la funció a cada columna objectiu
    for column in ['temp_max', 'temp_min', 'precipitacion']:
        df[column] = emplenar_mes_proper(df[column])

    return df

# Executar la funció per generar el df
df = generar_csv()

#Guardar el df en un CSV
df.to_csv('data/temperature_precipitation.csv', index=False)
print("Dades guardades a 'barcelona_temperatura_precipitacio_2021_2023.csv'")