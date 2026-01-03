#!/bin/bash

cd ~/ecommerce

mkdir -p vendas
mkdir -p vendas/backup


DATA=$(date +%Y%m%d)
HORA=$(date +%H.%M.%S)


cp dados_de_vendas.csv vendas/
cp vendas/dados_de_vendas.csv vendas/backup/dados-${DATA}.csv
mv vendas/backup/dados-${DATA}.csv vendas/backup/backup-dados-${DATA}.csv


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


zip vendas/backup/backup-dados-${DATA}.zip vendas/backup/backup-dados-${DATA}.csv


rm vendas/dados_de_vendas.csv
rm vendas/backup/backup-dados-${DATA}.csv

