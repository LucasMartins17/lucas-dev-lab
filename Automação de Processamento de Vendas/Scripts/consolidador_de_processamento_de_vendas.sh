#!/bin/bash

> ~/ecommerce/vendas/backup/relatorio_final.txt

for file in ~/ecommerce/vendas/backup/registro-*.txt; do
  if [ -f "$file" ]; then
    cat "$file" >> ~/ecommerce/vendas/backup/relatorio_final.txt
    echo -e "\n" >> ~/ecommerce/vendas/backup/relatorio_final.txt
  fi
done

echo "Consolidação completa. O relatório final foi salvo em ~/ecommerce/vendas/backup/relatorio_final.txt."

