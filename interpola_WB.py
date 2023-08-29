#-------------------------------------------------------------------------------------------------------
#
#      script interpolacao dos dados 
#
#--------------------------------------------------------------------------------------------------------
# by reginaldo.venturadesa@gmail.com  em agosto de 2023 
#
#  
#
#---------------------------------------------------------------------------------------------------------
import numpy as np
from pykrige.ok import OrdinaryKriging
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from netCDF4 import Dataset

def save_to_netcdf(filename, longitude, latitude, variable_name, data):
    rootgrp = Dataset(filename, "w", format="NETCDF4")
    
    rootgrp.createDimension("lon", len(longitude))
    rootgrp.createDimension("lat", len(latitude))
    
    lon_var = rootgrp.createVariable("lon", "f4", ("lon",))
    lon_var[:] = longitude
    
    lat_var = rootgrp.createVariable("lat", "f4", ("lat",))
    lat_var[:] = latitude
    
    var = rootgrp.createVariable(variable_name, "f4", ("lat", "lon"))
    var[:, :] = data
    
    rootgrp.close()


def interpola(obs_longitudes,obs_latitudes,values_to_interpolate,variograma):
    # Coordenadas da grade para interpolação (você pode ajustar isso conforme necessário)
    grid_latitudes = np.linspace(min(obs_latitudes), max(obs_latitudes), 100)
    grid_longitudes = np.linspace(min(obs_longitudes), max(obs_longitudes), 100)

    # Criar malha de coordenadas
    grid_x, grid_y = np.meshgrid(grid_longitudes, grid_latitudes)
    # Configurar o modelo de kriging
    OK = OrdinaryKriging(
         obs_longitudes,
         obs_latitudes,
         values_to_interpolate,
         variogram_model=variograma,  # Pode escolher um modelo de variograma diferente
    )

    # Realizar a interpolação
    z, ss = OK.execute("grid", grid_longitudes, grid_latitudes)
    return z,grid_x,grid_y

def plota_interp(grid_x,grid_y,z,niveis,colormap,obs_longitudes,obs_latitudes,valores,nomevar,nome_figura,modelo):
    # Plotar a interpolação
    plt.figure(figsize=(10, 8))
    plt.contourf(grid_x, grid_y, z, levels=niveis, cmap=colormap)
    plt.scatter(obs_longitudes, obs_latitudes, c=valores, cmap=colormap, edgecolors='k')
    # Plotar o shapefile
    gdf.plot(ax=plt.gca(), color='gray')  # Use ax=plt.gca() para sobrepor o shapefile ao scatter plot

    plt.colorbar(label=nomevar)
    plt.title("Interpolação com Kriging "+modelo)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.savefig(nome_figura, dpi=300, bbox_inches="tight")
    return None






# Carregar o shapefile
shapefile_path = 'bahia.shp'
gdf = gpd.read_file(shapefile_path)


# Carregar os dados do arquivo Excel
file_path = "relatorio.xlsx"
sheet_name = "CLIMA"  # Substitua pelo nome correto da planilha, se necessário
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Coordenadas das estações
obs_latitudes = df["latitude"]
obs_longitudes = df["longitude"]

# Valores a serem interpolados (neste exemplo, usaremos a coluna "per_dados_validos")
values_to_interpolate = df["Media"]*365


modelos=[ "linear","power","gaussian","spherical", "exponential", "hole-effect" ]

for model in modelos:
    # interpola 
    z,grid_x,grid_y = interpola(obs_longitudes,obs_latitudes,values_to_interpolate,model)

    # plota
    plota_interp(grid_x,grid_y,z,20,'coolwarm',obs_longitudes,obs_latitudes,values_to_interpolate,"Media","interp_clima_krigging_"+model,model)

    # Salva em NetCDF
    netcdf_filename = "interp_clima_krigging_" + model + ".nc"
    save_to_netcdf(netcdf_filename, grid_x[0, :], grid_y[:, 0], "Media", z)	

