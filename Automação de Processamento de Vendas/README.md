# Automação de Processamento de Vendas (Projeto Linux)
 **Objetivo**

O desafio consistia em criar e configurar scripts para processar arquivos CSV de vendas, organizando-os em uma estrutura de pastas dentro de um diretório chamado `ecommerce`. Dentro deste diretório, foram criadas as pastas `vendas` e `backup`, onde os arquivos de vendas foram processados e armazenados. O objetivo era **gerar relatórios diários a partir desses dados e consolidá-los em um relatório final**. Além disso, foi necessário configurar o agendamento automático para a execução dos scripts, garantindo a correta manipulação e arquivamento dos arquivos gerados.


# **Desenvolvimento** 

 ## 1 - Desenvolvimento dos Scripts 
 - ***1.1 Script de Processamento de Vendas*** (**processamento_de_vendas.sh**)
    
    - **Localização:** Pasta `ecommerce`
    - **Função:** Processar o arquivo CSV de vendas (**dados_de_vendas.csv**) para gerar relatórios diários sobre as vendas, capturando e organizando os dados de  forma detalhada.
    - **Descrição:** O script foi desenvolvido para ler e processar o arquivo CSV de vendas, extraindo e organizando as informações contidas nele. A cada execução, o script gera um relatório diário com um nome único baseado na data e hora da geração, garantindo que cada relatório seja distinto e não sobreponha relatórios anteriores. Este processo inclui a captura de informações-chave, como a data do primeiro e do último registro de venda, a quantidade total de itens distintos vendidos, e as primeiras linhas do arquivo CSV para revisão rápida. Esses relatórios são fundamentais para uma análise detalhada e contínua das vendas, permitindo uma visão clara e estruturada das transações diárias.

    **Como evidenciado na imagem a seguir:** 

      - **Imagem do codigo do Script `processamento_de_vendas.sh`:**

    ![codigo do processamento_de_vendas sh para mostar no README na parte de desenvolvimento](../evidencias/codigo%20do%20processamento_de_vendas.sh%20-%202.png)

 - ***1.2 Script de Consolidação*** (**consolidador_de_processamento_de_vendas.sh**)

    - **Localização:** Pasta `ecommerce`
    - **Função:** Consolidar os relatórios gerados pelo script de processamento, unificando os dados em um único arquivo para fornecer um relatório final  abrangente e bem estruturado.
    - **Descrição:** Este script é responsável por reunir e consolidar todos os relatórios diários criados pelo script de processamento. Ele lê cada arquivo de relatório gerado, anexa seu conteúdo a um arquivo principal chamado `relatorio_final.txt`, e garante que o arquivo consolidado reflita apenas os dados mais recentes. Para assegurar que o relatório final esteja sempre atualizado e livre de dados antigos, o script inicia sua execução limpando o conteúdo do arquivo relatorio_final.txt. Esse processo permite uma visão consolidada e clara das vendas, facilitando a análise e a monitorização contínua das informações ao longo do tempo.

   **Como evidenciado na imagem a seguir:** 
      - **Imagem do codigo do Script `consolidador_de_processamento_de_vendas.sh`:**
      ![codigo do processamento_de_vendas sh para mostar no README na parte de desenvolvimento](../evidencias/codigo%20do%20consolidador_de_vendas.sh%20%20-%201.png)
 ## 2 - Geração de Relatórios
 - ***2.1 Relatórios Diários***

   Após a execução do script processamento_de_vendas.sh, são gerados relatórios diários que contêm informações detalhadas sobre as vendas realizadas. Cada relatório é criado com um nome único que inclui a data e a hora da geração, garantindo que os dados de cada dia sejam registrados separadamente e não sejam sobrepostos. 

      - O script `processamento_de_vendas.sh` é executado para processar o arquivo CSV de vendas e gerar um relatório diário. O relatório contém:
         - Data do sistema operacional.
         - Data do primeiro e último registro de venda.
         - Quantidade total de itens distintos vendidos.
         - As primeiras linhas do arquivo CSV para revisão rápida.
         - Esses relatórios são armazenados em uma pasta de backup com nomes únicos baseados na data e hora.

      - O trecho responsável por essa funcionalidade é o seguinte:
   ```bash
      DATA_do_SISTEMA=$(date +%Y/%m/%d\ %H:%M)
      DATA_INICIO=$(tail -n +2 vendas/dados_de_vendas.csv | cut -d',' -f5 | sed 's/\([0-9]\{2\}\)\/\([0-9]\{2\}\)\/\([0-9]\{4\}\)/\3\2\1/' | sort | head -n 1 | sed 's/\(....\)\(..\)\(..\)/\1-\2-\3/')
      DATA_FIM=$(tail -n +2 vendas/dados_de_vendas.csv | cut -d',' -f5 | sed 's/\([0-9]\{2\}\)\/\([0-9]\{2\}\)\/\([0-9]\{4\}\)/\3\2\1/' | sort | tail -n 1 | sed 's/\(....\)\(..\)\(..\)/\1-\2-\3/')
      QUANTIDADE_ITENS=$(tail -n +2 vendas/dados_de_vendas.csv | cut -d',' -f2 | sort | uniq | wc -l)

      {
         echo "Data do sistema operacional: $DATA_do_SISTEMA"
         echo "Data do primeiro registro de venda: $DATA_INICIO"
         echo "Data do último registro de venda: $DATA_FIM"
         echo "Quantidade total de itens diferentes vendidos: $QUANTIDADE_ITENS"
         head -n 11 vendas/backup/backup-dados-${DATA}.csv
      } > vendas/backup/registro-${DATA}-${HORA}.txt
      ```
      
      **OBS: Foram extraídas 11 linhas para exibir o cabeçalho do arquivo, seguido das 10 primeiras linhas de produtos.**

 - ***2.2 Relatório Consolidado***
 
   O script `consolidador_de_processamento_de_vendas.sh` realiza a consolidação dos relatórios diários gerados pelo script `processamento_de_vendas.sh`. Ele agrega todos os relatórios diários em um único arquivo chamado `relatorio_final.txt`.

      - O processo de consolidação inclui:
         - *Limpeza Inicial*: O script começa limpando o conteúdo de relatorio_final.txt para garantir que o relatório final reflita apenas os dados mais recentes e não contenha informações antigas.
         - *Anexação de Dados*: Em seguida, o conteúdo de todos os relatórios diários é anexado a relatorio_final.txt, proporcionando uma visão unificada e clara das vendas ao longo do tempo.
   
-  ***2.3 Compactação dos Backups Diários***

   O script `processamento_de_vendas.sh` também lida com a compactação dos dados diários. Após gerar o arquivo de backup com os dados do dia, ele compacta esse arquivo em um formato ZIP. A compactação ajuda a otimizar o armazenamento e a organização dos arquivos. O arquivo ZIP é nomeado com base na data do backup, garantindo que cada arquivo compactado seja facilmente identificável.

      - O processo de compactação segue os seguintes passos:
     
         - O script copia o arquivo `dados_de_vendas.csv` para a pasta de backup.
         - Em seguida, o arquivo de backup é compactado em um arquivo ZIP com um nome que inclui a data do backup.
         - Após a compactação, o arquivo original e o backup não compactado são removidos para economizar espaço de armazenamento

      - O trecho de código responsável por essa funcionalidade é o seguinte:
   ```bash
      zip vendas/backup/backup-dados-${DATA}.zip vendas/backup/backup-dados-${DATA}.csv
      rm vendas/dados_de_vendas.csv
      rm vendas/backup/backup-dados-${DATA}.csv
   ```

   **Como evidenciado nas imagens a seguir:** 
      - **Imagens do resultado do relatorio_final.txt pt - 1:**

      ![codigo do processamento_de_vendas sh para mostar no README na parte de desenvolvimento](../evidencias/mostrando%20resultado%20do%20relatorio%20final%20-%20pt%201.png)

      - **Imagens do resultado do relatorio_final.txt: pt - 2:**

      ![codigo do processamento_de_vendas sh para mostar no README na parte de desenvolvimento](../evidencias/mostrando%20resultado%20do%20relatorio%20final%20-%20pt%202.png)


      - **Imagens dos resultados dos Scripts de `processamento_de_vendas.sh` e `consolidador_de_processamento_de_vendas.sh` apos serem executados:**

      ![codigo do processamento_de_vendas sh para mostar no README na parte de desenvolvimento](../evidencias/vendas%20e%20consolidador.png)

 ## 3 - Agendamento do Script
 - ***3.1 Configuração do Cron*** 

   Para garantir a execução automática dos scripts de processamento e consolidação, foi configurado o agendamento automático utilizando o cron. A configuração permite que o scrip `processamento_de_vendas.sh`seja executado todos os dias de segunda a quinta-feira às 15:27. Isso garante que os dados de vendas sejam processados e os relatórios diários sejam gerados automaticamente.

     *3.1.1 - Comando de Agendamento:*

     `27 15 * * 1-4 /home/lucas/ecommerce/processamento_de_vendas.sh`
     
     *3.1.2 - Descrição:*

     O comando acima configura o cron para executar o script `processamento_de_vendas.sh` às 15:27, de segunda a quinta-feira. Esse agendamento automatiza o processo de geração dos relatórios diários e a criação dos backups.

     **Como evidenciado na imagem a seguir:**
      - **Imagen demonstrando como foi feito o agendamento:**
      ![codigo do processamento_de_vendas sh para mostar no README na parte de desenvolvimento](../evidencias/print%20para%20mostar%20o%20agendamento.png)

 ## 4 - Execução e Reexecução dos Scripts
  - ***4.1 Execução Inicial*** 

  Para executar os scripts pela primeira vez, siga os passos abaixo:
   - *4.1.1 Abra o terminal e navegue até o diretório ecommerce onde os scripts e a planilha `dados_de_vendas.csv` estão localizados:*
     
      `cd /home/lucas/ecommerce` 
     
   - *4.1.2 Execute o script de processamento de vendas com o comando abaixo:* 
    
      `./processamento_de_vendas.sh` 
     
   - *4.1.3 Execute o script de consolidação para unificar os relatórios diários em um único arquivo:*
     
     `./consolidador_de_processamento_de_vendas.sh` 

   - *4.1.4 Navegue até o diretório vendas e backup onde os `registros.txt` diarios, `relatorio_final.txt` e o backup da planilha de `dados_de_vendas.csv` estao estão localizados:*

      `cd vendas/backup` 

   - *4.1.5 Apos isso para ler os `registro.txt` e o `relatorio_final.txt` no terminal execute o seguinte comando:*
   
     `cat registro.txt ou cat registro_final.txt`
   
   **OBS: Cada registro e gerado com seu dia e hora de criação entao sera nescessario ler ver seu nome completo como `registro-20240812-15.27.01.txt` por exemplo**
   
     
# Considerações finais

Em minha percepção, o desafio não foi tão complexo, principalmente devido à sólida base que obtive no curso de Linux. Essa formação foi fundamental para compreender e implementar as soluções de forma eficaz, atendendo aos requisitos estabelecidos com sucesso.
Incluí imagens e prints para evidenciar claramente as etapas e os resultados dos processos. Em algumas situações, optei por incluir trechos de código diretamente, pois isso proporcionou uma explicação mais clara e direta dos procedimentos realizados.
Acredito que a documentação está bem estruturada e fornece uma visão abrangente das etapas e dos resultados, permitindo uma fácil compreensão e reexecução do desafio.

# Diretorios dos arquivos

Nos diretórios abaixo, você poderá acessar as evidências que eu incluí, além de visualizar o resultado final na pasta `ecommerce`, que contém todos os relatórios, backups, e os códigos gerados. Para facilitar a compreensão, os scripts também foram clonados para uma pasta separada, caso haja qualquer confusão ao examiná-los na pasta `ecommerce`.

1 📁 - [Ecommerce - Scripts](Ecommerce-%20Scripts/)
 
2 📁 - [Evidencias](../evidencias/)


