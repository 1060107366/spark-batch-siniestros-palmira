from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

spark = SparkSession.builder \
    .appName("BatchSiniestrosPalmira") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

file_path = "Siniestros_Viales_Palmira.csv" 
df = spark.read.csv(file_path, header=True, inferSchema=True, sep=",")

print("\n--- 1. ESQUEMA DE LOS DATOS (Nombres de columnas) ---")
df.printSchema()

print(f"\n--- 2. Total de registros originales: {df.count()} ---")

df_clean = df.withColumnRenamed("CLASE SINIESTRO", "Tipo_Siniestro") \
             .withColumnRenamed("LESIONADOS Y MUERTOS", "Gravedad")

print("\n--- 3. Análisis: Top Tipos de Siniestros ---")
top_clases = df_clean.groupBy("Tipo_Siniestro").agg(count("*").alias("Cantidad")).orderBy(desc("Cantidad"))
top_clases.show(10, truncate=False)

print("\n--- 4. Distribución por Gravedad ---")
top_gravedad = df_clean.groupBy("Gravedad").agg(count("*").alias("Cantidad")).orderBy(desc("Cantidad"))
top_gravedad.show(5, truncate=False)

pd_top_clases = top_clases.limit(10).toPandas()

plt.figure(figsize=(10, 6))
sns.barplot(x="Cantidad", y="Tipo_Siniestro", data=pd_top_clases, palette="viridis")
plt.title("Top 10 Tipos de Siniestros Viales en Palmira")
plt.xlabel("Número de Casos")
plt.ylabel("Tipo de Siniestro")
plt.tight_layout()

output_path = "grafica_siniestros.png"
plt.savefig(output_path)
print(f"\n✅ Gráfica guardada exitosamente en: {output_path}")

spark.stop()