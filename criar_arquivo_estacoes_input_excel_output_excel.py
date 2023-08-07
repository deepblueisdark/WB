import pandas as pd

import subprocess
import pandas as pd

# Executar o comando na linha de comando para exportar do MDB para XLSX
comando_exportacao = "mdb-export HIDRO.mdb Estacao > estacoes.xlsx"
subprocess.run(comando_exportacao, shell=True)

# Carregar o arquivo Excel
nome_arquivo = 'estacoes.xlsx'  # Substitua pelo caminho real do arquivo
# Lista das colunas de interesse
colunas_interesse = [ 'Codigo', 'Latitude', 'Longitude','Nome','EstadoCodigo','BaciaCodigo','TipoEstacao']


# Ler o arquivo Excel e selecionar as colunas de interesse
dados = pd.read_excel(nome_arquivo, usecols=colunas_interesse)

# Filtrar linhas com valores não nulos nas colunas de interesse
dados_filtrados = dados.dropna(subset=colunas_interesse)

# Nome do arquivo de saída
nome_saida = 'lista_estacoes.xlsx'

# Salvar os dados filtrados em uma nova planilha Excel
dados_filtrados.to_excel(nome_saida, index=False)

print(f'Dados filtrados salvos em {nome_saida}')


