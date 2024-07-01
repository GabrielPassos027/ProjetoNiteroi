import requests
import json
from datetime import datetime, timedelta
from flask import current_app
import pandas as pd

def fetch_selic_data():
    url_selic = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais?%24format=json&%24filter=Indicador%20eq%20'Selic'"
    try:
        response = requests.get(url_selic)
        response.raise_for_status()
        data = response.json().get('value', [])

        # Converte a lista de dicionários em DataFrame
        df = pd.DataFrame(data)

        # Filtra a partir de 04/01/2019
        start_date = datetime(2019, 1, 4)
        df['Data'] = pd.to_datetime(df['Data'])
        df = df[df['Data'] >= start_date]

        # Função para ajustar para a próxima segunda-feira se for fim de semana
        def adjust_to_weekday(date):
            if date.weekday() == 5:  # Sábado
                return date + timedelta(days=2)
            elif date.weekday() == 6:  # Domingo
                return date + timedelta(days=1)
            return date

        # Lista para armazenar as datas filtradas
        filtered_dates = []
        current_date = start_date

        while current_date <= datetime.now():
            adjusted_date = adjust_to_weekday(current_date)
            filtered_dates.append(adjusted_date)
            current_date += timedelta(days=7)

        # Filtra os dados pelas datas ajustadas
        filtered_data = df[df['Data'].isin(filtered_dates)]

        # Seleciona os 4 primeiros dados de cada dia filtrado
        final_data = []
        for date in filtered_dates:
            daily_data = filtered_data[filtered_data['Data'] == date]
            daily_records = daily_data.head(4).to_dict('records')
            
            # Adiciona a "Data Referência" para cada grupo de 4 registros
            for i, record in enumerate(daily_records):
                record['Data Referência'] = record['Data'].year + i
            
            final_data.extend(daily_records)

        # Formata a coluna 'Data' para remover a hora
        for entry in final_data:
            entry['Data'] = entry['Data'].strftime('%Y-%m-%d')

        # Ordena os dados pela data em ordem decrescente
        final_data = sorted(final_data, key=lambda x: x['Data'], reverse=True)

        return final_data

    except requests.RequestException as e:
        current_app.logger.error(f"Erro ao obter dados SELIC: {e}")
        return []

def fetch_pib_data():
    url_pib = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais?%24format=json&%24filter=Indicador%20eq%20'PIB%20Total'"
    try:
        response = requests.get(url_pib)
        response.raise_for_status()
        data = response.json().get('value', [])

        # Converte a lista de dicionários em DataFrame
        df = pd.DataFrame(data)

        # Filtra a partir de 04/01/2019
        start_date = datetime(2019, 1, 4)
        df['Data'] = pd.to_datetime(df['Data'])
        df = df[df['Data'] >= start_date]

        # Função para ajustar para a próxima segunda-feira se for fim de semana
        def adjust_to_weekday(date):
            if date.weekday() == 5:  # Sábado
                return date + timedelta(days=2)
            elif date.weekday() == 6:  # Domingo
                return date + timedelta(days=1)
            return date

        # Lista para armazenar as datas filtradas
        filtered_dates = []
        current_date = start_date

        while current_date <= datetime.now():
            adjusted_date = adjust_to_weekday(current_date)
            filtered_dates.append(adjusted_date)
            current_date += timedelta(days=7)

        # Filtra os dados pelas datas ajustadas
        filtered_data = df[df['Data'].isin(filtered_dates)]

        # Seleciona os dados do quinto ao nono de cada dia filtrado
        final_data = []
        for date in filtered_dates:
            daily_data = filtered_data[filtered_data['Data'] == date]
            daily_records = daily_data.iloc[5:9].to_dict('records')

            # Adiciona a "Data Referência" para cada grupo de 4 registros
            for i, record in enumerate(daily_records):
                record['Data Referência'] = record['Data'].year + i

            final_data.extend(daily_records)

        # Formata a coluna 'Data' para remover a hora
        for entry in final_data:
            entry['Data'] = entry['Data'].strftime('%Y-%m-%d')

        # Ordena os dados pela data em ordem decrescente
        final_data = sorted(final_data, key=lambda x: x['Data'], reverse=True)

        return final_data
    except requests.RequestException as e:
        current_app.logger.error(f"Erro ao obter dados PIB: {e}")
        return []
    
def fetch_focus_ipca_data():
    url_ipca = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais?%24format=json&%24filter=Indicador%20eq%20'IPCA'"
    try:
        response = requests.get(url_ipca)
        response.raise_for_status()
        data = response.json().get('value', [])

        # Converte a lista de dicionários em DataFrame
        df = pd.DataFrame(data)

        # Filtra a partir de 04/01/2019
        start_date = datetime(2019, 1, 4)
        df['Data'] = pd.to_datetime(df['Data'])
        df = df[df['Data'] >= start_date]

        # Função para ajustar para a próxima segunda-feira se for fim de semana
        def adjust_to_weekday(date):
            if date.weekday() == 5:  # Sábado
                return date + timedelta(days=2)
            elif date.weekday() == 6:  # Domingo
                return date + timedelta(days=1)
            return date

        # Lista para armazenar as datas filtradas
        filtered_dates = []
        current_date = start_date

        while current_date <= datetime.now():
            adjusted_date = adjust_to_weekday(current_date)
            filtered_dates.append(adjusted_date)
            current_date += timedelta(days=7)

        # Filtra os dados pelas datas ajustadas
        filtered_data = df[df['Data'].isin(filtered_dates)]

        # Seleciona os dados do quinto ao nono de cada dia filtrado
        final_data = []
        for date in filtered_dates:
            daily_data = filtered_data[filtered_data['Data'] == date]
            daily_records = daily_data.iloc[5:9].to_dict('records')
            
            # Adiciona a "Data Referência" para cada grupo de 4 registros
            for i, record in enumerate(daily_records):
                record['Data Referência'] = record['Data'].year + i
            
            final_data.extend(daily_records)

        # Formata a coluna 'Data' para remover a hora
        for entry in final_data:
            entry['Data'] = entry['Data'].strftime('%Y-%m-%d')

        # Ordena os dados pela data em ordem decrescente
        final_data = sorted(final_data, key=lambda x: x['Data'], reverse=True)

        return final_data
    except requests.RequestException as e:
        current_app.logger.error(f"Erro ao obter dados IPCA: {e}")
        return []
    
def fetch_focus_cambio_data():
    url_cambio = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais?%24format=json&%24filter=Indicador%20eq%20'C%C3%A2mbio'"
    try:
        response = requests.get(url_cambio)
        response.raise_for_status()
        data = response.json().get('value', [])

        # Converte a lista de dicionários em DataFrame
        df = pd.DataFrame(data)

        # Filtra a partir de 04/01/2019
        start_date = datetime(2019, 1, 4)
        df['Data'] = pd.to_datetime(df['Data'])
        df = df[df['Data'] >= start_date]

        # Função para ajustar para a próxima segunda-feira se for fim de semana
        def adjust_to_weekday(date):
            if date.weekday() == 5:  # Sábado
                return date + timedelta(days=2)
            elif date.weekday() == 6:  # Domingo
                return date + timedelta(days=1)
            return date

        # Lista para armazenar as datas filtradas
        filtered_dates = []
        current_date = start_date

        while current_date <= datetime.now():
            adjusted_date = adjust_to_weekday(current_date)
            filtered_dates.append(adjusted_date)
            current_date += timedelta(days=7)

        # Filtra os dados pelas datas ajustadas
        filtered_data = df[df['Data'].isin(filtered_dates)]

        # Seleciona os dados do quinto ao nono de cada dia filtrado
        final_data = []
        for date in filtered_dates:
            daily_data = filtered_data[filtered_data['Data'] == date]
            daily_records = daily_data.iloc[5:9].to_dict('records')

            # Adiciona a "Data Referência" para cada grupo de 4 registros
            for i, record in enumerate(daily_records):
                record['Data Referência'] = record['Data'].year + i

            final_data.extend(daily_records)

        # Formata a coluna 'Data' para remover a hora
        for entry in final_data:
            entry['Data'] = entry['Data'].strftime('%Y-%m-%d')

        # Ordena os dados pela data em ordem decrescente
        final_data = sorted(final_data, key=lambda x: x['Data'], reverse=True)

        return final_data

    except requests.RequestException as e:
        current_app.logger.error(f"Erro ao obter dados Câmbio: {e}")
        return []