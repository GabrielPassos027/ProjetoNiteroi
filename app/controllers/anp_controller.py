import requests

def fetch_anp_data():
    url = "https://api.eia.gov/v2/petroleum/pri/spt/data/?frequency=monthly&data[0]=value&start=2019-01&end=2024-06&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key=M7QrsxD6Uza4APeLAQtEXiAg4ZmPGpdPuFwVodah"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
