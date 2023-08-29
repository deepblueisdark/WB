#-------------------------------------------------------------------------------------------------------
#
#      script plotar estações  
#
#--------------------------------------------------------------------------------------------------------
# by reginaldo.venturadesa@gmail.com  em agosto de 2023 
#
#  
#
#---------------------------------------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

import geopandas as gpd
import matplotlib.pyplot as plt


# Carregar o shapefile
shapefile_path = 'bahia.shp'
gdf = gpd.read_file(shapefile_path)


# Carregar os dados do arquivo Excel
file_path = "relatorio.xlsx"
sheet_name = "CLIMA"  # Substitua pelo nome correto da planilha, se necessário

# Ler o arquivo Excel, considerando a primeira linha como cabeçalhos das colunas
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Verificar se o DataFrame não está vazio
if not df.empty:
    # Extrair as coordenadas das estações
    longitudes = df["longitude"]
    latitudes = df["latitude"]
    nomes = df["Nome"]

    # Extrair os valores da coluna "per_dados_validos"
    per_dados_validos = df["per_dados_validos"]

    # Definir mapeamento de cores com base nos intervalos especificados
    cmap = ListedColormap(['red', 'yellow', 'green', 'blue'])
    bounds = [0, 0.3, 0.4, 0.7, 1]
    norm = plt.Normalize(bounds[0], bounds[-1])

    

    # Plotar o gráfico com cores mapeadas
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(longitudes, latitudes, c=per_dados_validos, cmap=cmap, norm=norm, marker="o")

    # Plotar o shapefile
    gdf.plot(ax=plt.gca(), color='gray')  # Use ax=plt.gca() para sobrepor o shapefile ao scatter plot

    # Adicionar rótulos de estação
    for i, nome in enumerate(nomes):
        plt.text(longitudes[i], latitudes[i], nome, fontsize=4, ha="right")

    plt.title("Posição das Estações")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)

    # Adicionar uma legenda de cores
    cbar = plt.colorbar(scatter)  # Use o objeto scatter como mappable
    cbar.set_label("Percentagem de Dados Válidos", labelpad=15)

    # Salvar o gráfico como arquivo PNG
    plt.savefig("posicao_estacoes_colored.png", dpi=300, bbox_inches="tight")
    plt.show()


else:
    print("O DataFrame está vazio. Verifique o arquivo Excel e os cabeçalhos das colunas.")







# import pandas as pd
# import matplotlib.pyplot as plt

# # Carregar os dados do arquivo Excel
# file_path = "./relatorio.xlsx"
# df = pd.read_excel(file_path)

# # Carregar os dados do arquivo Excel
# file_path = "relatorio.xlsx"
# sheet_name = "CLIMA"  # Substitua pelo nome correto da planilha, se necessário

# # Ler o arquivo Excel, considerando a primeira linha como cabeçalhos das colunas
# df = pd.read_excel(file_path, sheet_name=sheet_name)


# # Extrair as coordenadas das estações
# longitudes = df["longitude"]
# latitudes = df["latitude"]
# nomes = df["Nome"]

# # Plotar o gráfico
# plt.figure(figsize=(10, 8))
# plt.scatter(longitudes, latitudes, marker="o", color="blue")

# # Adicionar rótulos de estação
# for i, nome in enumerate(nomes):
    # plt.text(longitudes[i], latitudes[i], nome, fontsize=2, ha="right")

# plt.title("Posição das Estações")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.grid(True)

# # Salvar o gráfico como arquivo PNG
# plt.savefig("posicao_estacoes.png", dpi=300, bbox_inches="tight")
# plt.show()



