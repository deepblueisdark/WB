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



# Função para calcular a variancia no período
def plota_estacoes(df,arquivo_out_png, limite_max,limite_min,origem):
    periodo = df[(df['Per. Dados Validos'] >=limite_min ) & (df['Per. Dados Validos'] <= limite_max)]
    print(len(periodo)) 

    if not periodo.empty:
       # Extrair as coordenadas das estações
       longitudes = periodo["Longitude"]
       latitudes = periodo["Latitude"]
       nomes = periodo["Nome"]

       # Extrair os valores da coluna "per_dados_validos"
       per_dados_validos = periodo['Per. Dados Validos']

       # Definir mapeamento de cores com base nos intervalos especificados
       cmap = ListedColormap(['red','purple','magenta','violet','pink', 'orange','yellow', 'lime','green', 'blue','black'])
       bounds = [ 0, 0.1, 0.2, 0.3,  0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
       norm = plt.Normalize(bounds[0], bounds[-1])

      #colors = ['blue', 'green', 'yellow', 'orange', 'red', 'purple', 'pink', 'brown', 'gray', 'cyan', 'magenta', 'lime', 'teal', 'indigo', 'violet']


       # Plotar o gráfico com cores mapeadas
       plt.figure(figsize=(10, 8))
       scatter = plt.scatter(longitudes, latitudes, c=per_dados_validos, cmap=cmap, norm=norm, marker="o")
     
       # Plotar o shapefile
       #gdf.plot(ax=plt.gca(), color='gray')  # Use ax=plt.gca() para sobrepor o shapefile ao scatter plot
       #gdf.plot(ax=plt.gca(), edgecolor='gray')
       gdf.plot(ax=plt.gca(), edgecolor='gray', facecolor='none', lw=1)  # lw é a largura da linha da borda
	   
       # Adicionar rótulos de estação
       for index, row in df.iterrows():
           plt.text(row['Longitude'], row['Latitude'], row['Nome'], fontsize=2, ha="right")

       plt.title("Distribuição de estações:Perc. Dados válidos:"+str(limite_max*100)+"% a "+str(limite_min*100)+"%"+" ["+origem+"]")
       plt.xlabel("Longitude")
       plt.ylabel("Latitude")
       plt.grid(True)

       # Adicionar uma legenda de cores
       cbar = plt.colorbar(scatter)  # Use o objeto scatter como mappable
       cbar.set_label("Percentagem de Dados Válidos", labelpad=15)
       
       # Salvar o gráfico como arquivo PNG
       plt.savefig(arquivo_out_png, dpi=300, bbox_inches="tight")
       plt.show()
       return None
    else:
       print("O DataFrame está vazio. Verifique o arquivo Excel e os cabeçalhos das colunas.")
       return None




# Carregar o shapefile
shapefile_path = '/mnt/e/OneDrive/OPERACIONAL/SHAPES/estadosBR/BAHIA/BAHIA.shp'
gdf = gpd.read_file(shapefile_path)
#
#
#
# Carregar os dados do arquivo Excel
#
#
#
file_path = "relatorio_inmet_CONV_19610101_a_20221231_e_19910101_a_20201231.xlsx"
sheet_name = "TODOS"  # Substitua pelo nome correto da planilha, se necessário
#
#
#  ABA TODOS
#
#
df = pd.read_excel(file_path, sheet_name=sheet_name)
#
# PLOTA DISTRIBUIÇÃO 
#
# plota_estacoes(df,<nome da figura>, perc. minimo, perc. máximo, [observações] )
#
# nome da figura: nome da figura em png 
# perc. minimo : percentual mínimo de dados válidos (coluna Q na planilha)
# perc. máxima : percentual máxima de dados válidos (coluna Q na planilha)
#
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_100_a_80_per.png",1.0,.80," Para cada estação") 
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_100_a_60_per.png",1.0,.60," Para cada estação")  
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_100_a_50_per.png",1.0,.50," Para cada estação")  
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_todo_o_conjunto.png",1,0," Para cada estação") 
#
# ABA CLIMA
#
#
# PLOTA DISTRIBUIÇAO DOS DADOS 
#
#
df = pd.read_excel(file_path, sheet_name="CLIMA")
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_100_a_80_per_1991a20202.png",1.0,.80," Periodo: 1991-2020") 
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_100_a_60_per_1991a20202.png",1.0,.60," Periodo: 1991-2020")  
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_100_a_50_per_1991a20202.png",1.0,.50," Periodo: 1991-2020")  
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_todo_o_conjunto_1991a20202.png",1,0, " Periodo: 1991-2020") 
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_descartados_1991a20202.png",.30,0,   " Periodo: 1991-2020") 
plota_estacoes(df,"estacoes_INMET_CONV_BAHIA_30_a_50_per_1991a20202.png",.50,.30, " Periodo: 1991-2020") 



#
#
file_path = "relatorio_inmet_TEL_20000512_a_20231231_e_19910101_a_20201231.xlsx"
sheet_name = "TODOS"  # Substitua pelo nome correto da planilha, se necessário
#
#
#  ABA TODOS
#
#
df = pd.read_excel(file_path, sheet_name=sheet_name)
#
# PLOTA DISTRIBUIÇÃO 
#
# plota_estacoes(df,<nome da figura>, perc. minimo, perc. máximo, [observações] )
#
# nome da figura: nome da figura em png 
# perc. minimo : percentual mínimo de dados válidos (coluna Q na planilha)
# perc. máxima : percentual máxima de dados válidos (coluna Q na planilha)
#
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_100_a_80_per.png",1.0,.80," Para cada estação") 
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_100_a_60_per.png",1.0,.60," Para cada estação")  
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_100_a_50_per.png",1.0,.50," Para cada estação")  
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_todo_o_conjunto.png",1,0," Para cada estação") 
#
# ABA CLIMA
#
#
# PLOTA DISTRIBUIÇAO DOS DADOS 
#
#
df = pd.read_excel(file_path, sheet_name="CLIMA")
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_100_a_80_per_1991a20202.png",1.0,.80," Periodo: 1991-2020") 
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_100_a_60_per_1991a20202.png",1.0,.60," Periodo: 1991-2020")  
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_100_a_50_per_1991a20202.png",1.0,.50," Periodo: 1991-2020")  
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_todo_o_conjunto_1991a20202.png",1,0, " Periodo: 1991-2020") 
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_descartados_1991a20202.png",.30,0,   " Periodo: 1991-2020") 
plota_estacoes(df,"estacoes_INMET_TEL_BAHIA_30_a_50_per_1991a20202.png",.50,.30, " Periodo: 1991-2020") 

