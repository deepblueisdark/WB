#------------------------------------------------------------------------------------------
#
#   CODIGO PARA BAIXAR DADOS DO SISTEMA HIDROWEB/ANA
#  
#   AUTOR ORIGNAL: YURI MOREIRA 
#   AUTOR DAS MOFIFICAÇÕES : REGINALDO VENTURA DE SA (reginaldo.venturadesa@gmail.com) 
#         
#   versão banco mundiaL: JULHO DE 2023  
#   1) TIRAR PARTE QUE BAIXA DADOS FLUVIOMETRICOS
#   2) ADAPTAR PARA CRIAÇÃO DE CLIMATOLOGIA SEGUNDO PRODUTO 1 
#
#-----------------------------------------------------------------------------------------

import calendar
import xml.etree.ElementTree as ET

from typing import Union
from datetime import date, timedelta, datetime

import numpy as np
import pandas as pd
import requests



class ANA:
    """Classe de requisições da API da ANA."""

    url_base = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx"

    def __init__(self) -> None:
        """Inicialização da classe de consumo da API."""
        pass

    @classmethod
    def inventario(
        self,
        codigo: str = "",
        tipoest: Union[str, int] = "",
        telemetrica: Union[str, int] = 1,
    ) -> pd.DataFrame:
        """
        Obtém o inventário de postos da ANA.

        Obs: Caso nenhum parâmetro seja passado, será retornado o inventário completo.

        Parameters
        ----------
        codigo : str
            Código de 8 dígitos de um posto específico.

        tipoest : int
            Tipo de estação. (1: Fluviométrico; 2: Pluviométrico).

        telemetrica : bool
            1 caso seja desejado apenas telemétricas, 0 caso contrário. '' para obter
            todas.

        Returns
        -------
        pd.DataFrame
            Inventário de postos.
        """
        url_requisicao = f"{self.url_base}/HidroInventario?codEstDE={codigo}&codEstATE=&tpEst={tipoest}&nmEst=&nmRio=&codSubBacia=&codBacia=&nmMunicipio=&nmEstado=&sgResp=&sgOper=&telemetrica={telemetrica}"

        resposta = requests.get(url_requisicao)

        tree = ET.ElementTree(ET.fromstring(resposta.content))
        root = tree.getroot()

        estacoes = list()
        for estacao in root.iter("Table"):
            dados = {
                "latitude": [estacao.find("Latitude").text],
                "longitude": [estacao.find("Longitude").text],
                "altitude": [estacao.find("Altitude").text],
                "codigo": [estacao.find("Codigo").text],
                "nome": [estacao.find("Nome").text],
                "estado": [estacao.find("nmEstado").text],
                "municipio": [estacao.find("nmMunicipio").text],
                "responsavel": [estacao.find("ResponsavelSigla").text],
                "ultima_att": [estacao.find("UltimaAtualizacao").text],
                "tipo": [estacao.find("TipoEstacao").text],
                "data_ins": [estacao.find("DataIns").text],
                "data_alt": [estacao.find("DataAlt").text],
            }
            if telemetrica:
                dados.update(
                    {
                        "inicio_telemetria": [
                            estacao.find("PeriodoTelemetricaInicio").text
                        ],
                        "fim_telemetria": [estacao.find("PeriodoTelemetricaFim").text],
                    }
                )

            df = pd.DataFrame.from_dict(dados)
            df.set_index("codigo", inplace=True)
            estacoes.append(df)
        if len(estacoes) == 0:
            inventario=[]
            return inventario 
        else: 
           inventario = pd.concat(estacoes)

        return inventario

    def obter_chuva(
        self,
        cod_estacao: int,
        data_inicial: str = "",
        data_final: str = "",
        consistencia: int = 1,
    ) -> pd.DataFrame:
        """
        Obtém a série histórica de um posto pluviométrico.

        Caso não haja dados em algum intervalo do período solicitado, retorna todos os dados disponíveis.

        Parameters
        ----------
        cod_estacao : str
            Código da estação fluviométrica.

        data_inicial : str
            Data de início do intervalo, no formato dd/mm/yyyy.

        data_final : str
            Data final do intervalo, no formato dd/mm/yyyy.

        Returns
        -------
            pd.DataFrame: Dataframe contendo a série de vazões do posto, o nível máximo, médio e mínimo de cada mês e a consistência do dado (1: não consistido; 2: consistido)
        """
        url_requisicao = f"{self.url_base}/HidroSerieHistorica?CodEstacao={cod_estacao}&dataInicio={data_inicial}&dataFim={data_final}&tipoDados=2&nivelConsistencia="
        #print(url_requisicao)
        resposta = requests.get(url_requisicao)

        tree = ET.ElementTree(ET.fromstring(resposta.content))
        root = tree.getroot()

        df_mes = list()
        for mes in root.iter("SerieHistorica"):
            consistencia = mes.find("NivelConsistencia").text

            primeiro_dia_mes = pd.to_datetime(mes.find("DataHora").text, dayfirst=True)
            ultimo_dia_mes = calendar.monthrange(
                primeiro_dia_mes.year, primeiro_dia_mes.month
            )[1]
            lista_dias_mes = pd.date_range(
                primeiro_dia_mes, periods=ultimo_dia_mes, freq="D"
            ).tolist()

            dados, datas = [], []
            for i in range(len(lista_dias_mes)):
                datas.append(lista_dias_mes[i])
                dia = i + 1
                chuva = "Chuva{:02}".format(dia)
                dado = mes.find(chuva).text

                dados.append(dado)
            df = pd.DataFrame({'chuva': dados}, index=datas)
            df.index.name = 'data'
            df = df.assign(consistencia=consistencia)
            df_mes.append(df)

        try:
            serie = pd.concat(df_mes)
            serie.sort_index(inplace=True)
            serie['chuva'] = pd.to_numeric(serie['chuva'])
            serie = serie.set_index(["consistencia"], append=True).sort_index()
            serie = serie.reset_index().drop_duplicates(
                subset=["data"], keep="last")
            serie.set_index('data', inplace=True)
        except (ValueError):
            serie = pd.DataFrame([], columns=["chuva"])

        
        return serie

    def obter_vazoes(
        self, cod_estacao: int, data_inicial: str = "", data_final: str = ""
    ) -> pd.DataFrame:
        """
        Obtém a série histórica de um posto fluviométrico.

        Caso não haja dados em algum intervalo do período solicitado, retorna todos os dados disponíveis.

        Parameters
        ----------
        cod_estacao : str
            Código da estação fluviométrica.

        data_inicial : str
            Data de início do intervalo, no formato dd/mm/yyyy.

        data_final : str
            Data final do intervalo, no formato dd/mm/yyyy.

        Returns
        -------
            pd.DataFrame: Dataframe contendo a série de vazões do posto, o nível máximo, médio e mínimo de cada mês e a consistência do dado (1: não consistido; 2: consistido)
        """

        url_requisicao = f"{self.url_base}/HidroSerieHistorica?CodEstacao={cod_estacao}&dataInicio={data_inicial}&dataFim={data_final}&tipoDados=3&nivelConsistencia="
        #print(url_requisicao)
        resposta = requests.get(url_requisicao)

        tree = ET.ElementTree(ET.fromstring(resposta.content))
        root = tree.getroot()

        df_mes = []
        for mes in root.iter("SerieHistorica"):
            consistencia = mes.find("NivelConsistencia").text
            maxima = mes.find("Maxima").text
            minima = mes.find("Minima").text
            media = mes.find("Media").text

            primeiro_dia_mes = pd.to_datetime(mes.find("DataHora").text, dayfirst=True)
            ultimo_dia_mes = calendar.monthrange(
                primeiro_dia_mes.year, primeiro_dia_mes.month
            )[1]
            lista_dias_mes = pd.date_range(
                primeiro_dia_mes, periods=ultimo_dia_mes, freq="D"
            ).tolist()

            dados, datas = [], []
            for i in range(len(lista_dias_mes)):
                datas.append(lista_dias_mes[i])
                dia = i + 1
                vazao = "Vazao{:02}".format(dia)
                dado = mes.find(vazao).text

                dados.append(dado)
            df = pd.DataFrame({"vazoes": dados}, index=datas)
            df.index.name = 'data'
            df = df.assign(
                maxima=maxima,
                minima=minima,
                media=media,
                consistencia=consistencia,
            )
            df_mes.append(df)

        serie = pd.concat(df_mes)
        serie.sort_index(inplace=True)
        serie.vazoes = pd.to_numeric(serie.vazoes)
        serie = serie.set_index(["consistencia"], append=True).sort_index()
        serie = serie.reset_index().drop_duplicates(
                subset=["data"], keep="last")
        serie.set_index('data', inplace=True)

        return serie

    def obter_cotas(
        self, cod_estacao: int, data_inicial: str = "", data_final: str = ""
    ) -> pd.DataFrame:
        """
        Obtenção da série de cotas de um posto fluviométrico.
        Caso não haja dados em algum intervalo do período solicitado, retorna todos os dados disponíveis.

        Parameters
        ----------
        cod_estacao : str
            Código da estação fluviométrica.

        data_inicial : str
            Data de início do intervalo, no formato dd/mm/yyyy.

        data_final : str
            Data final do intervalo, no formato dd/mm/yyyy.

        Returns
        -------
            pd.DataFrame: Dataframe contendo a série de cotas, em metros, do nível de água no posto fluviométrico analisado.
        """
        url_requisicao = f"{self.url_base}/HidroSerieHistorica?CodEstacao={cod_estacao}&dataInicio={data_inicial}&dataFim={data_final}&tipoDados=1&nivelConsistencia="
        #print(url_requisicao)
        resposta = requests.get(url_requisicao)

        tree = ET.ElementTree(ET.fromstring(resposta.content))
        root = tree.getroot()

        df_mes = []
        for mes in root.iter("SerieHistorica"):
            consistencia = mes.find("NivelConsistencia").text
            primeiro_dia_mes = pd.to_datetime(mes.find("DataHora").text, dayfirst=True)
            ultimo_dia_mes = calendar.monthrange(
                primeiro_dia_mes.year, primeiro_dia_mes.month
            )[1]
            lista_dias_mes = pd.date_range(
                primeiro_dia_mes, periods=ultimo_dia_mes, freq="D"
            ).tolist()

            dados, datas = [], []
            for i in range(len(lista_dias_mes)):
                datas.append(lista_dias_mes[i])
                dia = i + 1
                cota = "Cota{:02}".format(dia)
                try:
                    dado = mes.find(cota).text
                except AttributeError:
                    dado = np.nan
                dados.append(dado)
            df = pd.DataFrame({"cota": dados}, index=datas)
            df.index.name = 'data'
            df = df.assign(consistencia=consistencia)
            df_mes.append(df)

        serie = pd.concat(df_mes)
        serie.sort_index(inplace=True)
        serie.cota = pd.to_numeric(serie.cota)
        serie.cota = serie.cota / 100
        serie = serie.set_index(["consistencia"], append=True).sort_index()
        serie = serie.reset_index().drop_duplicates(
        subset=["data"], keep="last")
        serie = serie.groupby(pd.Grouper(key='data',freq='D')).mean()
        #print(serie)
        
        return serie

header = ["codigo", "latitude", "longitude", "altitude"] 
cod_list = pd.read_csv('./postos')['Posto']
ana = ANA()
for cod in cod_list:
  juntar = []
  junta2 =[]
  a= pd.DataFrame()
  b= pd.DataFrame()
  c= pd.DataFrame()
  print(cod)
  estacao=ana.inventario(cod,2,0)
  if len(estacao) == 0:
     continue
  else:  	 
      Nome=estacao['nome'][0]
      latitude=float(estacao['latitude']) 
      longitude=float(estacao['longitude'])
      altitude=estacao['altitude'][0]g

  try:
    a = ana.obter_chuva(cod, '01/01/1900', date.today().strftime('%d/%m/%Y'))
    if not a.empty:
      juntar.append(a.drop(columns=['consistencia']))
  except:
    pass
  # try:
    # b = ana.obter_cotas(cod, '01/01/1990', date.today().strftime('%d/%m/%Y'))
    # if not b.empty:
      # print(cod)
      # juntar.append(b)
  # except:
    # pass
  # try:
    # c = ana.obter_vazoes(cod, '01/01/1990', date.today().strftime('%d/%m/%Y'))
    # if not c.empty:
      # juntar.append(c.drop(columns=['consistencia']))
  # except:
    # pass
  if juntar != []:
        arq = pd.concat(juntar, axis=1)
        arq.insert(0, 'altura', altitude)
        arq.insert(0, 'longitude', longitude)
        arq.insert(0, 'latitude', latitude)
        arq.insert(0, 'Nome', Nome)
        arq.insert(0, 'codigo', cod)

        with open(f'./{cod}.csv', 'w') as f:
            f.write("codigo {}\n".format(cod))
            f.write("Nome {}\n".format(Nome))
            f.write("latitude {}\n".format(latitude))
            f.write("longitude {}\n".format(longitude))
            f.write("altura {}\n\n".format(altitude))
            f.write("data,chuva\n")

            for idx, row in arq.iterrows():
                f.write("{},{}\n".format(idx.strftime('%Y-%m-%d'), row['chuva']))