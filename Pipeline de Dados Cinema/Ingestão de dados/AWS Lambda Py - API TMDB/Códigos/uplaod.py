import boto3
from tmdbv3api import TMDb, Movie, Find
from datetime import datetime
import json
import sys
import os  

tmdb = TMDb()
tmdb.api_key = os.getenv('TMDB_API_KEY')  
movie = Movie()
find = Find()

bucket_name = 'data-lake-do-lucas'
s3 = boto3.client('s3')

def obter_dados_tmdb_por_imdb_id(imdb_id):
    print("Buscando dados para o ID IMDb:", imdb_id)
    
    resultados = find.find(imdb_id, external_source='imdb_id')
    
    if resultados.get("movie_results"):
        print("Dados encontrados com sucesso!")
        dados = resultados['movie_results'][0]
        
        
        detalhes_filme = {
            "id": dados['id'],
            "title": dados['title'],
            "overview": dados['overview'],
            "genres": [genre['name'] for genre in dados.get('genres', [])],
            "release_date": dados.get('release_date'),
            "runtime": dados.get('runtime'),
            "vote_average": dados.get('vote_average'),
            "vote_count": dados.get('vote_count'),
            "original_language": dados.get('original_language'),
            "poster_path": dados.get('poster_path'),
            "cast": [] 
        }
        
        
        movie_details = movie.details(dados['id'])
        if 'cast' in movie_details:
            detalhes_filme['cast'] = [
                {"name": member['name'], "character": member['character']}
                for member in movie_details['cast'][:5]  # Limitar a 5 membros principais
            ]
        
        return detalhes_filme
    else:
        print("Erro: Nenhum resultado encontrado para o ID IMDb fornecido.")
        return None

def salvar_json_no_s3(dados, imdb_id):
    try:
        print("Preparando dados para salvar no S3...")
        
        json_data = json.dumps(dados)
        json_size = sys.getsizeof(json_data)
        
        if json_size > 10 * 1024 * 1024:
            print("Erro: O arquivo JSON excede 10 MB e não será salvo.")
            return
        
        today = datetime.today()
        ano, mes, dia = today.year, f"{today.month:02d}", f"{today.day:02d}"
        s3_key = f"Raw/Local/TMDB/JSON/{ano}/{mes}/{dia}/{imdb_id}.json"
        
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json_data,  
            ContentType='application/json'
        )
        print(f"Sucesso: Arquivo {s3_key} salvo com sucesso no S3.")
    except Exception as e:
        print(f"Erro ao salvar no S3: {e}")

def lambda_handler(event, context):
    imdb_id = event.get('imdb_id', 'tt3474994')  
    dados_filme = obter_dados_tmdb_por_imdb_id(imdb_id)

    if dados_filme:
        salvar_json_no_s3(dados_filme, imdb_id)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Dados salvos com sucesso!'})
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Erro ao obter dados'})
        }
