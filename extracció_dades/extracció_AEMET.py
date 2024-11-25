import requests
import pandas as pd
from datetime import datetime, timedelta

# Col·loca la teva clau API aquí (després de registrar-te a AEMET OpenData)
API_KEY = ""

# Definir els codis de les estacions de Barcelona
ESTACIONES = {
    "Barcelona El Prat": "0076",
    "Barcelona Drassanes": "0201X",
    "Barcelona, Port Olímpic": "0201D"
}

# Calcular les dates per l'últim mes
hoy = datetime.now()
primer_dia_mes_anterior = (hoy.replace(day=1) - timedelta(days=1)).replace(day=1)
ultimo_dia_mes_anterior = primer_dia_mes_anterior.replace(month=primer_dia_mes_anterior.month % 12 + 1) - timedelta(days=1)

# Funció per obtenir les dades d'una estació i període de temps
def obtener_datos(estacion_id, fecha_inicio, fecha_fin):
    # Donar format a les dates
    fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%dT00:00:00UTC")
    fecha_fin_str = fecha_fin.strftime("%Y-%m-%dT23:59:59UTC")

    # URL de la sol·licitud a l'API d'AEMET
    url = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_inicio_str}/fechafin/{fecha_fin_str}/estacion/{estacion_id}/?api_key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if 'datos' in data:
        # URL amb les dades reals
        datos_url = data['datos']
        datos_response = requests.get(datos_url)
        return datos_response.json()
    else:
        print(f"Error en obtenir les dades per a l'estació {estacion_id}: {data}")
        return []

# Funció principal per obtenir les dades de totes les estacions i guardar-les en un CSV
def generar_csv():
    # Inicialitzar una llista per emmagatzemar les dades de totes les estacions
    registros = []

    # Processar les dades per a cada estació
    for nombre_estacion, estacion_id in ESTACIONES.items():
        print(f"Obtenint dades de {nombre_estacion} des de {primer_dia_mes_anterior} fins a {ultimo_dia_mes_anterior}...")
        datos = obtener_datos(estacion_id, primer_dia_mes_anterior, ultimo_dia_mes_anterior)

        # Extreure les dades rellevants (temperatura i precipitació)
        for entry in datos:
            fecha = entry.get('fecha')
            temp_max = entry.get('tmax', None)
            temp_min = entry.get('tmin', None)
            precipitacion = entry.get('prec', None)

            # Afegir les dades al registre
            registros.append({
                'estacion': nombre_estacion,
                'fecha': fecha,
                'temp_max': temp_max,
                'temp_min': temp_min,
                'precipitacion': precipitacion
            })

    # Convertir els registres en un DataFrame de pandas
    df = pd.DataFrame(registros)

    # Convertir la columna de dates al format datetime
    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

    # Guardar les dades en un fitxer CSV
    df.to_csv('barcelona_temperatura_precipitacion_ultimo_mes.csv', index=False)
    print("Dades guardades a 'barcelona_temperatura_precipitacion_ultimo_mes.csv'")

# Executar la funció per generar el CSV
generar_csv()
