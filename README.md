# TFG — Visualización de Datos y Storytelling Digital

Trabajo de Fin de Grado del Grado en Ciencia de Datos, Universidad Europea de Valencia. Curso académico 2025-2026.

**Autor:** Luis Ballester Tamarit  
**Tutor:** Vicente Castillo Fauli

---

## Descripción

Este repositorio contiene el código desarrollado para la parte práctica del TFG, cuyo objetivo es el diseño de dashboards interactivos y la automatización de un pipeline ETL aplicado a un dataset de publicidad digital del segundo trimestre de 2020.

---

## Dataset

El dataset utilizado es el *Online Advertising Digital Marketing Data*, disponible públicamente en Kaggle:  
https://www.kaggle.com/datasets/naniruddhan/online-advertising-digital-marketing-data

---

## Requisitos

Para ejecutar los notebooks es necesario tener instaladas las siguientes librerías de Python:

pip install pandas numpy matplotlib seaborn gspread google-auth google-auth-oauthlib schedule

---

## Contenido de los archivos de código

**exploracion_analisis_calidad.ipynb**  
Exploración inicial del dataset: estructura, tipos de datos, estadísticas descriptivas, análisis de valores nulos, duplicados y outliers, y análisis de variación entre grupos.

**trasnformacion_etl_automatizacion_periodica_tfg.py**  
Limpieza del dataset, construcción de la columna de fecha, cálculo de métricas derivadas (CTR, CPC, CPM, Conv_Rate, Revenue_per_Conv, ROAS) y automatización del pipeline ETL con carga automática en Google Sheets mediante la API de Google.

**ejecutor_periodico.py**  
Scheduler de ejecución automática del pipeline ETL. Ejecuta `etl_pipeline.py` cada 15 minutos de forma automática mientras esté en ejecución, sincronizándose con el intervalo mínimo de actualización de Looker Studio desde Google Sheets.

---

## Ejecución automática del pipeline

Para lanzar el pipeline ETL de forma automática cada 15 minutos, ejecuta el siguiente comando y mantén la ventana abierta:

python ejecutor_periodico.py

La primera ejecución abrirá el navegador para autorizar el acceso a Google Sheets mediante OAuth. Las siguientes ejecuciones serán completamente automáticas.

---

## Dashboards

Los dashboards interactivos desarrollados están disponibles en los siguientes enlaces:

- **Looker Studio:** https://lookerstudio.google.com/reporting15ebed93-556a-48ab-9f1c-10c25111f182 
- **Power BI:** https://drive.google.com/file/d/1qykUm2SAPtDHj_5-WXIVU4b49nVDvdJQ/view?usp=sharing

---

## Referencia

Ruddhan, N. (2020). *Online Advertising Digital Marketing Data* [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/naniruddhan/online-advertising-digital-marketing-data