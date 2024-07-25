import requests
from app.models import SiconfiDataRREO,SiconfiDataRGF, RREO_SICONFI, RGF_SICONFI, db
import pandas as pd
import numpy as np
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import os
import getpass

# Configuração do log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração de retries para requests
session = requests.Session()
retry = Retry(
    total=5,
    read=5,
    connect=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# def fetch_ente():
#     url = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes"
#     response = requests.get(url, timeout=10)
#     if response.status_code == 200:
#         data = response.json()
#         municipios_rio = [
#             "Niterói", "Angra dos Reis", "Aperibé", "Araruama", "Areal", "Armação dos Búzios",
#             "Arraial do Cabo", "Barra do Piraí", "Barra Mansa", "Belford Roxo", "Bom Jardim",
#             "Bom Jesus do Itabapoana", "Cabo Frio", "Cachoeiras de Macacu", "Cambuci", 
#             "Campos dos Goytacazes", "Paraty", "Paty do Alferes", "Petrópolis", "Pinheiral", 
#             "Piraí", "Porciúncula", "Porto Real", "Quatis", "Queimados", "Quissamã", "Resende", 
#             "Rio Bonito", "Rio Claro", "Rio das Flores", "Rio das Ostras", "Rio de Janeiro", 
#             "Santa Maria Madalena", "Santo Antônio de Pádua", "São Fidélis", 
#             "São Francisco de Itabapoana", "São Gonçalo", "São João da Barra", 
#             "São João de Meriti", "São José de Ubá", "São José do Vale do Rio Preto", 
#             "São Pedro da Aldeia", "São Sebastião do Alto", "Sapucaia", "Saquarema", 
#             "Seropédica", "Silva Jardim", "Sumidouro", "Tanguá", "Teresópolis", 
#             "Trajano de Moraes", "Três Rios", "Valença", "Varre-Sai", "Vassouras", "Volta Redonda"
#         ]
#         municipios_nacionais = {
#             "Vila Velha": "3205200", 
#             "Vitória": "3205309", 
#             "Maringá": "4115200", 
#             "Uberlândia": "3170206", 
#             "São José dos Campos": "3549904", 
#             "Londrina": "4113700", 
#             "Santo André": "3547809", 
#             "Santos": "3548500", 
#             "Florianópolis": "4205407", 
#             "Joinville": "4209102", 
#             "São Caetano do Sul": "3548807"
#         }

#         # Filtra os dados para obter apenas os municípios do Rio de Janeiro (UF = RJ)
#         filtered_data = [item for item in data["items"] if item["ente"] in municipios_rio and item["uf"] == "RJ"]
        
#         # Adiciona os municípios nacionais à lista filtrada
#         for nome, cod_ibge in municipios_nacionais.items():
#             filtered_data.append({
#                 "ente": nome,
#                 "cod_ibge": cod_ibge, 
#             })
        
#         print(f"Total de municípios encontrados: {len(filtered_data)}")
#         return filtered_data
#     else:
#         print("Erro ao buscar dados dos entes.")
#         return None

def fetch_ente():
    url = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        municipios_rio = [
            "Niterói", "Angra dos Reis", "Aperibé", "Araruama", "Areal", "Armação dos Búzios",
            "Arraial do Cabo", "Barra do Piraí", "Barra Mansa", "Belford Roxo", "Bom Jardim",
            "Bom Jesus do Itabapoana", "Cabo Frio", "Cachoeiras de Macacu", "Cambuci", 
            "Campos dos Goytacazes", "Paraty", "Paty do Alferes", "Petrópolis", "Pinheiral", 
            "Piraí", "Porciúncula", "Porto Real", "Quatis", "Queimados", "Quissamã", "Resende", 
            "Rio Bonito", "Rio Claro", "Rio das Flores", "Rio das Ostras", "Rio de Janeiro", 
            "Santa Maria Madalena", "Santo Antônio de Pádua", "São Fidélis", 
            "São Francisco de Itabapoana", "São Gonçalo", "São João da Barra", 
            "São João de Meriti", "São José de Ubá", "São José do Vale do Rio Preto", 
            "São Pedro da Aldeia", "São Sebastião do Alto", "Sapucaia", "Saquarema", 
            "Seropédica", "Silva Jardim", "Sumidouro", "Tanguá", "Teresópolis", 
            "Trajano de Moraes", "Três Rios", "Valença", "Varre-Sai", "Vassouras", "Volta Redonda"
        ]
        municipios_nacionais = {
            "Vila Velha": "3205200", 
            "Vitória": "3205309", 
            "Maringá": "4115200", 
            "Uberlândia": "3170206", 
            "São José dos Campos": "3549904", 
            "Londrina": "4113700", 
            "Santo André": "3547809", 
            "Santos": "3548500", 
            "Florianópolis": "4205407", 
            "Joinville": "4209102", 
            "São Caetano do Sul": "3548807"
        }

        # Filtra os dados para obter apenas os municípios do Rio de Janeiro (UF = RJ)
        filtered_data = [item for item in data["items"] if item["ente"] in municipios_rio and item["uf"] == "RJ"]
        
        # Adiciona os municípios nacionais à lista filtrada
        for nome, cod_ibge in municipios_nacionais.items():
            filtered_data.append({
                "ente": nome,
                "cod_ibge": cod_ibge, 
            })
        
        print(f"Total de municípios encontrados: {len(filtered_data)}")
        return filtered_data
    else:
        print("Erro ao buscar dados dos entes.")
        return None

def fetch_siconfi_RREO_data(app):
    with app.app_context():
        entes = fetch_ente()
        if entes:
            total_entries = 0
            for an_exercicio in range(2019, 2025):
                for nr_periodo in range(1, 7):
                    for no_anexo in ["RREO-Anexo%2001", "RREO-Anexo%2002", "RREO-Anexo%2004", "RREO-Anexo%2006", "RREO-Anexo%2014"]:
                        for ente in entes:
                            cod_ibge = ente['cod_ibge']
                            url = (f"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?"
                                   f"an_exercicio={an_exercicio}&nr_periodo={nr_periodo}&co_tipo_demonstrativo=RREO&"
                                   f"no_anexo={no_anexo}&co_esfera=M&id_ente={cod_ibge}")
                            try:
                                response = session.get(url, timeout=10)
                                if response.status_code == 200:
                                    data = response.json()
                                    items = data.get('items', [])
                                    logger.info(f"Processando {len(items)} itens para o município com código IBGE {cod_ibge}, exercício {an_exercicio}, período {nr_periodo}, anexo {no_anexo}")

                                    for item in items:
                                        exists = SiconfiDataRREO.query.filter_by(
                                            instituicao=item.get('instituicao'),
                                            codIBGE=item.get('cod_ibge'),
                                            uf=item.get('uf'),
                                            coluna=item.get('coluna'),
                                            conta=item.get('conta'),
                                            idConta=item.get('cod_conta'),
                                            valor=item.get('valor'),
                                            exercicio=item.get('exercicio'),
                                            periodo=item.get('periodo'),
                                            anexo=item.get('anexo')
                                        ).first()
                                        
                                        if not exists:
                                            new_entry = SiconfiDataRREO(
                                                instituicao=item.get('instituicao'),
                                                codIBGE=item.get('cod_ibge'),
                                                uf=item.get('uf'),
                                                coluna=item.get('coluna'),
                                                conta=item.get('conta'),
                                                idConta=item.get('cod_conta'),
                                                valor=item.get('valor'),
                                                exercicio=item.get('exercicio'),
                                                periodo=item.get('periodo'),
                                                anexo=item.get('anexo')
                                            )
                                            db.session.add(new_entry)
                                            total_entries += 1
                                        # else:
                                        #     logger.info(f"Dado já inserido para {item.get('instituicao')} no período {nr_periodo}")
                                else:
                                    logger.error(f"Erro na solicitação para o código IBGE {cod_ibge}: {response.status_code}")
                            except requests.exceptions.RequestException as e:
                                logger.error(f"Erro na solicitação para o código IBGE {cod_ibge}: {str(e)}")
                            except Exception as e:
                                logger.error(f"Erro ao salvar os dados no banco de dados: {str(e)}")
                            time.sleep(3)
                    db.session.commit()
                    logger.info(f"Dados RREO salvos para o período {nr_periodo}. Total de entradas adicionadas: {total_entries}")
            logger.info(f"Dados RREO salvos. Total de entradas adicionadas: {total_entries}")
        else:
            logger.error("Nenhum ente encontrado.")





    
def fetch_siconfi_RGF_data(app):
    with app.app_context():
        entes = fetch_ente()
        if entes:
            total_entries = 0
            for an_exercicio in range(2019, 2025):
                for nr_periodo in range(1, 4):
                    for no_anexo in ["RGF-Anexo%2002"]:
                        for ente in entes:
                            cod_ibge = ente['cod_ibge']

                            url = (f'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rgf?'
                                    f'an_exercicio={an_exercicio}&in_periodicidade=Q&nr_periodo={nr_periodo}&'
                                    f'co_tipo_demonstrativo=RGF&no_anexo={no_anexo}&'
                                    f'co_esfera=M&co_poder=E&id_ente={cod_ibge}')
                            # logger.info(f"URL solicitada: {url}")
                            try:
                                response = session.get(url, timeout=10)
                                if response.status_code == 200:
                                    data = response.json()
                                    items = data.get('items', [])
                                    logger.info(f"Processando {len(items)} itens para o município com código IBGE {cod_ibge}, exercício {an_exercicio}, período {nr_periodo}, anexo {no_anexo}")

                                    for item in items:
                                        # Verifica se o registro já existe no banco de dados
                                        exists = SiconfiDataRGF.query.filter_by(
                                            instituicao=item.get('instituicao'),
                                            codIBGE=item.get('cod_ibge'),
                                            uf=item.get('uf'),
                                            coluna=item.get('coluna'),
                                            conta=item.get('conta'),
                                            idConta=item.get('cod_conta'),
                                            valor=item.get('valor'),
                                            exercicio=item.get('exercicio'),
                                            periodo=item.get('periodo'),
                                            anexo=item.get('anexo')
                                        ).first()
                                        
                                        if not exists:
                                            new_entry = SiconfiDataRGF(
                                                instituicao=item.get('instituicao'),
                                                codIBGE=item.get('cod_ibge'),
                                                uf=item.get('uf'),
                                                coluna=item.get('coluna'),
                                                conta=item.get('conta'),
                                                idConta=item.get('cod_conta'),
                                                valor=item.get('valor'),
                                                exercicio=item.get('exercicio'),
                                                periodo=item.get('periodo'),
                                                anexo=item.get('anexo')
                                            )
                                            db.session.add(new_entry)
                                            total_entries += 1
                                        # else:
                                        #     print("Dado já inserido")
                                else:
                                    logger.error(f"Erro na solicitação para o código IBGE {cod_ibge}: {response.status_code}")
                            except requests.exceptions.RequestException as e:
                                logger.error(f"Erro na solicitação para o código IBGE {cod_ibge}: {str(e)}")
                            time.sleep(3)
            db.session.commit()
            logger.info(f"Dados RGF salvos. Total de entradas adicionadas: {total_entries}")
        else:
            logger.error("Nenhum ente encontrado.")


# def save_rreo_data_to_db(app, file_path):
#     # Inicializar o contexto do aplicativo
#     with app.app_context():
#         # Carregar o CSV
#         lista = ["a", "b", "c", "d", "e", "f", "g", "h"]
#         df = pd.read_csv(file_path, names=lista, sep=';', encoding='latin-1')
        
#         # Extração das informações
#         exercicio = df.loc[0]['a'].replace('Exercício: ', '')
#         periodo = df.loc[1]['a'].replace('Período: ', '')
#         anexo = df.loc[3]['a']
#         tabela = df.loc[4]['a'].replace('Tabela: ', '')
        
#         # Ajuste do DataFrame
#         df = df.iloc[5:]
#         df.columns = df.iloc[0].tolist()
#         df = df[1:]
#         df['Exercicio'] = exercicio
#         df['Periodo'] = periodo
#         df['Anexo'] = anexo
#         df['Tabela'] = tabela
        
#         # Substituir valores inválidos por None
#         df = df.replace({np.nan: None})
#         df['Valor'] = df['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)
        
#         # Gerar e salvar CSV na área de trabalho
#         user = getpass.getuser()
#         desktop_path = os.path.join(f"C:/Users/{user}/Desktop", 'RREO_Uploads')
#         os.makedirs(desktop_path, exist_ok=True)
#         output_csv_path = os.path.join(desktop_path, f'arquivo_rreo_editado_{pd.Timestamp.now().strftime("%d%m%Y_%H%M%S")}.csv')
#         df.to_csv(output_csv_path, index=False, sep=';', encoding='latin-1')
#         print(f"CSV gerado e salvo em: {output_csv_path}")
        
#         # Salvar os dados no banco de dados
#         for index, row in df.iterrows():
#             rreo_record = RREO_SICONFI(
#                 instituicao=row['Instituição'],
#                 codIBGE=row['Cod.IBGE'],
#                 uf=row['UF'],
#                 coluna=row['Coluna'],
#                 conta=row['Conta'],
#                 idConta=row['Identificador da Conta'],
#                 valor=row['Valor'],
#                 exercicio=row['Exercicio'],
#                 periodo=row['Periodo'],
#                 anexo=row['Anexo'],
#                 tabela=row['Tabela']
#             )
#             db.session.add(rreo_record)
#         db.session.commit()
#         print("Dados RREO salvos no banco de dados")




def save_rreo_data_to_db(app, file_path):
    # Inicializar o contexto do aplicativo
    with app.app_context():
        # Carregar o CSV
        lista = ["a", "b", "c", "d", "e", "f", "g", "h"]
        df = pd.read_csv(file_path, names=lista, sep=';', encoding='latin-1')
        
        # Extração das informações
        exercicio = df.loc[0]['a'].replace('Exercício: ', '')
        periodo = df.loc[1]['a'].replace('Período: ', '')
        anexo = df.loc[3]['a']
        tabela = df.loc[4]['a'].replace('Tabela: ', '')
        
        # Ajuste do DataFrame
        df = df.iloc[5:]
        df.columns = df.iloc[0].tolist()
        df = df[1:]
        df['Exercicio'] = exercicio
        df['Periodo'] = periodo
        df['Anexo'] = anexo
        df['Tabela'] = tabela
        
        # Substituir valores inválidos por None
        df = df.replace({np.nan: None})
        df['Valor'] = df['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)
        
        # Obter os municípios de interesse
        municipios_interesse = fetch_ente()
        municipios_ibge = {str(item['cod_ibge']): item['ente'] for item in municipios_interesse}  # Converter o código IBGE para string
        
        # Filtrar o DataFrame para incluir apenas os municípios de interesse
        df_filtrado = df[df['Cod.IBGE'].astype(str).isin(municipios_ibge.keys())]  # Converter o código IBGE do DataFrame para string
        
        # Verificação e depuração
        print("Municípios de interesse:")
        for municipio in municipios_interesse:
            print(municipio)
        
        print("\nCódigos IBGE de interesse:")
        print(municipios_ibge)
        
        print("\nCódigos IBGE presentes no DataFrame filtrado:")
        print(df_filtrado['Cod.IBGE'].unique())

        # Comparativo
        print("\nComparativo:")
        total_municipios = len(municipios_interesse)
        total_cod_interesse = len(municipios_ibge)
        total_cod_encontrados = len(df_filtrado['Cod.IBGE'].unique())
        
        print(f"Total de municípios da função ente: {total_municipios}")
        print(f"Total de códigos IBGE de interesse: {total_cod_interesse}")
        print(f"Total de códigos IBGE encontrados: {total_cod_encontrados}")
        
        # Identificar municípios não encontrados
        cod_ibge_encontrados = set(df_filtrado['Cod.IBGE'].astype(str).unique())  # Converter o código IBGE para string
        cod_ibge_nao_encontrados = set(municipios_ibge.keys()) - cod_ibge_encontrados
        
        municipios_nao_encontrados = {cod: municipios_ibge[cod] for cod in cod_ibge_nao_encontrados}
        
        print("\nMunicípios de interesse não encontrados no DataFrame:")
        for cod_ibge, nome_municipio in municipios_nao_encontrados.items():
            print(f"{nome_municipio} (Código IBGE: {cod_ibge})")
        
        # Procurar novamente os dados faltantes na coluna Instituição e adicioná-los ao DataFrame filtrado
        for cod_ibge, nome_municipio in municipios_nao_encontrados.items():
            municipio_uf = f"{nome_municipio} - {cod_ibge[:2]}"  # Adiciona a UF à busca
            df_novos_dados = df[df['Instituição'].str.contains(municipio_uf, case=False, na=False)]
            df_filtrado = pd.concat([df_filtrado, df_novos_dados])
        
        # Gerar e salvar CSV na área de trabalho
        user = getpass.getuser()
        desktop_path = os.path.join(f"C:/Users/{user}/Desktop", 'RREO_Uploads')
        os.makedirs(desktop_path, exist_ok=True)
        output_csv_path = os.path.join(desktop_path, f'arquivo_rreo_editado_{pd.Timestamp.now().strftime("%d%m%Y_%H%M%S")}.csv')
        df_filtrado.to_csv(output_csv_path, index=False, sep=';', encoding='latin-1')
        print(f"CSV gerado e salvo em: {output_csv_path}")
        
        # Salvar os dados no banco de dados
        for index, row in df_filtrado.iterrows():
            rreo_record = RREO_SICONFI(
                instituicao=row['Instituição'],
                codIBGE=row['Cod.IBGE'],
                uf=row['UF'],
                coluna=row['Coluna'],
                conta=row['Conta'],
                idConta=row['Identificador da Conta'],
                valor=row['Valor'],
                exercicio=row['Exercicio'],
                periodo=row['Periodo'],
                anexo=row['Anexo'],
                tabela=row['Tabela']
            )
            db.session.add(rreo_record)
        db.session.commit()
        print("Dados RREO salvos no banco de dados")

# def save_rreo_data_to_db(app, file_path):
#     # Inicializar o contexto do aplicativo
#     with app.app_context():
#         # Carregar o CSV diretamente
#         df = pd.read_csv(file_path, sep=';', encoding='latin-1')

#         # Substituir valores inválidos por None
#         df = df.replace({pd.NA: None, pd.NaT: None})

#         # Salvar os dados no banco de dados
#         for index, row in df.iterrows():
#             rreo_record = RREO_SICONFI(
#                 instituicao=row.get('Instituição'),
#                 codIBGE=row.get('Cod.IBGE'),
#                 uf=row.get('UF'),
#                 coluna=row.get('Coluna'),
#                 conta=row.get('Conta'),
#                 idConta=row.get('Identificador da Conta'),
#                 valor=row.get('Valor'),
#                 exercicio=row.get('Exercicio'),
#                 periodo=row.get('Periodo'),
#                 anexo=row.get('Anexo'),
#                 tabela=row.get('Tabela')
#             )
#             db.session.add(rreo_record)
        
#         db.session.commit()
#         print("Dados RREO salvos no banco de dados")
        

def save_rgf_data_to_db(app, file_path):
    with app.app_context():
        # Carregar o CSV
        lista = ["a", "b", "c", "d", "e", "f", "g", "h","i"]
        df = pd.read_csv(file_path, names=lista, sep=';', encoding='latin-1')
        
        # Extração das informações
        exercicio = df.loc[0]['a'].replace('Exercício: ', '')
        periodo = df.loc[1]['a'].replace('Período: ', '')
        anexo = df.loc[3]['a']
        tabela = df.loc[4]['a'].replace('Tabela: ', '')

        # Ajuste do DataFrame
        df = df.iloc[5:]
        df.columns = df.iloc[0].tolist()
        df = df[1:]
        df['Exercicio'] = exercicio
        df['Periodo'] = periodo
        df['Anexo'] = anexo
        df['Tabela'] = tabela
        
        # Substituir valores inválidos por None
        df = df.replace({np.nan: None})
        df['Valor'] = df['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)

        for index, row in df.iterrows():
            rgf_record = RGF_SICONFI(
                instituicao=row['Instituição'],
                codIBGE=row['Cod.IBGE'],
                uf=row['UF'],
                coluna=row['Coluna'],
                conta=row['Conta'],
                idConta=row['Identificador da Conta'],
                valor=row['Valor'],
                exercicio=row['Exercicio'],
                periodo=row['Periodo'],
                anexo=row['Anexo'],
                tabela=row['Tabela']
            )
            db.session.add(rgf_record)
        db.session.commit()
        print("Dados RGF salvos")