# Análise de Dados Python Google play

# **Objetivo**

O objetivo deste projeto foi praticar Python utilizando as bibliotecas Pandas e Matplotlib. O projeto consistiu em ler e processar o arquivo `googleplaystore.csv`, gerar gráficos para análise de dados e visualizar informações como os top 5 apps por número de instalações, as categorias de apps e o app mais caro. Além disso, foi necessário identificar apps classificados como 'Mature 17+', os top 10 apps por número de reviews e realizar cálculos adicionais. O desafio também incluiu a criação de diferentes tipos de gráficos para uma melhor visualização dos dados.

## 1. Limpeza e Leitura dos dados 

### **1.1 - Leitura do Arquivo CSV**

Nesta etapa, realizamos a leitura do arquivo CSV que contém os dados dos aplicativos da Google Play Store. Utilizamos a biblioteca Pandas para carregar os dados em um DataFrame. Em seguida, removemos quaisquer duplicatas presentes no conjunto de dados para garantir a integridade e precisão da análise.

O código abaixo demonstra como o arquivo foi lido e as duplicatas foram eliminadas:

```python
import pandas as pd
csv = pd.read_csv('googleplaystore.csv')
csv.drop_duplicates(inplace=True)
print('Primeiras linhas do CSV:')
print(csv.head())
```

**Resultado:**

Abaixo está uma amostra das primeiras linhas do DataFrame, exibida após a leitura e limpeza inicial:

![Print das Primeiras Linhas do CSV](evidencias/Imagem%20dados%20apos%20limpeza.png)

### **1.2 - Limpeza da Coluna 'Installs'**

Nesta etapa, focamos na limpeza da coluna `Installs`, que contém o número de instalações de cada aplicativo. O objetivo foi transformar os dados em um formato numérico consistente para análise.

As seguintes operações foram realizadas:

### **1.2.1 Remoção de Caracteres Especiais:**
   - Removemos caracteres como vírgulas (`,`) e sinais de adição (`+`) que estavam presentes nos valores da coluna `Installs`.

### **1.2.2 Conversão para Tipo Numérico:**
   - Convertidos os valores da coluna `Installs` para numérico, tratando quaisquer valores inválidos com a opção `errors='coerce'`, que converte entradas não numéricas em `NaN`.

### **1.2.3 Remoção de Valores Nulos:**
   - Linhas com valores `NaN` foram removidas para garantir que apenas dados válidos fossem utilizados na análise.

### **1.2.4 Conversão Final para Inteiro:**
   - Os valores restantes foram convertidos para inteiros para facilitar a análise quantitativa.

O código abaixo ilustra essas operações:

```python
csv['Installs'] = csv['Installs'].str.replace(',', '').str.replace('+', '')
csv['Installs'] = pd.to_numeric(csv['Installs'], errors='coerce')
csv = csv.dropna(subset=['Installs']) 
csv['Installs'] = csv['Installs'].astype(int) 

print('Valores de Installs após as limpezas: ')
print(csv['Installs'].head(10))
```

**Resultado:**

Abaixo está uma amostra dos valores da coluna `Installs` após a limpeza:

![Print dos Valores de Installs Após a Limpeza](evidencias/Imagem%20install%20apos%20limpeza.png)

### **1.3 - Limpeza da Coluna 'App' e Análise dos Top 5 Apps**

Nesta etapa, realizamos a limpeza dos nomes dos aplicativos e identificamos os cinco aplicativos mais instalados. O objetivo foi preparar os dados para visualização e análise.

As seguintes operações foram realizadas:

#### **1.3.1  Limpeza dos Nomes dos Aplicativos:**
   - Removemos caracteres não ASCII dos nomes dos aplicativos para garantir que os nomes estejam em um formato legível e consistente.

   ```python
   csv['App'] = csv['App'].str.replace(r'[^\x00-\x7F]+', '', regex=True)
   ```

#### **1.3.2  Identificação dos Top 5 Aplicativos Mais Instalados:**
   - Selecionamos os cinco aplicativos com o maior número de instalações para análise detalhada.

   ```python
   top5 = csv.nlargest(5, 'Installs')
   print("Os top 5 Apps mais instalados: ")
   print(top5[['App', 'Installs']])
   ```

#### **1.3.3  Visualização dos Top 5 Aplicativos:**
   - Criamos um gráfico de barras para visualizar os cinco aplicativos mais instalados. O gráfico exibe o nome dos aplicativos e o número de instalações.

   ```python
   import matplotlib.pyplot as mp

   mp.figure(figsize=(19,8))
   mp.bar(top5['App'], top5['Installs'], color='skyblue')
   mp.xlabel('App')
   mp.ylabel('Número de instalações')
   mp.title('Top 5 Apps mais instalados')
   mp.xticks(rotation=0, ha='center')
   mp.show()
   ```
**Resultado:**

Abaixo está o gráfico que mostra os cinco aplicativos mais instalados, com a contagem de instalações:

![Gráfico dos Top 5 Apps Mais Instalados](evidencias/Imagem%20top%205%20apps%20apos%20limpeza.png)

### **2 - Distribuição das Categorias dos Aplicativos**

Nesta etapa, analisamos a distribuição das categorias dos aplicativos presentes no dataset para compreender a frequência com que cada categoria aparece. 

As seguintes operações foram realizadas:

#### **2.1 Contagem das Categorias:**
   - Contamos o número de aplicativos em cada categoria utilizando a função `value_counts()` para obter a frequência de cada categoria.

   ```python
   distrib_categoria = csv['Category'].value_counts()
   ```

#### **2.2 Visualização da Distribuição das Categorias:**
   - Criamos um gráfico de pizza para ilustrar a distribuição percentual das categorias dos aplicativos. Este gráfico ajuda a visualizar quais categorias são mais comuns e quais são menos frequentes.

   ```python
   import matplotlib.pyplot as mp

   mp.figure(figsize=(18, 8))
   mp.pie(distrib_categoria, labels=distrib_categoria.index, autopct='%1.1f%%')
   mp.title('Distribuição de categorias dos Apps')
   mp.show()
   ```

**Resultado:**

Abaixo está o gráfico de pizza que mostra a distribuição percentual das categorias dos aplicativos:

![Gráfico de Distribuição de Categorias dos Aplicativos](evidencias/Imagem%20do%20grafico%20de%20distribuição%20por%20categoria.png)

### **3 - Identificação do Aplicativo Mais Caro**

Nesta etapa, determinamos qual é o aplicativo mais caro no dataset e apresentamos seu preço. O objetivo foi identificar o aplicativo com o maior valor registrado para análise adicional.

As seguintes operações foram realizadas:

#### **3.1 Limpeza e Conversão da Coluna 'Price':**
   - Removemos o símbolo de dólar (`$`) e substituímos a entrada `'Free'` por `0` para que todos os preços possam ser tratados como valores numéricos.
   - Convertidos os valores da coluna `Price` para tipo numérico, tratando entradas inválidas como `NaN`.

   ```python
   csv['Price'] = csv['Price'].str.replace('$', '').replace('Free', '0')
   csv['Price'] = pd.to_numeric(csv['Price'], errors='coerce')
   ```

#### **3.2 Identificação do Aplicativo Mais Caro:**
   - Localizamos o aplicativo com o maior valor na coluna `Price` e exibimos seu nome e preço.

   ```python
   AppCaro = csv[csv['Price'] == csv['Price'].max()]
   print("\nO aplicativo mais caro é:{} \nValor do aplicativo: R$ {}".format(AppCaro['App'].values[0], AppCaro['Price'].values[0]))
   ```

**Resultado:**

Abaixo está a informação sobre o aplicativo mais caro encontrado no dataset:

![Resultado do Aplicativo Mais Caro](evidencias/Imagem%20do%20aplicativo%20mais%20caro.png)

### **4 - Contagem de Aplicativos Classificados como 'Mature 17+'**

Nesta etapa, contamos o número de aplicativos que são classificados como `Mature 17+` no dataset. O objetivo foi identificar quantos aplicativos possuem essa classificação etária específica.

As seguintes operações foram realizadas:

#### **4.1 Contagem de Aplicativos com Classificação 'Mature 17+':**
   - Utilizamos a função `shape[0]` para contar o número de linhas no dataset onde a classificação de conteúdo é `'Mature 17+'`.

   ```python
   Appmais17 = csv[csv['Content Rating'] == 'Mature 17+'].shape[0]
   print("\nO total de aplicativos com classificação para 'Mature 17+' é de: {}".format(Appmais17))
   ```

**Resultado:**

O total de aplicativos classificados como `'Mature 17+'` foi de:

![Resultado da Contagem de Aplicativos Mature 17+](evidencias/Imagem%20aplicativos%20com%20idade%20+17.png)

### **5 - Top 10 Aplicativos por Número de Reviews**

Nesta etapa, identificamos os 10 aplicativos com o maior número de avaliações (reviews) no dataset e geramos uma visualização para destacar esses aplicativos.

As seguintes operações foram realizadas:
#### **5.1 Limpeza e Conversão dos Dados:**
   - Removemos duplicatas para garantir que cada aplicativo seja contado apenas uma vez no cálculo.
   - Convertimos a coluna `Reviews` para o tipo `float` para facilitar a ordenação e a análise.

   ```python
   csv.drop_duplicates(inplace=True)
   csv['Reviews'] = csv['Reviews'].astype(float)
   ```

#### **5.2 Identificação dos Top 10 Aplicativos por Número de Reviews:**
   - Após remover duplicatas baseadas na coluna `App`, selecionamos os 10 aplicativos com o maior número de reviews.

   ```python
   csv_rmLinhadp = csv.drop_duplicates(subset=['App'])
   top10 = csv_rmLinhadp.nlargest(10, 'Reviews')
   print("Top 10 Apps por número de reviews:")
   print(top10[['App', 'Reviews']])
   ```

#### **5.3 Visualização dos Top 10 Aplicativos por Número de Reviews:**
   - Criamos um gráfico de barras para ilustrar os 10 aplicativos mais avaliados, destacando o número de reviews de cada um.

   ```python
   import matplotlib.pyplot as mp

   mp.figure(figsize=(12,8))
   mp.bar(top10['App'], top10['Reviews'], color='lightcoral')
   mp.xlabel('App')
   mp.ylabel('Número de Reviews')
   mp.title('Top 10 Apps por Número de Reviews')
   mp.xticks(rotation=45, ha='right')
   mp.show()
   ```

**Resultado:**

Abaixo está o gráfico de barras que mostra os 10 aplicativos com o maior número de reviews:

![Gráfico de Top 10 Apps por Número de Reviews](evidencias/Imagem%20top%2010%20aplicativos.png)

### **6 - Preço Médio dos Aplicativos por Categoria**

Nesta etapa, calculamos o preço médio dos aplicativos para cada categoria e geramos uma visualização gráfica para representar essas informações. Este cálculo adicional fornece uma visão detalhada dos preços médios das categorias de aplicativos, complementando as análises anteriores.

As seguintes operações foram realizadas:

#### **6.1 Cálculo do Preço Médio por Categoria:**
   - Agrupamos os aplicativos por categoria e calculamos o preço médio de cada uma. Este cálculo é importante para entender as diferenças de preços entre categorias.

   ```python
   mdprecoCategoria = csv.groupby('Category')['Price'].mean()
   print(f'Média de preço por categoria: {mdprecoCategoria}')
   ```

#### **6.2 Visualização do Preço Médio por Categoria:**
   - Criamos um gráfico de linhas para ilustrar o preço médio dos aplicativos em cada categoria. O gráfico mostra a variação dos preços médios entre as categorias, facilitando a comparação visual.

   ```python
   import matplotlib.pyplot as mp

   mp.figure(figsize=(14, 7))
   mp.plot(mdprecoCategoria.index, mdprecoCategoria.values, marker='o', linestyle='-', color='b')
   mp.xticks(rotation=90)
   mp.xlabel('Categoria')
   mp.ylabel('Preço Médio')
   mp.title('Preço Médio dos Aplicativos por Categoria')
   mp.grid(True)
   mp.show()
   ```

**Resultado:**

Abaixo está o calulos em forma de lista que ilustra o preço médio dos aplicativos por categoria:
![Calculo de Preço Médio por Categoria](evidencias/Imagem%20lista%20media%20preco%20por%20categoria.png)

Abaixo está o gráfico que ilustra o preço médio dos aplicativos por categoria:

![Gráfico de Preço Médio por Categoria](evidencias/Imagem%20grafico%20linha%20media%20preco%20por%20categoria.png)

### **7 - Relação entre Instalações e Reviews**

Nesta seção, analisamos a relação entre o número de instalações de um aplicativo e o número de reviews recebidos. A visualização por gráfico de dispersão (scatter plot) permite observar se há uma correlação entre esses dois fatores, proporcionando insights sobre a popularidade e o feedback dos usuários.

As operações realizadas foram:

#### **7.1 Criação do Gráfico de Dispersão:**
   - Utilizamos um gráfico de dispersão para representar a relação entre as colunas `Installs` (Número de Instalações) e `Reviews` (Número de Reviews).
   - Cada ponto no gráfico representa um aplicativo, onde a posição no eixo X indica o número de instalações e no eixo Y indica o número de reviews.

   ```python
   import matplotlib.pyplot as mp

   mp.figure(figsize=(12, 8))
   mp.scatter(csv['Installs'], csv['Reviews'], alpha=0.5)
   mp.xlabel('Número de Instalações')
   mp.ylabel('Número de Reviews')
   mp.title('Relação entre Instalações e Reviews')
   mp.grid(True)
   mp.show()
   ```

#### **7.2 Visualização do Resultado:**
   - O gráfico gerado mostra a dispersão dos aplicativos com base no número de instalações e reviews. Isso permite analisar visualmente se aplicativos mais instalados tendem a ter mais reviews, ou se há exceções.

**Resultado:**

Abaixo está o gráfico que ilustra a relação entre o número de instalações e reviews dos aplicativos:

![Gráfico de Relação entre Instalações e Reviews](evidencias/imagem%20grafico%20de%20reviews%20e%20numero%20de%20instalacao.png)


### **8 - Aplicativo com o Menor Número de Instalações**

Nesta parte do código, identificamos qual é o aplicativo com o menor número de instalações entre todos os listados no dataset. Esse dado pode fornecer insights sobre os aplicativos menos populares ou com menos visibilidade na Google Play Store.

As operações realizadas foram:

#### **8.1 Identificação do Aplicativo com Menos Instalações:**
   - Foi utilizado o método `min()` para encontrar o menor valor na coluna `Installs`, que representa o número de instalações.
   - Em seguida, buscamos o nome do aplicativo que possui esse menor número de instalações.

   ```python
   AppMenosBaixado = csv[csv['Installs'] == csv['Installs'].min()]
   print(f"O aplicativo menos baixado é: {AppMenosBaixado['App'].values[0]} \nNúmero de instalações: {AppMenosBaixado['Installs'].values[0]}")
   ```

#### **8.2 Exibição do Resultado:**
   - O nome do aplicativo com o menor número de instalações é exibido, assim como o valor exato de instalações que ele possui.

**Resultado:**

Após a execução deste código, o resultado foi:

![Imagem aplicativo menos instalado](evidencias/Imagem%20aplicativo%20menos%20instalado.png)

Esse tipo de análise é útil para entender a cauda longa da distribuição dos aplicativos, identificando aqueles que têm menos sucesso na loja.

Sim, uma conclusão baseada nas etapas apresentadas pode ser elaborada com foco nos principais resultados e aprendizados obtidos ao longo do desafio. Aqui está uma sugestão de como estruturá-la:


# **Conclusão**

Neste projeto, foram utilizadas técnicas de análise de dados utilizando Python, Pandas e Matplotlib para processar e visualizar informações sobre os aplicativos da Google Play Store. Durante a realização do projeto, foi possível executar diversas tarefas importantes, como a limpeza de dados, transformação de colunas em formatos adequados e a geração de gráficos para facilitar a visualização e interpretação dos dados.

Através da análise, obtivemos insights valiosos, como:

- Os **Top 5 aplicativos mais instalados**, evidenciando a popularidade de determinados apps.
- A **distribuição das categorias** de aplicativos, onde conseguimos identificar quais tipos de apps são mais comuns na loja.
- A identificação do **aplicativo mais caro**, que destacou como certos aplicativos podem ter valores significativamente mais elevados.
- O total de aplicativos classificados como **'Mature 17+'**, ajudando a compreender a presença de conteúdo voltado para um público mais adulto.
- A lista dos **Top 10 aplicativos por número de reviews**, permitindo uma análise da popularidade dos apps com base na opinião dos usuários.
- E por fim, a análise do **preço médio dos aplicativos por categoria**, que forneceu uma visão detalhada das diferenças de preços entre diferentes tipos de apps.

Essas etapas foram essenciais para aprimorar habilidades em manipulação de dados e visualização de informações, além de destacar a importância da limpeza e organização dos dados para garantir resultados confiáveis e úteis.

Com o uso dessas ferramentas e técnicas, foi possível responder perguntas importantes sobre o dataset da Google Play Store, e esses insights podem ser aplicados a análises mais amplas no futuro.


# Observação

Os códigos relacionados ao projeto estão organizados na pasta denominada `Codigos`. Esta organização visa proporcionar uma visualização mais prática e simplificada de todos os arquivos pertinentes ao desafio. 
Dentro desta pasta, você encontrará o arquivo **.ipynb** intitulado `analises.ipynb`, que contém uma explicação clara sobre o funcionamento das análises gráficas e cálculos realizados. Vale destacar que a explicação no notebook é mais concisa em comparação com a encontrada no README.md do projeto. Por fim ao acessar a pasta nomeada de `CSV` você poderá encontrar o arquivo `googleplaystore.csv`, que foi utilizado para esse projeto.
