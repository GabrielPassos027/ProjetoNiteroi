import requests
import time

import os
from bs4 import BeautifulSoup
import pandas as pd
import shutil
from openpyxl import load_workbook
from datetime import datetime


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
        data = response.json()
        
        # Filtrar dados para incluir apenas a partir de 201901
        filtered_data = [item for item in data if item['D3C'] >= '201901']
        
        return filtered_data
    else:
        raise Exception(f"Erro na requisição Desemprego: {response.status_code}")
    

def download_caged_data():
    url = "http://pdet.mte.gov.br/novo-caged"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all("a", text="3. Tabelas.xlsx")
    if links:
        file_url = links[0]["href"]
        full_file_url = "http://pdet.mte.gov.br" + file_url

        response = requests.get(full_file_url)
        if response.status_code == 200:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            download_folder = os.path.join(desktop_path, "IBGE-Postos de Trabalho")
            os.makedirs(download_folder, exist_ok=True)
            temp_file_path = os.path.join(download_folder, "temp_download.xlsx")

            with open(temp_file_path, "wb") as file:
                file.write(response.content)

            # Carregar o arquivo Excel usando pandas
            xls = pd.ExcelFile(temp_file_path)

            # Verificar se a aba "Tabela 8.1" existe
            if "Tabela 8.1" in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name="Tabela 8.1")

                # Corrigir os nomes das colunas removendo "Unnamed" e ajustando a formatação
                df.columns = [col if 'Unnamed' not in col else '' for col in df.columns]

                # Salvar a aba específica em um novo arquivo Excel
                final_file_path = os.path.join(download_folder, "Tabela_8_1.xlsx")
                with pd.ExcelWriter(final_file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name="Tabela 8.1", index=False)

                # Fechar o arquivo Excel para liberar o recurso
                xls.close()

                # Mesclar as células no arquivo final
                wb = load_workbook(final_file_path)
                ws = wb["Tabela 8.1"]

                # Mesclar E5:H5
                ws.merge_cells('E5:H5')
                # Mesclar B5:B6
                ws.merge_cells('B5:B6')
                # Mesclar C5:C6
                ws.merge_cells('C5:C6')
                # Mesclar D5:D6
                ws.merge_cells('D5:D6')

                # Lógica para mesclar células a partir de I5 até que não haja mais conteúdo
                start_col = 9  # Coluna I
                row = 5

                while True:
                    if ws.cell(row=row, column=start_col).value:
                        end_col = start_col + 4  # Mescla 5 colunas à direita
                        ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
                        start_col = end_col + 1  # Avança para a próxima célula a verificar
                    else:
                        break

                wb.save(final_file_path)

                # Remover o arquivo temporário
                os.remove(temp_file_path)

                return final_file_path
        else:
            raise Exception("Erro ao baixar o arquivo")
    else:
        raise Exception("Elemento com a nome 'Tabela.xlsx' não encontrado")