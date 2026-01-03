import pandas as pand
import matplotlib.pyplot as mp

csv = pand.read_csv('googleplaystore.csv')
csv.drop_duplicates(inplace=True) 
print('Primeiras linhas do CSV: ')
print(csv.head())

csv['Installs'] = csv['Installs'].str.replace(',', '').str.replace('+', '')
csv['Installs'] = pand.to_numeric(csv['Installs'], errors='coerce')
csv = csv.dropna(subset=['Installs'])  
csv['Installs'] = csv['Installs'].astype(int) 

print('Valores de Installs após as limpezas: ')
print(csv['Installs'].head(10))

csv['App'] = csv['App'].str.replace(r'[^\x00-\x7F]+', '', regex=True)

top5 = csv.nlargest(5, 'Installs')
print("Os top 5 Apps mais instalados: ")
print(top5[['App', 'Installs']])

mp.figure(figsize=(19,8))
mp.bar(top5['App'], top5['Installs'], color='skyblue')
mp.xlabel('App')
mp.ylabel('Número de instalações')
mp.title('Top 5 Apps mais instalados')
mp.xticks(rotation=0, ha='center')
mp.show()

distrib_categoria = csv['Category'].value_counts()
mp.figure(figsize=(18, 8))
mp.pie(distrib_categoria, labels=distrib_categoria.index, autopct='%1.1f%%') 
mp.title('Distribuição de categorias dos Apps')
mp.show()

csv['Price'] = csv['Price'].str.replace('$', '').replace('Free', '0')
csv['Price'] = pand.to_numeric(csv['Price'], errors='coerce')
AppCaro = csv[csv['Price'] == csv['Price'].max()]
print("\nO aplicativo mais caro é:{} \nValor do aplicativo: R$ {}".format(AppCaro['App'].values[0], AppCaro['Price'].values[0]))

Appmais17 = csv[csv['Content Rating'] == 'Mature 17+'].shape[0]
print("\nO total de aplicativos com classificação para 'Mature 17+' é de: {}".format(Appmais17))

csv.drop_duplicates(inplace=True)
csv['Reviews'] = csv['Reviews'].astype(float)
csv_rmLinhadp = csv.drop_duplicates(subset=['App'])
top10 = csv_rmLinhadp.nlargest(10, 'Reviews')
print("Top 10 Apps por número de reviews:")
print(top10[['App', 'Reviews']])

mp.figure(figsize=(12,8))
mp.bar(top10['App'], top10['Reviews'], color='lightcoral')
mp.xlabel('App')
mp.ylabel('Número de Reviews')
mp.title('Top 10 Apps por Número de Reviews')
mp.xticks(rotation=45, ha='right')
mp.show()

mdprecoCategoria = csv.groupby('Category')['Price'].mean()
print(f'Media preco por categoria: {mdprecoCategoria}')

mdprecoCategoria = csv.groupby('Category')['Price'].mean().sort_index()
mp.figure(figsize=(14, 7))
mp.plot(mdprecoCategoria.index, mdprecoCategoria.values, marker='o', linestyle='-', color='b')
mp.xticks(rotation=90)
mp.xlabel('Categoria')
mp.ylabel('Preço Médio')
mp.title('Preço Médio dos Aplicativos por Categoria')
mp.grid(True)
mp.show()

mp.scatter(csv['Installs'], csv['Reviews'])
mp.xlabel('Número de Instalações')
mp.ylabel('Número de Reviews')
mp.title('Relação entre Instalações e Reviews')
mp.show()

AppMenosBaixado = csv[csv['Installs'] == csv['Installs'].min()]
print(f"O aplicativo menos baixado é: {AppMenosBaixado['App'].values[0]} \nNúmero de instalações: {AppMenosBaixado['Installs'].values[0]}")



