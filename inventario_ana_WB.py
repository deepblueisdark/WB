#------------------------------------------------------------------
#
#      Faz download do invenatrio do sistema HIDROWEB 
#      gera o arquivos postos com os codigos das estações.
#
#      selecionar o codigo do estado ou pais para baixar o inventario 
#
#      
# -----------------------------------------------------------------
#
#  By reginaldo.venturadesa@gmail.com 
# 
#  2023 / agosto : criação do código 
#
#
#_----------------------------------------------------------------------
#
# TODO
# ( ) -  fazer pegar o link automaticamente. nesta fase ainda temos que copiar o link do inventario do site
#        por que ele muda toda hora. 
#
#-------------------------------------------------------------------------
#
#
#
#
#----------------------------------------------------------------------------------------
import subprocess
import pandas as pd
import requests
import zipfile
import io

#
#   LINK DO INVENTARIO 
# 
#  https://www.snirh.gov.br/hidroweb/download 
#
#  copiar o link  para a linha abaixo:
#
url = "https://www.snirh.gov.br/hidroweb/rest/api/documento/download?documentos=267"


response = requests.get(url)
if response.status_code == 200:
    with io.BytesIO(response.content) as zip_content:
        with zipfile.ZipFile(zip_content, 'r') as zip_ref:
            zip_ref.extractall("./")
        print("Arquivo descompactado com sucesso.")
else:
    print("Falha ao baixar o arquivo.")
    exit() 
	
	
	

#
# 1 = FLUVIOMETRICA
# 2 = PLUVIOMETRICA
# 
TIPOESTACAO = 2

#
# ESTADO 
# (VER ESTADO.XLSX PARA CODIGOS)
#
#
#
# Codigo	Sigla	Nome
# 1	    RO	RONDONIA
# 2	    AC	ACRE
# 3	    AM	AMAZONAS
# 4	    RR	RORAIMA
# 5	    PA	PARÃ
# 6	    AP	AMAPÃ
# 7	    MA	MARANHÃƒO
# 8	    PI	PIAUÃ
# 9	    CE	CEARÃ
# 10	RN	RIO GRANDE DO NORTE
# 11	PB	PARAÃBA
# 12	PE	PERNAMBUCO
# 13	AL	ALAGOAS
# 15	SE	SERGIPE
# 16	BA	BAHIA
# 17	MG	MINAS GERAIS
# 18	ES	ESPÃRITO SANTO
# 19	RJ	RIO DE JANEIRO
# 21	SP	SÃƒO PAULO
# 22	PR	PARANÃ
# 23	SC	SANTA CATARINA
# 24	RS	RIO GRANDE DO SUL
# 25	MT	MATO GROSSO
# 26	GO	GOIÃS
# 27	DF	DISTRITO FEDERAL
# 28	MS	MATO GROSSO DO SUL
# 29	TO	TOCANTINS
# 61	UR	URUGUAI
# 62	AR	ARGENTINA
# 63	PG	PARAGUAI
# 64	CH	CHILE
# 65	BO	BOLÃVIA
# 66	PU	PERU
# 67	CO	COLÃ”MBIA
# 68	EQ	EQUADOR
# 69	VE	VENEZUELA
# 70	GU	GUIANA
# 71	SU	SURINAME
# 72	GF	GUIANA FRANCESA

ESTADO = 16  ###16 = BAHIA 

# Executar o comando na linha de comando para exportar do MDB para CSV
comando_exportacao = "mdb-export HIDRO.mdb Estacao > estacoes.csv"
subprocess.run(comando_exportacao, shell=True)

nome_arquivo = 'estacoes.csv'

# Lista das colunas de interesse
colunas_interesse = ['Codigo', 'Latitude', 'Longitude', 'Nome', 'EstadoCodigo', 'BaciaCodigo', 'TipoEstacao']

# Ler o arquivo CSV e selecionar as colunas de interesse
dados = pd.read_csv(nome_arquivo, usecols=colunas_interesse)

# Aplicar filtro para linhas vazias apenas na coluna 'Codigo'
dados_filtrados = dados[dados['Codigo'].notna()]

# Aplicar o terceiro filtro para coluna 'TipoEstacao'
dados_filtrados = dados_filtrados[dados_filtrados['TipoEstacao'] == TIPOESTACAO]

dados_filtrados = dados_filtrados[dados_filtrados['EstadoCodigo'] == ESTADO]

# Nome do arquivo Excel de saída após o filtro
nome_saida_excel = 'lista_estacoes.xlsx'

# Salvar os dados filtrados em um novo arquivo Excel
dados_filtrados.to_excel(nome_saida_excel, sheet_name="TODOS", index=False)

print(f'Dados filtrados salvos em {nome_saida_excel}')

# Criar arquivo de texto com valores da coluna "Codigo"
nome_arquivo_texto = 'postos'
codigos_postos = dados_filtrados['Codigo'].tolist()
codigos_postos.sort()  # Classificar em ordem crescente


with open(nome_arquivo_texto, 'w') as arquivo_texto:
    arquivo_texto.write('Posto\n')
    for codigo in codigos_postos:
        arquivo_texto.write(str(codigo) + '\n')

print(f'Arquivo de texto com códigos dos postos criado: {nome_arquivo_texto}')
