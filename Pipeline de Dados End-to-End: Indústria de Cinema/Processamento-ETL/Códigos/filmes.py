from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date, dayofmonth, month, year

spark = SparkSession.builder.appName("CSV_to_Parquet_Cleaned").getOrCreate()

caminho_csv = "s3://data-lake-do-lucas/Raw/Local/CSV/Movies/2024/10/23/movies.csv"
cmBuckte = "s3://data-lake-do-lucas/TRUSTED/"

df = spark.read.option("header", "true") \
    .option("delimiter", "|") \
    .option("inferSchema", "true") \
    .csv(caminho_csv)

df_limpo = df.dropna().dropDuplicates()

df_limpo = df_limpo \
    .withColumn("anoLancamento", col("anoLancamento").cast("int")) \
    .withColumn("tempoMinutos", col("tempoMinutos").cast("int")) \
    .withColumn("notaMedia", col("notaMedia").cast("double")) \
    .withColumn("numeroVotos", col("numeroVotos").cast("int")) \
    .withColumn("anoNascimento", col("anoNascimento").cast("int")) \
    .withColumn("anoFalecimento", col("anoFalecimento").cast("int"))

df_limpo = df_limpo \
    .withColumn("ano", year(current_date())) \
    .withColumn("mes", month(current_date())) \
    .withColumn("dia", dayofmonth(current_date()))

sdBuckte = f"{cmBuckte}Movies/{df_limpo.select('ano').first()['ano']}/{df_limpo.select('mes').first()['mes']}/{df_limpo.select('dia').first()['dia']}/"

df_limpo.write.parquet(sdBuckte, mode="overwrite")

spark.stop()

print("Arquivos CSV processados e salvos com sucesso na Trusted Zone!")
