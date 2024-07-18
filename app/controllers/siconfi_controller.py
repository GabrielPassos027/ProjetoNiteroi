import requests
from app.models import RREO_SICONFI, RGF_SICONFI, db
import pandas as pd
import numpy as np

def fetch_siconfi_RREO_data(an_exercicio, nr_periodo, no_anexo):
    url = (f'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?'
           f'an_exercicio={an_exercicio}&nr_periodo={nr_periodo}&'
           f'co_tipo_demonstrativo=RREO&no_anexo={no_anexo}&'
           f'co_esfera=E&id_ente=33')
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        resultados_filtrados = []

        for item in items:
            resultado = {
                'conta': item.get('conta'),
                'cod_conta': item.get('cod_conta'),
                'coluna': item.get('coluna'),
                'valor': item.get('valor'),
                'exercicio': item.get('exercicio'),
                'instituicao': item.get('instituicao'),
                'id': f"{item.get('conta')}{item.get('coluna')}"
            }
            resultados_filtrados.append(resultado)
        
        return resultados_filtrados
    else:
        return []
    
def fetch_siconfi_RGF_data(an_exercicio, nr_periodo):
    url = (f'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rgf?'
           f'an_exercicio={an_exercicio}&in_periodicidade=Q&nr_periodo={nr_periodo}&'
           f'co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2002&'
           f'co_esfera=E&co_poder=E&id_ente=33')
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        resultados_filtrados = []

        for item in items:
            resultado = {
                'conta': item.get('conta'),
                'cod_conta': item.get('cod_conta'),
                'coluna': item.get('coluna'),
                'valor': item.get('valor'),
                'cod_ibge': item.get('cod_ibge'),
                'populacao': item.get('populacao'),
                'instituicao': item.get('instituicao'),
                'id': f"{item.get('conta')}{item.get('coluna')}"
            }
            resultados_filtrados.append(resultado)
        
        return resultados_filtrados
    else:
        return []

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

        # Salvar os dados no banco de dados
        for index, row in df.iterrows():
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
        print("Dados RREO salvos")
        

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