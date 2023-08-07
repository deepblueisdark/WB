import subprocess

# Executar o comando na linha de comando para exportar do MDB para CSV
comando_exportacao = "mdb-export HIDRO.mdb Estacao > estacoes.csv"
subprocess.run(comando_exportacao, shell=True)

nome_arquivo = 'estacoes.csv'

# Lista das colunas de interesse
# Lista das colunas de interesse
colunas_interesse = [ 'Codigo', 'Latitude', 'Longitude','Nome','EstadoCodigo','BaciaCodigo','TipoEstacao']


# Ler o arquivo CSV e selecionar as colunas de interesse
dados_filtrados = []

with open(nome_arquivo, 'r') as arquivo_csv:
    cabecalho = arquivo_csv.readline().strip().split(',')
    col_indices = [cabecalho.index(coluna) for coluna in colunas_interesse]
    
    for linha in arquivo_csv:
        valores = linha.strip().split(',')
        if len(valores) >= max(col_indices) + 1:  # Verificar se a linha tem índices suficientes
            linha_filtrada = [valores[i] for i in col_indices]
            dados_filtrados.append(linha_filtrada)

# Nome do arquivo CSV de saída após o filtro
nome_saida = 'lista_estacoes.csv'

# Escrever os dados filtrados em um novo arquivo CSV
with open(nome_saida, 'w') as arquivo_saida:
    # Escrever o cabeçalho
    arquivo_saida.write(','.join(colunas_interesse) + '\n')
    
    # Escrever os dados filtrados
    for linha in dados_filtrados:
        arquivo_saida.write(','.join(linha) + '\n')

print(f'Dados filtrados salvos em {nome_saida}')