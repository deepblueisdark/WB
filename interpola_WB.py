##-------------------------------------------------------------------------------------------------------
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
from matplotlib.colors import ListedColormap
from scipy.spatial.distance import cdist





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

def interpola_idw(obs_longitudes, obs_latitudes, values_to_interpolate, grid):
    interpolated_values = np.zeros((len(grid['lon']), len(grid['lat'])))
    
    for i in range(len(grid['lon'])):
        for j in range(len(grid['lat'])):
            point = (grid['lon'][i], grid['lat'][j])
            distances = np.sqrt((obs_longitudes - point[0])**2 + (obs_latitudes - point[1])**2)
            weights = 1.0 / (distances**2)
            interpolated_values[i, j] = np.sum(weights * values_to_interpolate) / np.sum(weights)
    
    return interpolated_values
	
	

def interpola(obs_longitudes,obs_latitudes,values_to_interpolate,variograma,grid):
    # Coordenadas da grade para interpolação (você pode ajustar isso conforme necessário)
	
	#
	# baseado nos dados brutos
	#
    #grid_latitudes = np.linspace(min(obs_latitudes), max(obs_latitudes), 100)
    #grid_longitudes = np.linspace(min(obs_longitudes), max(obs_longitudes), 100)

    #
	#  definido pelo usuario 
	#
	
    #grid_latitudes = np.linspace(-19, -8, 100)
    #grid_longitudes = np.linspace(-48, -37, 100)
  

    # Criar malha de coordenadas
    grid_x, grid_y = np.meshgrid(grid['lon'], grid['lat'])
    # Configurar o modelo de kriging
    OK = OrdinaryKriging(
         obs_longitudes,
         obs_latitudes,
         values_to_interpolate,
         variogram_model=variograma,  # Pode escolher um modelo de variograma diferente
    )

    # Realizar a interpolação
    z, ss = OK.execute("grid", grid['lon'], grid['lat'])
    return z,grid_x,grid_y

def plota_interp(grid_x,grid_y,z,niveis,colormap,obs_longitudes,obs_latitudes,valores,nomevar,nome_figura,modelo):
    # Plotar a interpolação
    #cmap = ListedColormap(['red','purple','magenta','violet','pink', 'orange','yellow', 'lime','green', 'blue','black'])
    #bounds = [ 0, 250, 500, 700,  1000, 1300, 1500,2000, 2500,3000, 3500]
    cmap = ListedColormap(['red','orange','yellow', 'lime', 'blue'])
    bounds = [ 250, 500,   1000, 1500,2000]
	
    norm = plt.Normalize(bounds[0], bounds[-1])
	
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(obs_longitudes, obs_latitudes, c=valores, cmap=cmap, norm=norm, marker="o")
    plt.contourf(grid_x, grid_y, z, levels=niveis, cmap=cmap)
    plt.scatter(obs_longitudes, obs_latitudes, c=valores, cmap=cmap, edgecolors='k')
    # Plotar o shapefile
    #gdf.plot(ax=plt.gca(), color='gray')  # Use ax=plt.gca() para sobrepor o shapefile ao scatter plot
    gdf.plot(ax=plt.gca(), edgecolor='gray', facecolor='none', lw=1)  # lw é a largura da linha da borda
    #plt.colorbar(label=nomevar)
	
	# Adicionar uma legenda de cores
    cbar = plt.colorbar(scatter)  # Use o objeto scatter como mappable
    cbar.set_label("Media", labelpad=15)
       
	
    plt.title("Interpolação com "+modelo)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.savefig(nome_figura, dpi=300, bbox_inches="tight")
    return None






# Carregar o shapefile
shapefile_path= '/mnt/e/OneDrive/OPERACIONAL/SHAPES/estadosBR/BAHIA/BAHIA.shp'
gdf = gpd.read_file(shapefile_path)
lon_min, lat_min, lon_max, lat_max = gdf.total_bounds

# Carregar os dados do arquivo Excel
file_path = "selecao.xlsx"
sheet_name = "selecao"  # Substitua pelo nome correto da planilha, se necessário
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Coordenadas das estações
obs_latitudes = df["Latitude"]
obs_longitudes = df["Longitude"]

# Valores a serem interpolados (neste exemplo, usaremos a coluna "per_dados_validos")
values_to_interpolate = df["Media"]*365


# Criar um DataFrame para o relatório
# BAHIA
grid = {
    "lat": np.linspace(-19, -8, 100),
    "lon": np.linspace(-48, -35, 100)
}

# #from shapefile
# grid = {
    # "lat": np.linspace(lat_min, lat_max, 100),
    # "lon": np.linspace(lon_min, lon_max, 100)
# }


modelos=[ "linear","power","gaussian","spherical", "exponential", "hole-effect" ]

for model in modelos:
    # interpola 
    z,grid_x,grid_y = interpola(obs_longitudes,obs_latitudes,values_to_interpolate,model,grid)

    # plota
    plota_interp(grid_x,grid_y,z,20,'coolwarm',obs_longitudes,obs_latitudes,values_to_interpolate,"Media","interp_clima_krigging_"+model,"Krigging "+model)

    # Salva em NetCDF
    netcdf_filename = "interp_clima_krigging_" + model + ".nc"
    save_to_netcdf(netcdf_filename, grid_x[0, :], grid_y[:, 0], "Media", z)	


# Interpolação IDW
z_idw = interpola_idw(obs_longitudes, obs_latitudes, values_to_interpolate, grid)

# Combinar as interpolações Kriging e IDW
#z_final = (z + z_idw) / 2.0

# Plota e salva
plota_interp(grid_x, grid_y, z_idw, 20, 'coolwarm', obs_longitudes, obs_latitudes, values_to_interpolate, "Media", "interp_clima_idw", "IDW")

# Salva em NetCDF
netcdf_filename = "interp_clima_idw.nc"
save_to_netcdf(netcdf_filename, grid_x[0, :], grid_y[:, 0], "Media", z_idw)