from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when, array, current_date, dayofmonth, month, year
from pyspark.sql.types import ArrayType, StringType
import os


spark = SparkSession.builder.appName("JSON_to_Parquet").getOrCreate()

caminho_csv = "s3://data-lake-do-lucas/Raw/Local/TMDB/JSON/2024/11/04/"

cmBuckte = "s3://data-lake-do-lucas/TRUSTED/"

df = spark.read.json(caminho_csv)

df_clean = df \
    .withColumn("release_date", when(col("release_date") == "", None).otherwise(col("release_date"))) \
    .withColumn("release_date", to_date(col("release_date"), "yyyy-MM-dd")) \
    .withColumn("runtime", when(col("runtime").isNull(), 0).otherwise(col("runtime"))) \
    .withColumn("genres", when(col("genres").isNull(), array()).otherwise(col("genres"))) \
    .withColumn("cast", when(col("cast").isNull(), array()).otherwise(col("cast")))

df_clean = df_clean \
    .withColumn("ano", year(current_date())) \
    .withColumn("mes", month(current_date())) \
    .withColumn("dia", dayofmonth(current_date()))

df_clean = df_clean.dropna(subset=["id", "title", "overview"])

output_dir = f"{cmBuckte}TMDB/{df_clean.select('ano').first()['ano']}/{df_clean.select('mes').first()['mes']}/{df_clean.select('dia').first()['dia']}/"

df_clean.write.parquet(output_dir, mode="overwrite")

spark.stop()

print("Arquivos JSON processados e salvos com sucesso na Trusted Zone!")
