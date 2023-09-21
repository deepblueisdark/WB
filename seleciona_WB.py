import pandas as pd
import glob

# Defina o limite máximo
LIMITE_MAX = 0.80

# Lista de nomes de arquivos Excel
#arquivos_excel = ['relatorio_ana_20230630_a_19120901_e_19910101_a_20201231.xlsx', 
#'relatorio_inmet_CONV_19610101_a_20231231_e_19810101_a_20100101.xlsx', 
#'relatorio_inmet_TEL_20000523_a_20231231_e_19810101_a_20100101.xlsx']


arquivos_excel = glob.glob("./"+ "relatorio*.xlsx")



# Nome da planilha de destino
planilha_destino = 'selecao.xlsx'

# Inicialize um DataFrame vazio para armazenar os dados filtrados
dados_filtrados = pd.DataFrame()

# Loop através dos arquivos Excel
for arquivo in arquivos_excel:
    # Leia o arquivo Excel
    df = pd.read_excel(arquivo, sheet_name='CLIMA')
    
    # Filtrar os dados com base na coluna 'Perc'
    df_filtrado = df[df['Per. Dados Validos'] > LIMITE_MAX]
    
    # Concatenar os dados filtrados ao DataFrame principal
    dados_filtrados = pd.concat([dados_filtrados, df_filtrado])

# Salvar os dados filtrados em um novo arquivo Excel
dados_filtrados.to_excel(planilha_destino, index=False, sheet_name='selecao')
