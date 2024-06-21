import requests
import time

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