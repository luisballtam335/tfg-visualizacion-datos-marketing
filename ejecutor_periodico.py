import schedule
import time
import subprocess
import os
from datetime import datetime

#Ruta al script ETL
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 
              'trasnformacion_etl_automatizacion_periodica_tfg.py')

def ejecutar_pipeline():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando pipeline ETL...")
    resultado = subprocess.run(
        ['python', SCRIPT_PATH], 
        capture_output=True, 
        text=True
    )
    if resultado.returncode == 0:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Pipeline completado")
        print(resultado.stdout)
    else:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error en el pipeline:")
        print(resultado.stderr)

#Para programar ejecución diaria 
#schedule.every().day.at("11:55").do(ejecutar_pipeline)

#Para poder programarlo cada 15 minutos y que esté en paralelo con la actualización mínima de Looker:
schedule.every(15).minutes.do(ejecutar_pipeline)

print(f"Ejecutor iniciado.")
print(f"Próxima ejecución: {schedule.next_run()}")
print(f"El pipeline se ejecutará cada 15 minutos.")
print(f"Mantén esta ventana abierta para que el scheduler funcione.")

while True:
    schedule.run_pending()
    time.sleep(60)