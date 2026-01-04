# 🎯 Pipeline de Dados End-to-End: Indústria de Cinema

Este projeto faz parte do meu **Dev Lab de Engenharia de Dados** e tem como objetivo desenvolver, na prática, uma arquitetura de Data Lake na AWS, passando por todas as etapas do ciclo de dados:

✔ ingestão
✔ processamento
✔ modelagem analítica
✔ visualização e geração de insights

O projeto integra dados provenientes de **arquivos CSV** e de uma **API externa do TMDB**, estruturando-os em um ambiente escalável e orientado a analytics.

---

## 🚀 Objetivos do Projeto

🔹 Construção de um Data Lake em arquitetura em camadas
🔹 Desenvolvimento de pipeline ETL com PySpark no AWS Glue
🔹 Conversão de dados brutos para formato otimizado (Parquet)
🔹 Modelagem dimensional para análises de negócio
🔹 Consultas analíticas via Athena
🔹 Criação de dashboards no QuickSight

O foco do projeto é demonstrar:

> habilidades técnicas + visão analítica + boas práticas arquiteturais.

---

## 🧱 Estrutura do Projeto

```
01-Ingestao/
02-Processamento-ETL/
03-Modelagem-Analytics/
04-Visualizacao/
```

Cada pasta representa uma etapa do pipeline de dados.

---

## 🔹 1. Ingestão de Dados (01-Ingestao)

### 📥 Função

Responsável por capturar e armazenar os dados de:

* Arquivos CSV (fonte estática)
* API TMDB (fonte dinâmica)

Os dados são armazenados na camada:

🟤 **Raw / Bronze** — formato original, sem transformação

### 🛠️ Tecnologias aplicadas

* Boto3 para integração com AWS
* AWS Lambda (Serverless) para ingestão automática
* Armazenamento em JSON no S3

Estrutura no S3:

```
raw/
 ├── csv/
 └── api_tmdb/
```

Nesta etapa demonstro conhecimento em:

✔ integração com APIs
✔ automação serverless
✔ organização de dados no Data Lake

---

## 🔹 2. Processamento — ETL (02-Processamento-ETL)

### 🧹 Função

Transformação dos dados brutos com foco em:

✔ limpeza
✔ padronização
✔ eficiência de armazenamento
✔ performance de leitura

Os dados tratados seguem para:

⚪ **Trusted / Silver**

### 🛠️ Tecnologias aplicadas

* Apache Spark (PySpark) no AWS Glue
* Conversão de CSV/JSON → Parquet
* Processamento distribuído

Benefícios alcançados:

✔ redução de custo de armazenamento
✔ consultas mais rápidas
✔ estrutura pronta para analytics

---

## 🔹 3. Modelagem & Analytics (03-Modelagem-Analytics)

### 🧠 Função

Organiza os dados para análise de negócio por meio de:

⭐ **Modelagem Dimensional (Star Schema)**

* Tabelas Fato
* Tabelas Dimensão

Dados armazenados na:

🟡 **Refined / Gold**

### 🛠️ Tecnologias aplicadas

* AWS Glue Crawler para catalogação
* Consultas SQL no Amazon Athena

Resultados:

✔ dados organizados por domínio de negócio
✔ alto desempenho para análises
✔ base preparada para BI

---

## 🔹 4. Visualização & Insights (04-Visualizacao)

### 📊 Função

Criação de dashboards interativos no:

➡ Amazon QuickSight

Conectado ao Athena para análise direta no S3.

### 🔎 Principais análises realizadas

* Popularidade de artistas
* Tendência de gêneros (Drama, Romance, Comédia)
* Evolução histórica de produções
* Distribuição temporal de lançamentos

Objetivo desta etapa:

✔ transformar dados em decisão
✔ comunicar resultados de forma visual
✔ validar a arquitetura analítica do projeto

---

## 🧩 Tecnologias Utilizadas

| Área                 | Ferramenta         |
| -------------------- | ------------------ |
| Data Lake            | Amazon S3          |
| Ingestão & Automação | AWS Lambda + Boto3 |
| Processamento        | AWS Glue + PySpark |
| Catálogo de Dados    | AWS Glue Crawler   |
| Query Engine         | Amazon Athena      |
| Visualização         | Amazon QuickSight  |
| Fonte Externa        | TMDB API           |

---

## 📌 Competências Desenvolvidas no Projeto

✔ Arquitetura de Data Lake em camadas
✔ Processamento distribuído com Spark
✔ ETL orientado a performance
✔ Modelagem dimensional para analytics
✔ Integração entre serviços AWS
✔ Construção de pipeline escalável e modular

