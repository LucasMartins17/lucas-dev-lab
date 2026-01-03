import boto3
import os
from datetime import datetime

BUCKET_NAME = 'testedesafio' 
RAW_ZONE_PATH = 'Raw/Local/CSV'
PROFILE_NAME = 'Lucas-Martins-Elias-de-Oliveira'  

def upload_csv(arquivo, tipo):
    
    if not os.path.exists(arquivo):
        print(f"Erro: o arquivo {arquivo} não foi encontrado.")
        return
    
    session = boto3.Session(profile_name=PROFILE_NAME)
    s3 = session.client('s3')
    
    today = datetime.today()
    s3_key = f"{RAW_ZONE_PATH}/{tipo}/{today.year}/{today.month:02d}/{today.day:02d}/{os.path.basename(arquivo)}"
    
    try:

        s3.upload_file(arquivo, BUCKET_NAME, s3_key)
        print(f"Upload bem-sucedido: {s3_key}")
    except Exception as e:
        print(f"Erro ao fazer upload: {str(e)}")

if __name__ == "__main__":
    filmes = 'movies.csv'  
    series = 'series.csv'  
    

    upload_csv(filmes, 'Movies')  
    upload_csv(series, 'Series')  
