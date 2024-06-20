import requests
import time

def fetch_ipca_data():
    url = "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/first%206/c315/all/d/v63%202"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na requisição IPCA: {response.status_code}")

def fetch_unemployment_data():
    url = "https://apisidra.ibge.gov.br/values/t/6381/n1/all/v/4099/p/all/d/v4099%201"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na requisição Desemprego: {response.status_code}")