#-------------------------------------------------------------------------------------------------------
#
#      script clusterizaçõ e avaliação por histogramas  
#
#--------------------------------------------------------------------------------------------------------
# by reginaldo.venturadesa@gmail.com  em agosto de 2023 
#
#  
#
#---------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage

# Carregar os dados do arquivo Excel
file_path = "relatorio.xlsx"
sheet_name = "CLIMA"
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Criar a variável x
x = data["Media"] * 365

# Definir os intervalos e rótulos de classificação
intervals = [0, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, np.inf]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

# Definir os intervalos e rótulos de classificação
#intervals = [0, 400,  1000, 2000, 3000, np.inf]
#labels = [0, 1, 2, 3, 4]



# Definir cores para cada intervalo
colors = ['blue', 'green', 'yellow', 'orange', 'red', 'purple', 'pink', 'brown', 'gray', 'cyan', 'magenta', 'lime', 'teal', 'indigo', 'violet']

# Adicionar a coluna de classificação
data["Classificacao"] = pd.cut(x, bins=intervals, labels=labels)

# Carregar o shapefile
shapefile_path = 'bahia.shp'
gdf = gpd.read_file(shapefile_path)

# Definir o conjunto de dados para a clusterização
x_for_clustering = data[["Classificacao"]]

# Clustering dos dados
kmeans = KMeans(n_clusters=14)
identified_clusters = kmeans.fit_predict(x_for_clustering)

data_with_clusters = data.copy()
data_with_clusters['Cluster'] = identified_clusters

# Substituir o valor infinito por um valor maior que o maior valor em x
max_value = np.max(x)
intervals[-1] = max_value + 1

# Plotar os resultados
plt.figure(figsize=(10, 8))
scatter = plt.scatter(data['longitude'], data['latitude'], c=data_with_clusters['Cluster'], cmap='rainbow')
gdf.plot(ax=plt.gca(), color='gray')
plt.xlim(-48, -37)
plt.ylim(-19, -8)

# Adicionar legenda com rótulos de intervalos
legend_labels = [f"{intervals[i]} - {intervals[i+1]}" for i in range(len(intervals) - 1)]
plt.legend(handles=scatter.legend_elements()[0], labels=legend_labels, title="Intervalos", loc="lower left", ncols=2, fontsize='small')
plt.title("Clusterizaçao K-Means")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True)

# Ajustar rótulos do eixo X com espaçamento adequado
plt.xticks(rotation=90)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(base=len(data) // 20))  # Ajuste o divisor conforme necessário
plt.savefig("cluster.png", dpi=300, bbox_inches="tight")
plt.show()

# Calcular e plotar o dendrograma
Z = linkage(x_for_clustering, method='ward')
plt.figure(figsize=(10, 6))
dendrogram(Z)
plt.title("Dendrograma de Cluster")
plt.xlabel("Índices dos Pontos")
plt.ylabel("Distância")

# Ajustar rótulos do eixo X do dendrograma com espaçamento adequado
plt.xticks(rotation=90)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(base=len(data) // 20))  # Ajuste o divisor conforme necessário
plt.savefig("dendrograma.png", dpi=300, bbox_inches="tight")
plt.show()

# Criar histograma baseado nos intervalos
plt.figure(figsize=(8, 6))
plt.hist(x, bins=intervals, color='blue', edgecolor='black', alpha=0.7)
plt.title("Histograma dos Intervalos")
plt.xlabel("Valor")
plt.ylabel("Frequência")
plt.xticks(intervals[:-1], rotation=45)
plt.savefig("histograma.png", dpi=300, bbox_inches="tight")
plt.show()

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import geopandas as gpd
# from sklearn.cluster import KMeans

# # Carregar os dados do arquivo Excel
# file_path = "relatorio.xlsx"
# sheet_name = "CLIMA"
# data = pd.read_excel(file_path, sheet_name=sheet_name)

# # Criar a variável x
# x = data["Media"] * 365

# # Definir os intervalos e rótulos de classificação
# intervals = [0, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, np.inf]
# labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

# # Definir cores para cada intervalo
# colors = ['blue', 'green', 'yellow', 'orange', 'red', 'purple', 'pink', 'brown', 'gray', 'cyan', 'magenta', 'lime', 'teal', 'indigo', 'violet']

# # Adicionar a coluna de classificação
# data["Classificacao"] = pd.cut(x, bins=intervals, labels=labels)

# # Carregar o shapefile
# shapefile_path = 'bahia.shp'
# gdf = gpd.read_file(shapefile_path)

# # Definir o conjunto de dados para a clusterização
# x_for_clustering = data[["Classificacao"]]

# # Clustering dos dados
# kmeans = KMeans(n_clusters=14)
# identified_clusters = kmeans.fit_predict(x_for_clustering)

# data_with_clusters = data.copy()
# data_with_clusters['Cluster'] = identified_clusters

# # Plotar os resultados
# plt.figure(figsize=(10, 8))
# scatter = plt.scatter(data['longitude'], data['latitude'], c=data_with_clusters['Cluster'], cmap='rainbow')
# gdf.plot(ax=plt.gca(), color='gray')
# plt.xlim(-48, -37)
# plt.ylim(-19, -8)

# # Adicionar legenda com rótulos de intervalos
# legend_labels = [f"{intervals[i]} - {intervals[i+1]}" for i in range(len(intervals) - 1)]
# plt.legend(handles=scatter.legend_elements()[0], labels=legend_labels, title="Intervalos", loc="lower left",ncols=2)
# plt.title("Clusterizaçao K-Means")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.grid(True)
# plt.savefig("cluster.png", dpi=300, bbox_inches="tight")
# plt.show()




# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import geopandas as gpd
# from sklearn.cluster import KMeans

# # Carregar os dados do arquivo Excel
# file_path = "relatorio.xlsx"
# sheet_name = "CLIMA"
# data = pd.read_excel(file_path, sheet_name=sheet_name)

# # Criar a variável x
# x = data["Media"] * 365

# # Definir os intervalos e rótulos de classificação
# intervals = [0,400, 600, 800, 1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000, np.inf]
# labels =    [  0,   1,   2,    3,   4,   5,   6,   7,   8 ,  9,  10,  11,  12 ,13 ,14]
# print(len(labels),len(intervals))

# # Adicionar a coluna de classificação
# data["Classificacao"] = pd.cut(x, bins=intervals, labels=labels)

# # Carregar o shapefile
# shapefile_path = 'bahia.shp'
# gdf = gpd.read_file(shapefile_path)

# # Definir o conjunto de dados para a clusterização
# x_for_clustering = data[["Classificacao"]]
# print(x_for_clustering)
# # Clustering dos dados
# kmeans = KMeans(n_clusters=14)
# identified_clusters = kmeans.fit_predict(x_for_clustering)

# data_with_clusters = data.copy()
# data_with_clusters['Cluster'] = identified_clusters

# # Plotar os resultados
# plt.scatter(data['longitude'], data['latitude'], c=data_with_clusters['Cluster'], cmap='rainbow')
# gdf.plot(ax=plt.gca(), color='gray') 
# plt.xlim(-48, -37)
# plt.ylim(-19, -8)
# plt.savefig("cluster.png", dpi=300, bbox_inches="tight")



# # # This Python 3 environment comes with many helpful analytics libraries installed
# # # It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# # # For example, here's several helpful packages to load

# # import numpy as np # linear algebra
# # import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# # import matplotlib.pyplot as plt
# # #import seaborn as sns
# # # Set the styles to Seaborn
# # #sns.set()
# # # Import the KMeans module so we can perform k-means clustering with sklearn
# # from sklearn.cluster import KMeans
# # # Input data files are available in the read-only "../input/" directory
# # # For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

# # import geopandas as gpd


		
		
# # # You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# # # You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current sessio
# # # Carregar os dados do arquivo Excel
# # file_path = "relatorio.xlsx"
# # sheet_name = "CLIMA"  # Substitua pelo nome correto da planilha, se necessário
# # data = pd.read_excel(file_path, sheet_name=sheet_name)

# # x = data["Media"]*365



# # # Carregar o shapefile
# # shapefile_path = 'bahia.shp'
# # gdf = gpd.read_file(shapefile_path)

# # #data=pd.read_csv('../input/catecorical/Categorical.csv')
# # x = data.iloc[:,20:21]

# # # Valores a serem interpolados (neste exemplo, usaremos a coluna "per_dados_validos")


# # print(x)


# # #clustering data
# # kmeans = KMeans(8)
# # kmeans.fit(x)

# # #predict cluster
# # identified_clusters = kmeans.fit_predict(x)
# # print(identified_clusters)

# # data_with_clusters = data.copy()
# # data_with_clusters['Cluster'] = identified_clusters

# # plt.scatter(data['longitude'], data['latitude'], c=data_with_clusters['Cluster'], cmap = 'rainbow')
# # gdf.plot(ax=plt.gca(), color='gray') 
# # plt.xlim(-48,-37)
# # plt.ylim(-19,-8)
# # plt.savefig("cluster.png", dpi=300, bbox_inches="tight")

