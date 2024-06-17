import requests

def fetch_anp_data():
    api_key = "M7QrsxD6Uza4APeLAQtEXiAg4ZmPGpdPuFwVodah"
    url = ("https://api.eia.gov/v2/petroleum/pri/spt/data/"
           "?frequency=monthly&data[0]=value&start=2019-01&end=2024-06"
           "&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
           f"&api_key={api_key}")

    try:
        response = requests.get(url)
        data = response.json()
        
        # Verifica se os dados foram retornados corretamente
        if 'response' in data and 'data' in data['response']:
            # Filtra os dados pelo 'product-name' igual a "UK Brent Crude Oil"
            filtered_data = [item for item in data['response']['data'] if item['product-name'] == "UK Brent Crude Oil"]
            # # Imprime os dados filtrados para inspeção
            # print("Dados filtrados:")
            # for item in filtered_data:
            #     print(item)

            return filtered_data
        else:
            print("Falha ao buscar dados da ANP")
            return []
    except Exception as e:
        print(f"Erro ao buscar dados da API ANP: {e}")
        return []
