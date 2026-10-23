# Guía de Ejecución Paso a Paso (Entorno VirtualBox)

Este documento detalla el proceso de instalación, configuración y ejecución del entorno para el procesamiento batch de los siniestros viales.

## 1. Preparación del Dataset
1. Descargar el conjunto de datos en formato CSV desde Datos Abiertos.
2. Revisar su ubicación y transferirlo a la máquina virtual (VM) utilizando WinSCP.
3. Asegurarse de que el archivo esté en la carpeta personal (`/home/vboxuser/`) verificando con:
   ```bash
   ls -lh ~/Siniestros_Viales_Palmira_20261022*

##2. Instalación de Librerías

Instalar las librerías de Python necesarias para la visualización de datos:

bash
python3 -m pip install --user matplotlib seaborn pandas

##3. Creación del Script batch_siniestros.py
Se creó el script en el directorio /opt/kafka/ utilizando el editor nano:

bash
nano /opt/kafka/batch_siniestros.py

Nota importante sobre las columnas: Durante el desarrollo, se detectó que el dataset original contiene nombres de columnas con espacios (ej. CLASE SINIESTRO, LESIONADOS Y MUERTOS). Por lo tanto, el script final realiza un renombrado de columnas (withColumnRenamed) para facilitar el procesamiento.

Código final implementado:

python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc
import matplotlib
matplotlib.use('Agg') # Para guardar imágenes sin interfaz gráfica
import matplotlib.pyplot as plt
import seaborn as sns

## 1. Iniciar la sesión de Spark
spark = SparkSession.builder \
    .appName("BatchSiniestrosPalmira") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

## 2. Cargar el dataset
file_path = "/home/vboxuser/Siniestros_Viales_Palmira_20261022.csv" 
df = spark.read.csv(file_path, header=True, inferSchema=True, sep=",")

print("\n--- 1. ESQUEMA DE LOS DATOS ---")
df.printSchema()

print(f"\n--- 2. Total de registros originales: {df.count()} ---")

## 3. Limpieza y renombrado (Crucial para evitar errores)
df_clean = df.withColumnRenamed("CLASE SINIESTRO", "Tipo_Siniestro") \
             .withColumnRenamed("LESIONADOS Y MUERTOS", "Gravedad")

## 4. Análisis Exploratorio (EDA)
print("\n--- 3. Análisis: Top Tipos de Siniestros ---")
top_clases = df_clean.groupBy("Tipo_Siniestro").agg(count("*").alias("Cantidad")).orderBy(desc("Cantidad"))
top_clases.show(10, truncate=False)

print("\n--- 4. Distribución por Gravedad ---")
top_gravedad = df_clean.groupBy("Gravedad").agg(count("*").alias("Cantidad")).orderBy(desc("Cantidad"))
top_gravedad.show(5, truncate=False)

## 5. Visualización
pd_top_clases = top_clases.limit(10).toPandas()

plt.figure(figsize=(10, 6))
sns.barplot(x="Cantidad", y="Tipo_Siniestro", data=pd_top_clases, palette="viridis")
plt.title("Top 10 Tipos de Siniestros Viales en Palmira")
plt.xlabel("Número de Casos")
plt.ylabel("Tipo de Siniestro")
plt.tight_layout()

output_path = "/home/vboxuser/grafica_siniestros.png"
plt.savefig(output_path)
print(f"\n✅ Gráfica guardada exitosamente en: {output_path}")

spark.stop()


4. Ejecución del Script
Para ejecutar el script asegurando que Spark use el Python de usuario (donde se instalaron las librerías), se ejecutó el siguiente comando:

bash
PYSPARK_PYTHON=python3 /opt/spark/bin/spark-submit batch_siniestros.py
