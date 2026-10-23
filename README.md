# Análisis Batch de Siniestros Viales en Palmira con Apache Spark

##  Descripción del Proyecto
Este proyecto implementa una solución de **procesamiento en batch** utilizando **Apache Spark (PySpark)** para analizar el conjunto de datos abierto de *Siniestros Viales en Palmira*, disponible en Datos Abiertos Colombia.

El script realiza las siguientes tareas:
1. Carga del dataset desde un archivo CSV.
2. Limpieza y transformación de datos (renombrado de columnas con espacios).
3. Análisis Exploratorio de Datos (EDA) para identificar los tipos de siniestros más comunes y su gravedad.
4. Generación de una visualización gráfica (gráfico de barras) guardada como imagen.

##  Tecnologías Utilizadas
*   **Apache Spark 3.5.x** (PySpark)
*   **Python 3.10+**
*   **Pandas** (para manipulación previa a la gráfica)
*   **Matplotlib / Seaborn** (para la visualización)
*   **Java 17** (Requisito para Spark)

##  Dataset
*   **Fuente:** [Datos Abiertos Colombia - Siniestros Viales Palmira](https://www.datos.gov.co/Transporte/Siniestros-Viales-Palmira/sjpx-eqfp/about_data)
*   **Formato:** CSV (descargado de la API).
*   **Nota:** El archivo CSV (`Siniestros_Viales_Palmira.csv`) está incluido en el repositorio ya es decisión por temas de tamaño. Debes descargarlo y colocarlo en la raíz del proyecto.

##  Requisitos Previos e Instalación

1. Tener instalado **Java 17** (`java -version`).
2. Tener instalado **Apache Spark** y configurada la variable de entorno `SPARK_HOME`.
3. Instalar las dependencias de Python ejecutando:
   ```bash
   pip install -r requirements.txt
