import subprocess
import pandas as pd

# Executar o comando na linha de comando para exportar do MDB para CSV
comando_exportacao = "mdb-export HIDRO.mdb Estacao > estacoes.csv"
subprocess.run(comando_exportacao, shell=True)

# Nome do arquivo CSV de saída
nome_arquivo_csv = 'estacoes.csv'

# Lista das colunas de interesse
colunas_interesse = [ 'Codigo', 'Latitude', 'Longitude','Nome','EstadoCodigo','BaciaCodigo','TipoEstacao']


# Ler o arquivo CSV e selecionar as colunas de interesse
dados = pd.read_csv(nome_arquivo_csv, usecols=colunas_interesse)

# Filtrar linhas com valores não nulos nas colunas de interesse
dados_filtrados = dados.dropna(subset=colunas_interesse)

# Nome do arquivo Excel de saída
nome_saida_excel = 'lista_estacoes.xlsx'

# Salvar os dados filtrados em um novo arquivo Excel
dados_filtrados.to_excel(nome_saida_excel, index=False)

print(f'Dados filtrados salvos em {nome_saida_excel}')
