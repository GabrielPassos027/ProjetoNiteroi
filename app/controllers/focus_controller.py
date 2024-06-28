import requests
import json
from datetime import datetime
from flask import current_app

def fetch_selic_data():
    url_selic = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoSelic?%24format=json"
    try:
        response = requests.get(url_selic)
        response.raise_for_status()
        data = response.json().get('value', [])
        filtered_data = [entry for entry in data if datetime.strptime(entry['Data'], '%Y-%m-%d') >= datetime(2019, 1, 2)]
        sorted_data = sorted(filtered_data, key=lambda x: x['Data'], reverse=True)
        return sorted_data
    except requests.RequestException as e:
        current_app.logger.error(f"Erro ao obter dados SELIC: {e}")
        return []

def fetch_pib_data():
    url_pib = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoTrimestrais?%24format=json&%24filter=Indicador%20eq%20'PIB%20Total'"
    try:
        response = requests.get(url_pib)
        response.raise_for_status()
        data = response.json().get('value', [])
        filtered_data = [entry for entry in data if datetime.strptime(entry['Data'], '%Y-%m-%d') >= datetime(2019, 1, 2)]
        sorted_data = sorted(filtered_data, key=lambda x: x['Data'], reverse=True)
        return sorted_data
    except requests.RequestException as e:
        current_app.logger.error(f"Erro ao obter dados PIB: {e}")
        return []
    
def fetch_focus_ipca_data():
    url_ipca = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativaMercadoMensais?%24format=json&%24filter=Indicador%20eq%20'IPCA'"
    try:
        response = requests.get(url_ipca)
        response.raise_for_status()
        data = response.json().get('value', [])
        filtered_data = [entry for entry in data if datetime.strptime(entry['Data'], '%Y-%m-%d') >= datetime(2019, 1, 2)]
        sorted_data = sorted(filtered_data, key=lambda x: x['Data'], reverse=True)
        return sorted_data
    except requests.RequestException as e:
        current_app.logger.error(f"Erro ao obter dados IPCA/Câmbio: {e}")
        return []
    
def fetch_focus_cambio_data():
    url_cambio = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativaMercadoMensais?%24format=json&%24filter=Indicador%20eq%20'C%C3%A2mbio'"
    try:
        response = requests.get(url_cambio)
        response.raise_for_status()
        data = response.json().get('value', [])
        filtered_data = [entry for entry in data if datetime.strptime(entry['Data'], '%Y-%m-%d') >= datetime(2019, 1, 2)]
        sorted_data = sorted(filtered_data, key=lambda x: x['Data'], reverse=True)
        return sorted_data
    except requests.RequestException as e:
        current_app.logger.error(f"Erro ao obter dados IPCA/Câmbio: {e}")
        return []
