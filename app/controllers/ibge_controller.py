import requests
import time

import os
from bs4 import BeautifulSoup
import pandas as pd

lista_url = [
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/first%206/c315/all/d/v63%202",
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/202007,202008,202009,202010,202011,202012/c315/all/d/v63%202",
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/202101,202102,202103,202104,202105,202106/c315/all/d/v63%202",
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/202107,202108,202109,202110,202111,202112/c315/all/d/v63%202",
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/202201,202202,202203,202204,202205,202206/c315/all/d/v63%202",
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/202207,202208,202209,202210,202211,202212/c315/all/d/v63%202",
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/202301,202302,202303,202304,202305,202306/c315/all/d/v63%202",
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/202307,202308,202309,202310,202311,202312/c315/all/d/v63%202",
    "https://apisidra.ibge.gov.br/values/t/7060/n1/all/v/63/p/last%205/c315/all/d/v63%202"
]

def fetch_ipca_data():
    all_data = []
    for url in lista_url:
        response = requests.get(url)
        if response.status_code == 200:
            all_data.extend(response.json())
        else:
            raise Exception(f"Erro na requisição IPCA: {response.status_code}")
        time.sleep(10)  # Pausa de 10 segundos entre as requisições

    # Filtrar dados para remover linhas indesejadas
    filtered_data = [item for item in all_data if item['D4N'] != 'Geral, grupo, subgrupo, item e subitem']

    # Extrair opções únicas para filtros e ordená-las
    variable_options = sorted(list(set(item['D3C'] for item in filtered_data)))
    unit_options = sorted(list(set(item['V'] for item in filtered_data)))
    value_options = sorted(list(set(item['D4N'] for item in filtered_data)))

    return filtered_data, variable_options, unit_options, value_options


def fetch_unemployment_data():
    url = "https://apisidra.ibge.gov.br/values/t/6381/n1/all/v/4099/p/all/d/v4099%201"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na requisição Desemprego: {response.status_code}")
    

def download_caged_data():
    url = "http://pdet.mte.gov.br/novo-caged"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    item = soup.find("li", class_="item-6225")
    if item:
        file_url = item.find("a")["href"]
        full_file_url = "http://pdet.mte.gov.br" + file_url

        response = requests.get(full_file_url)
        if response.status_code == 200:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            download_folder = os.path.join(desktop_path, "IBGE-Postos de Trabalho")
            os.makedirs(download_folder, exist_ok=True)
            temp_file_path = os.path.join(download_folder, "temp_download.xlsx")

            with open(temp_file_path, "wb") as file:
                file.write(response.content)

            # Processar o arquivo Excel e extrair a aba "Tabela 8.1"
            df = pd.read_excel(temp_file_path, sheet_name="Tabela 8.1")

            # Salvar apenas a aba "Tabela 8.1"
            final_file_path = os.path.join(download_folder, "Tabela_8_1.xlsx")
            df.to_excel(final_file_path, index=False)

            # Remover o arquivo temporário
            os.remove(temp_file_path)

            return final_file_path
        else:
            raise Exception("Erro ao baixar o arquivo")
    else:
        raise Exception("Elemento com a classe 'item-6225' não encontrado")