import requests
from app.models import RREO_SICONFI, RGF_SICONFI, db

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

