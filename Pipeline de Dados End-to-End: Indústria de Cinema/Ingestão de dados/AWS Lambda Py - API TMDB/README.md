# AWS Lambda Py - API TMDB

## **Objetivo** 
 
 O objetivo é usar AWS Lambda para capturar dados da API TMDB e armazená-los no Amazon S3 em formato JSON. Os dados devem complementar os já existentes na Etapa 1 sem modificar os arquivos originais. O código deve ser organizado no Git, com documentação detalhada em Markdown, incluindo explicações sobre o uso da API e a estrutura dos dados. A ingestão deve ser automatizada com Amazon EventBridge ou CloudWatch, e as boas práticas de segurança, como não armazenar tokens no código, devem ser seguidas.
 
## 1. Etapa

### 1.1 Criando a Layer no AWS Lambda

Para usar bibliotecas externas como `tmdbv3api` e `boto3` no AWS Lambda, é necessário criar uma camada (Layer). Siga os passos abaixo para criar a layer e implementá-la na função Lambda.

#### Passo 1: Instalar as Bibliotecas Localmente

Primeiro, crie um diretório para as bibliotecas e instale as dependências necessárias:
```bash
mkdir python
pip install tmdbv3api -t python/
```

#### Passo 2: Criar o Arquivo ZIP

```bash
zip -r python.zip python
```

#### Passo 3: Carregar a Camada no AWS Lambda

Para carregar a camada no AWS Lambda, siga os seguintes passos:

1. No console do AWS Lambda, vá para a seção **Layers** e clique em **Create layer**.
2. Preencha as informações da camada:
   - **Nome**: Defina um nome para a camada (por exemplo: `tmdb-layer`).
   - **Descrição**: Opcional, mas adicione uma descrição (por exemplo: `Camada com as libs TMDB e boto3`).
   - **Arquivo .zip**: Faça o upload do arquivo `lambda_layer.zip` que você criou.
   - **Compatibilidade**: Selecione a versão do Python que você está usando no Lambda (por exemplo, Python 3.11).

![subindo a camada para o Lambda](../evidencias/Camada.png)

Isso criará a camada, que poderá ser adicionada às funções Lambda conforme necessário.

#### Passo 4: Configurando a Variável de Ambiente para Usar a API do TMDB

Para garantir segurança no código, definimos a chave da API como uma variável de ambiente no AWS Lambda, com o nome `TMDB_API_KEY`, conforme mostrado na imagem a seguir:

![Definindo a variável de ambiente da chave da API](../evidencias/variavel.png)


## 2. Etapa

### 2.1 Executando o Código no Lambda

Nesta etapa, vamos executar o código no Lambda para testar sua funcionalidade e garantir sua eficácia. O código abaixo mostra como buscar dados do TMDB usando a API, processá-los e armazená-los em um bucket do Amazon S3.

#### Bloco 1: Importação das Bibliotecas

 - Primeiro, importamos as bibliotecas necessárias para interagir com o TMDB, Amazon S3 e manipulação de dados.

```python
import boto3
from tmdbv3api import TMDb, Movie, Find
from datetime import datetime
import json
import sys
import os
``` 

**Explicação:**
- **boto3**: Usado para acessar e manipular objetos no Amazon S3.
- **tmdbv3api**: Biblioteca que facilita a interação com a API do TMDB.
- **datetime**: Para trabalhar com datas e gerar nomes baseados no tempo.
- **json, sys, os**: Utilizados para manipulação de dados, verificar tamanhos e acessar variáveis de ambiente.


#### Bloco 2: Configuração do TMDb e Inicialização do S3

 - Aqui configuramos a chave da API do TMDB e inicializamos o cliente do S3.

 ```python
tmdb = TMDb()
tmdb.api_key = os.getenv('TMDB_API_KEY') 
movie = Movie()
find = Find()
bucket_name = 'data-lake-do-lucas'
s3 = boto3.client('s3')
```

**Explicação:**
- **API do TMDB**: A chave da API é obtida de uma variável de ambiente para garantir a segurança.
- **Objetos TMDB**: Inicializa os objetos `Movie` e `Find` para interagir com a API TMDB.
- **S3**: Configura o cliente do S3 para permitir o upload de dados no bucket especificado.

#### Bloco 3: Função para Obter Dados do TMDB por IMDb ID

 - Esta função busca dados sobre um filme com base no ID do IMDb fornecido.

 ```python
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
                for member in movie_details['cast'][:5]  
            ]
        
        return detalhes_filme
    else:
        print("Erro: Nenhum resultado encontrado para o ID IMDb fornecido.")
        return None
 ```

**Explicação:**
- **Busca no TMDB**: A função usa o `IMDb ID` para procurar dados sobre o filme no TMDB.
- **Detalhes do filme**: Retorna informações como título, gênero, data de lançamento, duração, média de votos e mais.
- **Elenco**: Limita a lista de atores a cinco membros principais.
- **Retorno**: Se encontrado, retorna os dados do filme; caso contrário, retorna `None`.

#### Bloco 4: Função para Salvar os Dados no S3

  - Aqui, salvamos os dados obtidos em um arquivo JSON no Amazon S3.

 ```python
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
 ```
**Explicação:**
- **`json.dumps(dados)`**: Converte os dados para o formato JSON.
- **`sys.getsizeof(json_data)`**: Verifica o tamanho do arquivo JSON.
- **Tamanho de 10MB**: Se o arquivo exceder 10MB, ele não será salvo.
- **Salvamento no S3**: O arquivo JSON é salvo no S3 com um caminho gerado com base na data atual.

 #### Bloco 5: Função Principal do Lambda

  - Esta é a função principal que será chamada pelo Lambda, onde o código é executado.

 ```python
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
 ```

**Explicação:**
- **`event.get('imdb_id')`**: Obtém o `imdb_id` do evento, com um valor padrão.
- **`obter_dados_tmdb_por_imdb_id(imdb_id)`**: Busca os dados do filme no TMDB.
- **`salvar_json_no_s3(dados_filme, imdb_id)`**: Salva os dados no S3.
- **Respostas**: Retorna status 200 (sucesso) ou 500 (erro) dependendo do resultado da operação.
 

 ## Código Completo

 - Agora que dividimos e explicamos cada bloco, aqui está o código completo:

```python
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
                for member in movie_details['cast'][:5]  
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
```

## 3. Etapa: Resultados das Consultas

Nesta etapa, apresentaremos os resultados das consultas realizadas para três filmes com base nos critérios definidos:

- **Melhor Filme de 2018**  
  **ID**: `tt8447664`  
  **Título**: *Kingsman*  
  **Nota Média**: 9.60  

  Busca e salvamento executados com sucesso: 

  ![Buscando os dados do ID](../evidencias/tt8447664.png)  
  ![Verificando o salvamento](../evidencias/sv-3.png)

- **Filme com Maior Nota Média**  
  **ID**: `tt0380452`  
  **Título**: *Isa lang ang dapat mahalin*  
  **Ano**: 1997  
  **Nota Média**: 10.00  

  Busca e salvamento executados com sucesso:

  ![Buscando os dados do ID](../evidencias/tt0380452.png)  
  ![Verificando o salvamento](../evidencias/sv-1.png)

- **Filmes em que Suzana Pires Aparece**  
  **ID**: `tt3474994`  
  **Título**: *Casa Grande*  

  Busca e salvamento executados com sucesso:  

  ![Buscando os dados do ID](../evidencias/tt3474994.png)  
  ![Verificando o salvamento](../evidencias/sv-2.png)

## Observação

Gostaria de destacar que as análises realizadas sobre os IDs dos filmes apresentados podem ser revisadas nas próximas etapas. Tenho a intenção de examinar mais detalhadamente os dois arquivos CSV e identificar pontos adicionais que possam ser mais relevantes para focar e comparar com os dados já obtidos.

O código utilizado para realizar as consultas no Lambda está localizado na pasta Codigos, que faz parte da estrutura do projeto. Dentro dessa pasta, também está o arquivo python.zip, que contém as bibliotecas necessárias para a execução do código. Esse arquivo foi criado e configurado para garantir que todas as dependências, como a API do TMDb, sejam corretamente carregadas durante a execução no Lambda.
A estrutura da pasta Codigos e a presença do arquivo python.zip são essenciais para o funcionamento adequado do projeto no ambiente Lambda, permitindo a execução automatizada e eficiente das consultas e o processamento dos dados.

# Conclusão

Nesta etapa, conseguimos integrar dados da API do TMDb e realizar consultas detalhadas sobre filmes específicos. As consultas foram bem-sucedidas, e os dados foram processados e salvos corretamente no Amazon S3. Além disso, conseguimos identificar filmes com as maiores notas médias e buscar informações específicas sobre a participação de atores.
Embora os resultados apresentados sejam baseados em dados iniciais, a análise ainda está em andamento. Nas próximas etapas, pretendo aprofundar a análise dos dados e buscar novas comparações e insights, com o objetivo de tornar as consultas mais completas e relevantes.
A integração com o TMDb e o uso do S3 proporcionaram uma forma eficiente de armazenar e gerenciar as informações, o que contribui para o sucesso da execução até o momento.
