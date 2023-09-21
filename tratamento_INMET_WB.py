#-------------------------------------------------------------------------------------------------------
#
#      script tratamento dos dados do INMET CONvENCIONAIS 
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
    num_dados_totais = len(periodo)
    if num_dados_totais == 0:
       num_dias = (fim - inicio).days  # Calcular número de dias
       num_dados_validos=0.0
       per_semchuva=0.0
       per_comchuva=0.0
       per_semdados=0.0
       per_dados_validos=0.0
    else:      
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

def cria_saida_excel(relatorio_total,relatorio_total2,inicio_hist,final_hist,inicio_hist2,final_hist2):
    data1_str = inicio_hist.strftime("%Y%m%d")
    data2_str = final_hist.strftime("%Y%m%d")
    data3_str = inicio_hist2.strftime("%Y%m%d")
    data4_str = final_hist2.strftime("%Y%m%d")
    if (TIPO_ESTACAO == 0):
       # Crie o nome do arquivo de saída com base nas datas formatadas
       arquivo_relatorio  = f"relatorio_inmet_CONV_{data1_str}_a_{data2_str}_e_{data3_str}_a_{data4_str}.xlsx"
    else:
       # Crie o nome do arquivo de saída com base nas datas formatadas
       arquivo_relatorio  = f"relatorio_inmet_TEL_{data1_str}_a_{data2_str}_e_{data3_str}_a_{data4_str}.xlsx"
    # Criar um arquivo Excel com duas abas
    with pd.ExcelWriter(arquivo_relatorio, engine='xlsxwriter') as writer:
        # Salvar o DataFrame total de relatórios na primeira aba
        relatorios_total.to_excel(writer, sheet_name='TODOS', index=False)
    
        # Salvar o DataFrame total de relatórios na segunda aba
        relatorios_total2.to_excel(writer, sheet_name='CLIMA', index=False)

    print("Arquivo Excel de relatório gerado com sucesso:", arquivo_relatorio)
    return None 


def processa_arquivos_csv(arquivos_csv, inicio="",fim=""):
    inicio_hist=datetime.strptime("3000-01-01","%Y-%m-%d")
    final_hist=datetime.strptime("1900-01-01","%Y-%m-%d")
	# Criar um DataFrame para os relatórios
    relatorios_total = pd.DataFrame()
    relatorios_total2 = pd.DataFrame()	
    header=["Arquivo", "Nome","Codigo","Longitude","Latitude","Altititude",
    "Data Inicial", "Data Final", "Dados Totais", "Numero de Dias", "Sem Chuva", "Com Chuva", 
    "Dados Validos","Sem Dados", "Per. sem Chuva","Per. com Chuva","Per. Dados Validos","Per. Sem Dados","Soma","Media",
    "Máximo Chuva", "Desvio Padrao","Variancia","Tempo de Retorno", 
    "P05", "P10", "P20 Chuva", "P25 Chuva", "P50 Chuva", "P75 Chuva", "P90 Chuva", "P95 Chuva", "P99 Chuva"]
     

    # Loop pelos arquivos CSV
    for arquivo_csv in arquivos_csv:
        relatorio = pd.DataFrame()
        relatorio2 = pd.DataFrame()
        # Lê o arquivo original
        print(arquivo_csv)
        with open(arquivo_csv, 'r', encoding='iso-8859-1') as f:
            lines = f.readlines()

            #print(len(lines[10]))  
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
        data_inicial = cabecalho[6].split(": ")[1]
        status=len(lines[10])  
      
        # Encontra a linha com o cabeçalho original e substitui pelo novo cabeçalho
        if ( status == 59):   
            lines[10] = "Data Medicao;Hora Medicao;PRECIPITACAO_TOTAL_HORARIO(mm);\n"
        else:
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

        if (inicio == ""):
            data_inicial = df['Data Medicao'].min()
            if ( data_inicial < inicio_hist ):
                inicio_hist=data_inicial
        else:
            data_inicial = datetime.strptime(inicio, "%Y-%m-%d")
            inicio_hist=data_inicial
			
        if (fim == ""):
            data_final = df['Data Medicao'].max()
            if ( data_final > final_hist ):
               final_hist=data_final  
        else:
             data_final=datetime.strptime(fim, "%Y-%m-%d")
             final_hist=data_final 
                

        

        #
        # faz os calculos co mos dados lidos
        #
        sem_chuva,com_chuva,sem_dados,soma_da_chuva,num_dados_totais,num_dias,num_dados_validos,per_semchuva,per_comchuva,per_semdados,per_dados_validos  =calcular_varios_periodo(df, data_inicial, data_final) 
    

        media_chuva = calcular_media_periodo(df, data_inicial,data_final)
        desvpad_chuva = calcular_desvpad_periodo(df, data_inicial,data_final)
        var_chuva = calcular_variancia_periodo(df, data_inicial,data_final)
        max_chuva = calcular_maximo_periodo(df, data_inicial,data_final)
        percentis=calcular_percentil_periodo(df, data_inicial, data_final) 


        # Criar um DataFrame para o relatório
        relatorio = pd.DataFrame({
            'Arquivo': [arquivo_csv],
            'Nome':[nome],
            'Codigo':[codigo_estacao],
            'Longitude':[longitude],
            'Latitude':[latitude],
            'Altitude':[altitude],
     #       'Situacao':[situacao], =====================================> retirado por enquanto. habilite quando for util. 
            'Data Inicial': [data_inicial],
            'Data Final': [data_final],
            'Dados Totais':[num_dados_totais],
            'Numero de Dias':[num_dias],
            'Sem Chuva': [sem_chuva],
            'Com Chuva': [com_chuva],
            'Dados Validos': [num_dados_validos],
            'Sem Dados': [sem_dados],
            'Per. Sem Chuva':[per_semchuva],
            'Per. Com Chuva':[per_comchuva],
            'Per. Dados Validos':[per_dados_validos],
            'Per. Sem Dados':[per_semdados],
            'Soma': [soma_da_chuva],
            'Media': [media_chuva],
            'Maximo Chuva':[max_chuva],
            'Desvio Padrao':[desvpad_chuva],
            'Variancia':[var_chuva],      
            'P05':[percentis[0.05]],
            'P10':[percentis[0.10]],
            'P20':[percentis[0.20]],
            'P25':[percentis[0.25]],
            'P50':[percentis[0.50]],
            'P75':[percentis[0.75]],
            'P90':[percentis[0.90]],
            'P95':[percentis[0.95]],
            'P99':[percentis[0.99]]
            
        })        
        #  Adicionar o relatório ao DataFrame total
        if ( num_dados_validos != 0 ):
            relatorios_total = pd.concat([relatorios_total, relatorio], ignore_index=True)       

    
    return relatorios_total,inicio_hist,final_hist
    
    
#
#
#
#
#   
# Caminho para a pasta contendo os arquivos CSV
#
#
#
#
#
#


pasta_csv = "./INMET_TELEMETRICAS/"
TIPO_ESTACAO=1   ##  0 = CONVENCIONAL, 1=TELEMETRICA 
# Obtém a lista de arquivos CSV na pasta
arquivos_csv = glob.glob(pasta_csv + "*.csv")
relatorios_total = pd.DataFrame()
relatorios_total2 = pd.DataFrame()
relatorios_total,inicio_hist,final_hist =processa_arquivos_csv(arquivos_csv)
relatorios_total2,inicio_hist2,final_hist2  =processa_arquivos_csv(arquivos_csv,'1991-01-01','2020-12-31')
cria_saida_excel(relatorios_total,relatorios_total2,inicio_hist,final_hist,inicio_hist2,final_hist2)

pasta_csv = "./INMET_CONVENCIONAIS/"
TIPO_ESTACAO=0   ##  0 = CONVENCIONAL, 1=TELEMETRICA 
# Obtém a lista de arquivos CSV na pasta
arquivos_csv = glob.glob(pasta_csv + "*.csv")
relatorios_total,inicio_hist,final_hist =processa_arquivos_csv(arquivos_csv)
relatorios_total2,inicio_hist2,final_hist2  =processa_arquivos_csv(arquivos_csv,'1991-01-01','2020-12-31')
cria_saida_excel(relatorios_total,relatorios_total2,inicio_hist,final_hist,inicio_hist2,final_hist2)



