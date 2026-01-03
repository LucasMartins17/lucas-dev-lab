from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date, dayofmonth, month, year, monotonically_increasing_id, hash

spark = SparkSession.builder.appName("Parquet_to_Refined").getOrCreate()

trusted_path = "s3://data-lake-do-lucas/TRUSTED/Movies/2024/11/21/"
refined_path = "s3://data-lake-do-lucas/REFINED/"

df_trusted = spark.read.parquet(trusted_path)

df_trusted = df_trusted.dropDuplicates()

df_trusted = df_trusted \
    .withColumn("anoLancamento", col("anoLancamento").cast("int")) \
    .withColumn("tempoMinutos", col("tempoMinutos").cast("int")) \
    .withColumn("notaMedia", col("notaMedia").cast("double")) \
    .withColumn("numeroVotos", col("numeroVotos").cast("int")) \
    .withColumn("anoNascimento", col("anoNascimento").cast("int")) \
    .withColumn("anoFalecimento", col("anoFalecimento").cast("int"))

df_trusted = df_trusted \
    .withColumn("ano", year(current_date())) \
    .withColumn("mes", month(current_date())) \
    .withColumn("dia", dayofmonth(current_date()))

refined_partition = f"{refined_path}Movies/{df_trusted.select('ano').first()['ano']}/{df_trusted.select('mes').first()['mes']}/{df_trusted.select('dia').first()['dia']}/"

# Dimensão: Títulos
dim_titulos = df_trusted.select("titulopincipal", "titulooriginal").distinct() \
    .withColumnRenamed("titulopincipal", "titulo_principal") \
    .withColumnRenamed("titulooriginal", "titulo_original") \
    .withColumn("id_titulo", monotonically_increasing_id())  
dim_titulos.write.parquet(f"{refined_partition}dim_titulos", mode="overwrite")

# Dimensão: Tempo
dim_tempo = df_trusted.select("ano", "mes", "dia").distinct().withColumn("id_tempo", monotonically_increasing_id())  
dim_tempo.write.parquet(f"{refined_partition}dim_tempo", mode="overwrite")

# Dimensão: Gênero
dim_genero = df_trusted.select("genero").distinct() \
    .withColumn("id_genero", hash("genero"))  
dim_genero.write.parquet(f"{refined_partition}dim_genero", mode="overwrite")

# Dimensão: Artista
dim_artista = df_trusted.select("nomeartista", "anonascimento", "anofalecimento", "profissao").distinct() \
    .withColumn("id_artista", hash("nomeartista", "anonascimento", "anofalecimento", "profissao"))  
dim_artista.write.parquet(f"{refined_partition}dim_artista", mode="overwrite")

# Dimensão: Personagem
dim_personagem = df_trusted.select("personagem", "generoartista").distinct() \
    .withColumn("id_personagem", hash("personagem", "generoartista"))  
dim_personagem.write.parquet(f"{refined_partition}dim_personagem", mode="overwrite")

# Tabela de Fato: Filmes
fato_filmes = df_trusted \
    .join(dim_tempo, on=["ano", "mes", "dia"], how="inner") \
    .join(dim_genero, on=["genero"], how="inner") \
    .join(dim_artista, on=["nomeartista"], how="inner") \
    .join(dim_personagem, on=["personagem", "generoartista"], how="inner") \
    .join(dim_titulos, (df_trusted["titulopincipal"] == dim_titulos["titulo_principal"]) & 
                      (df_trusted["titulooriginal"] == dim_titulos["titulo_original"]), how="inner") \
    .select(
        "id_tempo", "id_genero", "id_artista", "id_personagem", "id_titulo",  
        "anoLancamento", "tempoMinutos", "notaMedia", "numeroVotos"
    ) \
    .distinct()  

fato_filmes.write.parquet(f"{refined_partition}fato_filmes", mode="overwrite")

spark.stop()

print("Arquivos Parquet processados e salvos com sucesso na Refined Zone!")
