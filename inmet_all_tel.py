#-------------------------------------------------------------------------------------------------------
#
#      script tratamento dos dados do INMET TELEMETRICAS
#
#--------------------------------------------------------------------------------------------------------
# by reginaldo.venturadesa@gmail.com  em agosto de 2023 
#
#  
#
#---------------------------------------------------------------------------------------------------------
import pandas as pd
import glob
import xlsxwriter
from datetime import datetime

# Função para calcular a média no período
def calcular_varios_periodo(df, inicio, fim):
    periodo = df[(df['Data Medicao'] >= inicio) & (df['Data Medicao'] <= fim)]
    # Calcular os campos adicionais
    sem_chuva = periodo[periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'] == 0.0].shape[0]
    com_chuva = periodo[periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'] > 0.0].shape[0]
    sem_dados = periodo[periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'].isnull()].shape[0]
    soma_da_chuva = periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'].sum()
    num_dados_totais = len(df)
    num_dias = (fim - inicio).days  # Calcular número de dias
    num_dados_validos=sem_chuva+com_chuva
    per_semchuva=sem_chuva/num_dados_totais
    per_comchuva=com_chuva/num_dados_totais
    per_semdados=sem_dados/num_dados_totais
    per_dados_validos=num_dados_validos/num_dados_totais 
 
    return sem_chuva,com_chuva,sem_dados,soma_da_chuva,num_dados_totais,num_dias,num_dados_validos,per_semchuva,per_comchuva,per_semdados,per_dados_validos 
   




# Função para calcular a média no período
def calcular_media_periodo(df, inicio, fim):
    periodo = df[(df['Data Medicao'] >= inicio) & (df['Data Medicao'] <= fim)]
    return periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'].mean()

# Função para calcular a soma no período
def calcular_maximo_periodo(df, inicio, fim):
    periodo = df[(df['Data Medicao'] >= inicio) & (df['Data Medicao'] <= fim)]
    return periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'].max()

# Função para calcular a soma no período
def calcular_soma_periodo(df, inicio, fim):
    periodo = df[(df['Data Medicao'] >= inicio) & (df['Data Medicao'] <= fim)]
    return periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'].sum()

# Função para calcular a contagem no período
def calcular_conta_periodo(df, inicio, fim):
    periodo = df[(df['Data Medicao'] >= inicio) & (df['Data Medicao'] <= fim)]
    return periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'].count()

# Função para calcular a desvio padrao no período
def calcular_desvpad_periodo(df, inicio, fim):
    periodo = df[(df['Data Medicao'] >= inicio) & (df['Data Medicao'] <= fim)]
    return periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'].std()

	
# Função para calcular a variancia no período
def calcular_variancia_periodo(df, inicio, fim):
    periodo = df[(df['Data Medicao'] >= inicio) & (df['Data Medicao'] <= fim)]
    return periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'].var()


def calcular_percentil_periodo(df, inicio, fim):
    periodo = df[(df['Data Medicao'] >= inicio) & (df['Data Medicao'] <= fim)]

    # Filtrar valores acima de 0.0 antes de calcular os percentis
    valores_acima_de_zero = periodo[periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'] > 0.0]
    
    percentis_dinamico = valores_acima_de_zero['PRECIPITACAO_TOTAL_HORARIO(mm)'].quantile([0.05, 0.10, 0.20, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
    return percentis_dinamico
	
	
# Caminho para a pasta contendo os arquivos CSV
pasta_csv = "./TELEMETRICAS/"

# Obtém a lista de arquivos CSV na pasta
arquivos_csv = glob.glob(pasta_csv + "*.csv")

# Criar um DataFrame para os relatórios
relatorios_total = pd.DataFrame()
relatorios_total2 = pd.DataFrame()

# Loop pelos arquivos CSV
for arquivo_csv in arquivos_csv:
    # Lê o arquivo original
    with open(arquivo_csv, 'r') as f:
        lines = f.readlines()
        #print(lines[0:10])
    # Extrair informações do cabeçalho
    cabecalho = [line.strip() for line in lines[0:10]]  # Extrair linhas 3 a 10 (0-indexed)
    #print(cabecalho)
    nome = cabecalho[0].split(": ")[1]
    codigo_estacao = cabecalho[1].split(": ")[1]
    latitude = float(cabecalho[2].split(": ")[1])
    longitude = float(cabecalho[3].split(": ")[1])
    altitude = float(cabecalho[4].split(": ")[1])
    situacao = cabecalho[5].split(": ")[1]

    
  
    # Encontra a linha com o cabeçalho original e substitui pelo novo cabeçalho
    ##lines[10] = "Data Medicao;Hora Medicao;PRECIPITACAO_TOTAL_HORARIO(mm);\n"
    lines[10] = "Data Medicao;Hora Medicao;PRECIPITACAO_TOTAL_HORARIO(mm);TEMPMAX;TEMPMIN;\n"

    # Escreve o resultado em um novo arquivo
    novo_arquivo_csv = "novo_arquivo.csv"
    with open(novo_arquivo_csv, 'w') as f:
        f.writelines(lines)

    # Leitura do arquivo CSV usando Pandas
    df = pd.read_csv(novo_arquivo_csv, sep=';', skiprows=10, parse_dates=[0], na_values=['null'])


    # Converte a coluna 'Data Medicao' para o formato de data
    df['Data Medicao'] = pd.to_datetime(df['Data Medicao'])

    df['PRECIPITACAO_TOTAL_HORARIO(mm)'] = pd.to_numeric(df['PRECIPITACAO_TOTAL_HORARIO(mm)'], errors='coerce')

    # Agrupar por mês e ano e calcular a soma mensal de 'Chuva'
    df_monthly = df.groupby([df['Data Medicao'].dt.year, df['Data Medicao'].dt.month])['PRECIPITACAO_TOTAL_HORARIO(mm)'].sum()

    # Renomear índices para mês e ano
    df_monthly.index.names = ['Ano', 'Mês']

    # Calcular o número de dias com chuva, sem chuva e sem dados
    df['Tipo de Chuva'] = pd.cut(df['PRECIPITACAO_TOTAL_HORARIO(mm)'], bins=[-1, 0, float('inf')], labels=['SEMDADOS', 'SEMCHUVA'])
    df['Tipo de Chuva'] = df['Tipo de Chuva'].cat.add_categories(['COMCHUVA'])
    df['Tipo de Chuva'].fillna('COMCHUVA', inplace=True)
    # Obter o ano inicial e final
    ano_inicial = df['Data Medicao'].dt.year.min()
    ano_final = df['Data Medicao'].dt.year.max()
    data_inicial = df['Data Medicao'].min()
    data_final = df['Data Medicao'].max()
	
    # Calcular os campos adicionais
    # sem_chuva = df[df['PRECIPITACAO_TOTAL_HORARIO(mm)'] == 0.0].shape[0]
    # com_chuva = df[df['PRECIPITACAO_TOTAL_HORARIO(mm)'] > 0.0].shape[0]
    # sem_dados = df[df['PRECIPITACAO_TOTAL_HORARIO(mm)'].isnull()].shape[0]
    # soma_da_chuva = df['PRECIPITACAO_TOTAL_HORARIO(mm)'].sum()
    
    sem_chuva,com_chuva,sem_dados,soma_da_chuva,num_dados_totais,num_dias,num_dados_validos,per_semchuva,per_comchuva,per_semdados,per_dados_validos  =calcular_varios_periodo(df, data_inicial, data_final) 
    
	
    # Group by and unstack
    df_daily_counts = df.groupby([df['Data Medicao'].dt.year, df['Data Medicao'].dt.month, 'Tipo de Chuva']).size().unstack(fill_value=0)

    # # Salvar os resultados em um arquivo Excel separado
    # saida_excel = arquivo_csv.replace('.csv', '_somas_mensais.xlsx')
    # with pd.ExcelWriter(saida_excel) as writer:
        # df_monthly.reset_index().to_excel(writer, sheet_name='Somas Mensais', index=False)
        # df_daily_counts.to_excel(writer, sheet_name='Somas Mensais', startcol=3, index=False)

    # print("Arquivo Excel gerado com sucesso:", saida_excel)

    # num_dados_totais = len(df)
    # num_dias = (data_final - data_inicial).days  # Calcular número de dias
    # num_dados_validos=sem_chuva+com_chuva
    
    # per_semchuva=sem_chuva/num_dados_totais
    # per_comchuva=com_chuva/num_dados_totais
    # per_semdados=sem_dados/num_dados_totais
    # per_dados_validos=num_dados_validos/num_dados_totais 
    
    
    

    media_chuva = calcular_media_periodo(df, data_inicial,data_final)
    desvpad_chuva = calcular_desvpad_periodo(df, data_inicial,data_final)
    var_chuva = calcular_variancia_periodo(df, data_inicial,data_final)
    max_chuva = calcular_maximo_periodo(df, data_inicial,data_final)
    #periodo = df[(df['Data Medicao'] >= data_inicial) & (df['Data Medicao'] <= data_final)]
    #valores_acima_de_zero = periodo[periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'] > 0.0]
    #percentis= valores_acima_de_zero['PRECIPITACAO_TOTAL_HORARIO(mm)'].quantile([0.05, 0.10, 0.20, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
    percentis=calcular_percentil_periodo(df, data_inicial, data_final) 
    
    #---------------------------------------
	#
	# definidno periodos especiais 
	#
	#
    inicio='2000-01-01' 
    fim='2020-12-31' 
	
	
	
	
    # Converter as strings de data em objetos datetime
    data1 = datetime.strptime(inicio, "%Y-%m-%d")
    data2 = datetime.strptime(fim, "%Y-%m-%d")
    
    xsem_chuva,xcom_chuva,xsem_dados,xsoma_da_chuva,xnum_dados_totais,xnum_dias,xnum_dados_validos,xper_semchuva,xper_comchuva,xper_semdados,xper_dados_validos  =calcular_varios_periodo(df,data1, data2) 
    xmedia_chuva = calcular_media_periodo(df, data1,data2)
    xdesvpad_chuva = calcular_desvpad_periodo(df, data1,data2)
    xvar_chuva = calcular_variancia_periodo(df, data1,data2)
    xmax_chuva = calcular_maximo_periodo(df, data1,data2)
    #periodo = df[(df['Data Medicao'] >= data1) & (df['Data Medicao'] <= data2)]
    #valores_acima_de_zero = periodo[periodo['PRECIPITACAO_TOTAL_HORARIO(mm)'] > 0.0]
    #percentis= valores_acima_de_zero['PRECIPITACAO_TOTAL_HORARIO(mm)'].quantile([0.05, 0.10, 0.20, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
    xpercentis=calcular_percentil_periodo(df, data1, data2) 
   
    

    # Criar um DataFrame para o relatório
    relatorio = pd.DataFrame({
        'Arquivo CSV': [arquivo_csv],
        'Nome':[nome],
        'Codigo':[codigo_estacao],
        'Longitude':[longitude],
        'Latitude':[latitude],
        'Altitude':[altitude],
 #       'Situacao':[situacao],
        'Ano Inicial': [data_inicial],
        'Ano Final': [data_final],
        'Dados_totais':[num_dados_totais],
        'Numero Dias':[num_dias],
        'Sem Chuva': [sem_chuva],
        'Com Chuva': [com_chuva],
        'Dados validos': [num_dados_validos],
        'Sem Dados': [sem_dados],
        'Per. Sem Chuva':[per_semchuva],
        'Per. Com Chuva':[per_comchuva],
        'Per. Dados Validos':[per_dados_validos],
        'Per. Sem dados:':[per_semdados],
        'Soma da Chuva': [soma_da_chuva],
        'Média chuva': [media_chuva],
        'Maximo chuva':[max_chuva],
        'Desvio padrão':[desvpad_chuva],
        'Variancia chuva':[var_chuva],      
        'P 05':[percentis[0.05]],
        'P 10':[percentis[0.10]],
        'P 20':[percentis[0.20]],
        'P 25':[percentis[0.25]],
        'P 50':[percentis[0.50]],
        'P 75':[percentis[0.75]],
        'P 90':[percentis[0.90]],
        'P 95':[percentis[0.95]],
        'P 99':[percentis[0.99]]
        
    })

    # Criar um DataFrame para o relatório
    relatorio2 = pd.DataFrame({
        'Arquivo CSV': [arquivo_csv],
        'Nome':[nome],
        'Codigo':[codigo_estacao],
        'Longitude':[longitude],
        'Latitude':[latitude],
        'Altitude':[altitude],
 #       'Situacao':[situacao],
        'Ano Inicial': [data1],
        'Ano Final': [data2],
        'Dados_totais':[xnum_dados_totais],
        'Numero Dias':[xnum_dias],
        'Sem Chuva': [xsem_chuva],
        'Com Chuva': [xcom_chuva],
        'Dados validos': [xnum_dados_validos],
        'Sem Dados': [xsem_dados],
        'Per. Sem Chuva':[xper_semchuva],
        'Per. Com Chuva':[xper_comchuva],
        'Per. Dados Validos':[xper_dados_validos],
        'Per. Sem dados:':[xper_semdados],
        'Soma da Chuva': [xsoma_da_chuva],
        'Média chuva': [xmedia_chuva],
        'Maximo chuva':[xmax_chuva],
        'Desvio padrão':[xdesvpad_chuva],
        'Variancia chuva':[xvar_chuva],      
        'P 05':[xpercentis[0.05]],
        'P 10':[xpercentis[0.10]],
        'P 20':[xpercentis[0.20]],
        'P 25':[xpercentis[0.25]],
        'P 50':[xpercentis[0.50]],
        'P 75':[xpercentis[0.75]],
        'P 90':[xpercentis[0.90]],
        'P 95':[xpercentis[0.95]],
        'P 99':[xpercentis[0.99]]
        
    })

    # Adicionar o relatório ao DataFrame total
    relatorios_total = pd.concat([relatorios_total, relatorio], ignore_index=True)
    relatorios_total2 = pd.concat([relatorios_total2, relatorio2], ignore_index=True)



# Resto do seu código...

# Nome do arquivo de relatório
arquivo_relatorio = "relatorio_inmet_tel.xlsx"

# Criar um arquivo Excel com duas abas
with pd.ExcelWriter(arquivo_relatorio, engine='xlsxwriter') as writer:
    # Salvar o DataFrame total de relatórios na primeira aba
    relatorios_total.to_excel(writer, sheet_name='TODOS', index=False)
    
    # Salvar o DataFrame total de relatórios na segunda aba
    relatorios_total2.to_excel(writer, sheet_name='CLIMA', index=False)

print("Arquivo Excel de relatório gerado com sucesso:", arquivo_relatorio)

