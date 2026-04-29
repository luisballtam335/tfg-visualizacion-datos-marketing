import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

print('Librerías cargadas correctamente')

#Autenticación con cuenta de servicio de Google
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
gc = gspread.authorize(creds)

print('Autenticación completada')

#Carga del CSV original
CSV_PATH = os.path.join(os.path.dirname(__file__), 'online_advertising_performance_data.csv')
df_raw = pd.read_csv(CSV_PATH)

print(f'Extracción completada')
print(f'Filas extraídas: {len(df_raw):,}')
print(f'Timestamp de extracción: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

df = df_raw.copy()

#Eliminar columnas vacías
cols_vacias = [c for c in df.columns if df[c].isnull().all()]
df = df.drop(columns=cols_vacias)
print(f'Columnas vacías eliminadas: {cols_vacias}')

#Eliminar duplicados
before = len(df)
df = df.drop_duplicates()
print(f'Duplicados eliminados: {before - len(df)}')

#Imputar nulos en placement
df['placement'] = df['placement'].fillna('Unknown')
print(f'Nulos en placement imputados')

#Construir fecha
month_map = {
    'January':1,'February':2,'March':3,'April':4,
    'May':5,'June':6,'July':7,'August':8,
    'September':9,'October':10,'November':11,'December':12
}
df['month_num'] = df['month'].map(month_map)
df['Date'] = pd.to_datetime({
    'year': 2020,
    'month': df['month_num'],
    'day': df['day']
})
df['Week']      = df['Date'].dt.isocalendar().week.astype(int)
df['Weekday']   = df['Date'].dt.day_name()
df['Month_Num'] = df['Date'].dt.month

#Convertir Date a string para Google Sheets
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
print(f'Fecha construida')

#Métricas derivadas
df['CTR'] = np.where(df['displays'] > 0,
    (df['clicks'] / df['displays'] * 100).round(4), 0)
df['CPC'] = np.where(df['clicks'] > 0,
    (df['cost'] / df['clicks']).round(4), 0)
df['CPM'] = np.where(df['displays'] > 0,
    (df['cost'] / df['displays'] * 1000).round(4), 0)
df['Conv_Rate'] = np.where(df['clicks'] > 0,
    (df['post_click_conversions'] / df['clicks'] * 100).round(4), 0)
df['Revenue_per_Conv'] = np.where(df['post_click_conversions'] > 0,
    (df['revenue'] / df['post_click_conversions']).round(4), 0)
df['ROAS'] = np.where(df['cost'] > 0,
    (df['revenue'] / df['cost']).round(4), 0)
print(f'Métricas derivadas calculadas')

#Añadir timestamp de última actualización
df['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(f'\nTransformación completada')
print(f'Shape final: {df.shape}')
print(f'Nulos restantes: {df.isnull().sum().sum()}')

#Configuración
NOMBRE_HOJA = 'online_advertising_clean3'

#Abrir la hoja de Google Sheets
spreadsheet = gc.open(NOMBRE_HOJA)
worksheet = spreadsheet.sheet1

print(f'Hoja conectada: {NOMBRE_HOJA}')
print(f'Filas actuales en la hoja: {len(worksheet.get_all_values())}')

#Separar columnas numéricas y no numéricas
cols_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
cols_texto = df.select_dtypes(exclude=[np.number]).columns.tolist()

#Convertir solo las columnas de texto a string
df_export = df.copy()
for col in cols_texto:
    df_export[col] = df_export[col].astype(str)

#Construir la lista de datos
data = [df_export.columns.tolist()] + df_export.values.tolist()

#Limpiar y cargar
worksheet.clear()
worksheet.update(data, value_input_option='USER_ENTERED')

print(f'Carga completada')
print(f'Filas cargadas: {len(df_export):,}')

#Verificación post-carga
filas_en_sheets = len(worksheet.get_all_values()) - 1
filas_en_df = len(df)

print('VERIFICACIÓN POST-CARGA')
print(f'Filas en el dataframe:   {filas_en_df:,}')
print(f'Filas en Google Sheets:  {filas_en_sheets:,}')

if filas_en_sheets == filas_en_df:
    print('Carga verificada correctamente — los datos coinciden ✓')
else:
    print('Error — el número de filas no coincide ✗')
