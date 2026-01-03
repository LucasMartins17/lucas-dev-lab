# Pipeline de Dados End-to-End: Indústria de Cinema

## **Objetivo**

Praticar a combinação de conhecimentos adquiridos no programa, com foco na construção de um Data Lake na AWS, realizando a ingestão de arquivos CSV e dados de API, utilizando tecnologias como boto3, Docker e o serviço Amazon S3. O objetivo principal desta etapa é carregar os dados localmente para o S3 na camada RAW Zone, como parte do processo de ingestão de dados para a primeira fase do Data Lake.

## 1. Etapa

### 1.1 Criação do Bucket no Amazon S3

Nesta etapa, foi criado o bucket **`data-lake-do-lucas`** no serviço **Amazon S3**. Esse bucket servirá como repositório central para os arquivos CSV que serão processados ao longo do desafio. Ele será utilizado para a ingestão de dados na **RAW Zone**, onde os dados brutos serão armazenados antes de qualquer processamento adicional. Esse bucket também será a base para as próximas etapas, como o processamento e análise dos dados nas futuras sprints.
As pastas dentro do bucket seguirão a estrutura recomendada, garantindo a correta organização e padronização dos dados, com a definição de subdiretórios que categorizam origem, formato, e data de processamento, permitindo fácil gerenciamento e rastreabilidade dos arquivos.

![Criando o bucket para o desafio](../evidencias/criandoBucket.png)

### 1.2 Exibindo o Bucket

Abaixo está uma imagem do bucket **`data-lake-do-lucas`** já criado, mas ainda sem nenhum arquivo armazenado. Esta captura foi feita para documentar a configuração inicial do bucket. Nas próximas etapas, este bucket será utilizado para demonstrar o funcionamento dos códigos desenvolvidos, conforme os dados forem sendo carregados e processados.

![Bucket antes da execucao dos codigos](../evidencias/bucketant.png)

## 2. Etapa

Nesta etapa, foi desenvolvido o código em Python responsável por realizar o upload dos arquivos CSV de filmes e séries para o bucket **`data-lake-do-lucas`** no Amazon S3. O código utiliza a biblioteca **boto3** para se conectar à AWS e gerenciar o upload dos arquivos, garantindo que eles sejam armazenados na estrutura correta dentro da **RAW Zone**.

### 2.1 Explicação do Código:

- A biblioteca **boto3** foi utilizada para interagir com o serviço Amazon S3.
- O script verifica se o arquivo existe localmente antes de tentar fazer o upload, evitando erros desnecessários.
- A variável **`BUCKET_NAME`** define o bucket onde os arquivos serão armazenados, e **`RAW_ZONE_PATH`** define o caminho de armazenamento dentro do bucket.
- O caminho no S3 segue o formato: `Raw/Local/CSV/<tipo>/<ano>/<mês>/<dia>/<arquivo>`, onde o tipo pode ser 'Movies' ou 'Series'.
- A função **`upload_csv`** recebe o arquivo CSV e o tipo (filmes ou séries), realiza o upload para o bucket, e em caso de sucesso, imprime uma mensagem de confirmação.
- A seção **`if __name__ == "__main__"`** é responsável por chamar a função para dois arquivos: `movies.csv` e `series.csv`.

#### Código:

```python
import boto3
import os
from datetime import datetime

BUCKET_NAME = 'data-lake-do-lucas'
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
```

### 2.2 Funcionalidades:

1. O código busca os arquivos `movies.csv` e `series.csv` localmente.
2. Utiliza a biblioteca **boto3** para realizar o upload dos arquivos para o **bucket S3**.
3. A estrutura de pastas dentro do bucket segue a organização padronizada por tipo de conteúdo, data e formato.

## 3. Etapa

Nesta etapa, foi criado o **Dockerfile** para a construção de um container que executará o código Python de upload dos arquivos CSV para o Amazon S3. O container garante que o ambiente necessário esteja configurado corretamente para rodar o script, independentemente da máquina local.

### 3.1 Explicação do Dockerfile:

```dockerfile
FROM python:3.9-slim
```
- **FROM python:3.9-slim**: Utiliza uma imagem base do Python 3.9 em uma versão minimalista (slim), o que reduz o tamanho da imagem Docker, mas ainda inclui tudo o que é necessário para rodar o Python e as bibliotecas exigidas.

```dockerfile
WORKDIR /app
```
- **WORKDIR /app**: Define o diretório de trabalho dentro do container como `/app`, onde o código da aplicação será armazenado e executado.

```dockerfile
COPY . /app
```
- **COPY . /app**: Copia todos os arquivos do diretório atual (onde o Dockerfile está localizado) para o diretório `/app` dentro do container. Isso inclui o script Python e qualquer arquivo necessário para sua execução.

```dockerfile
RUN pip install boto3
```
- **RUN pip install boto3**: Instala a biblioteca **boto3** dentro do container, que é necessária para interagir com o Amazon S3.

```dockerfile
CMD ["python", "main.py"]
```
- **CMD ["python", "main.py"]**: Define o comando que será executado quando o container for iniciado. Neste caso, ele executa o arquivo `main.py`, que é o script Python que realiza o upload dos arquivos CSV para o S3.

### 3.2 Dockerfile:  
```dockerfile
    FROM python:3.9-slim

    
    WORKDIR /app

   
    COPY . /app

    
    RUN pip install boto3

    
    CMD ["python", "main.py"]
```

### 3.3 Resumo:

- O **Dockerfile** constrói um ambiente isolado e configurado para rodar o script Python de upload para o S3.
- A imagem do Python 3.9 foi escolhida por ser leve e adequada para a execução de scripts.
- O diretório de trabalho é definido como `/app`, onde todos os arquivos da aplicação serão copiados.
- A biblioteca **boto3** é instalada no ambiente durante a construção do container, garantindo que todas as dependências estejam resolvidas.
- Ao iniciar o container, o script Python principal será automaticamente executado, realizando o upload dos arquivos para o Amazon S3.

## 4. Etapa:

Nesta etapa, apresentarei as execuções do código desenvolvido e os resultados obtidos. Abaixo, serão demonstradas as operações realizadas, evidenciando o funcionamento correto do script e a integração com o Amazon S3.

### 4.1 Criando a Imagem no Docker

Para criar a imagem Docker, utilizei o seguinte comando:

```bash
docker build -t s3-upload .

```

Este comando instrui o Docker a construir uma imagem a partir do `Dockerfile` presente no diretório atual, atribuindo o nome `s3-upload` à imagem gerada. Como podemos ver na imagem a segui: 

![Criando a imagem no docker](../evidencias/imgdocker.png)

### 4.2 Executando o Container a Partir da Imagem

Nesta etapa, o container foi executado utilizando o seguinte comando:

```bash
docker run -v C:/Users/lmart/.aws:/root/.aws -v C:/Users/lmart/OneDrive/Documentos/desafiopy:/app s3-upload
```

Esse comando faz o seguinte:
- **`-v C:/Users/lmart/.aws:/root/.aws`**: Mapeia o diretório local que contém as credenciais da AWS para o diretório do container, permitindo que o script acesse as credenciais necessárias para realizar operações no Amazon S3.
- **`-v C:/Users/lmart/OneDrive/Documentos/desafiopy:/app`**: Mapeia o diretório local onde os arquivos CSV estão armazenados para o diretório `/app` no container.
- **`s3-upload`**: Especifica o nome da imagem a ser utilizada para criar o container.

Essa execução permite que o script carregue os arquivos CSV para o bucket do Amazon S3, conforme demonstrado nos resultados a seguir:

- **Resultado do Upload dos Arquivos:**
![Resultado 1 do Container](../evidencias/resultado-1.png)

- **Resultado do Bucket com os Arquivos:**
![Resultado 2 do Container](../evidencias/resultado-2.png)

- **Resultado do Bucket mostrando o caminho do arquivo no S3 - movies.csv:**
![Resultado 3 do Container - movies.csv](../evidencias/resultado-mvs.png)

- **Resultado do Bucket mostrando o caminho do arquivo no S3 - series.csv:**
![Resultado 4 do Container - series.csv](../evidencias/resultado-srs.png)

# Conclusão

Neste desafio, desenvolvemos um pipeline de ingestão de dados para um Data Lake utilizando a AWS, especificamente o serviço S3. Através da criação de um bucket no S3 e do desenvolvimento de um script em Python, conseguimos carregar arquivos CSV de filmes e séries para a camada de armazenamento RAW. 
O processo foi realizado em um container Docker, permitindo um ambiente controlado e replicável. As execuções mostraram resultados positivos, com os arquivos corretamente armazenados e organizados no S3, conforme o padrão estabelecido. 
Com essa implementação, adquirimos experiência prática em manipulação de dados na nuvem, utilização da biblioteca Boto3 para interações com a AWS e compreensão do funcionamento de containers Docker. Esse projeto é um passo importante para avançar nas etapas seguintes do desafio, que incluirão o processamento e análise dos dados armazenados. 
A experiência adquirida aqui será valiosa para projetos futuros e para aprofundar o conhecimento em arquitetura de dados e serviços em nuvem.

### Observação 

Os arquivos do desafio estão localizados na pasta chamada *Arquivos*, que se encontra dentro da pasta do desafio. Os arquivos CSV não foram incluídos no repositório devido ao seu tamanho. Optei por deixá-los fora para garantir uma melhor gestão do repositório.

# Análises

Para o desafio final, pretendo realizar as seguintes análises:

- **Contar a popularidade do artista em filmes**: Nesta análise, contarei quantos filmes cada artista participou e exibirei os 10 artistas mais conhecidos, baseando-me na frequência de suas aparições.

- **Contar quantos filmes foram lançados por ano**: Esta análise envolve a contagem de filmes lançados por ano e a identificação dos 5 anos com o maior número de lançamentos. Isso nos permitirá entender quais anos foram mais produtivos para a indústria do cinema.

- **Mostrar a nota média de filmes da categoria romance**: Aqui, calcularei a média das notas dos filmes do gênero romance. Essa informação será útil para avaliar a recepção crítica geral dessa categoria de filmes.
