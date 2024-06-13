from flask import Blueprint, render_template, request,send_from_directory, current_app,redirect,url_for
from app.controllers.siconfi_controller import fetch_siconfi_RREO_data, fetch_siconfi_RGF_data
from app import db
from app.models import SiconfiDataRREO, SiconfiDataRGF
from datetime import datetime
import pytz
import os
from app.controllers.anp_controller import fetch_anp_data
from app.utils.web_scraper import download_next_focus_report

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/siconfi_bases')
def siconfi_bases():
    return render_template('siconfi_bases.html')

@main.route('/siconfi_RGF', methods=['GET', 'POST'])
def siconfi_RGF():
    data = []
    data_count = 0
    an_exercicio = nr_periodo = ""
    if request.method == 'POST':
        an_exercicio = request.form.get('an_exercicio')
        nr_periodo = request.form.get('nr_periodo')
        data = fetch_siconfi_RGF_data(an_exercicio, nr_periodo)
        data_count = len(data)
    return render_template('siconfi_RGF.html', data=data, data_count=data_count, an_exercicio=an_exercicio, nr_periodo=nr_periodo)

@main.route('/siconfi_RREO', methods=['GET', 'POST'])
def siconfi_RREO():
    data = []
    data_count = 0
    an_exercicio = nr_periodo = no_anexo = ""
    if request.method == 'POST':
        an_exercicio = request.form.get('an_exercicio')
        nr_periodo = request.form.get('nr_periodo')
        no_anexo = request.form.get('no_anexo')
        data = fetch_siconfi_RREO_data(an_exercicio, nr_periodo, no_anexo)
        data_count = len(data)
    return render_template('siconfi_RREO.html', data=data, data_count=data_count, an_exercicio=an_exercicio, nr_periodo=nr_periodo, no_anexo=no_anexo)

@main.route('/salvar_dado_RREO', methods=['POST'])
def salvar_dado_RREO():
    an_exercicio = request.form['an_exercicio']
    nr_periodo = request.form['nr_periodo']
    no_anexo = request.form['no_anexo']

    # print("Parâmetros recebidos:", an_exercicio, nr_periodo, no_anexo)

    # Consultar a API SICONFI
    dados_api = fetch_siconfi_RREO_data(an_exercicio, nr_periodo, no_anexo)
    # print("Dados da API:", dados_api)

    # Verificar se há dados retornados
    if dados_api:
        # Salvar todos os dados retornados da consulta no banco de dados
        for item in dados_api:
            novo_dado = SiconfiDataRREO(
                conta=item['conta'],
                cod_conta=item['cod_conta'],
                coluna=item['coluna'],
                valor=item['valor'],
                exercicio=item['exercicio'],
                instituicao=item['instituicao'],
                data_busca=datetime.now()
            )
            db.session.add(novo_dado)

        # Commit das alterações no banco de dados
        db.session.commit()

        return 'Dados salvos com sucesso!'
    else:
        return 'Nenhum dado retornado da consulta à API SICONFI.'
    
@main.route('/salvar_dado_RGF', methods=['POST'])
def salvar_dado_RGF():
    an_exercicio = request.form['an_exercicio']
    nr_periodo = request.form['nr_periodo']

    # print("Parâmetros recebidos:", an_exercicio, nr_periodo, no_anexo)

    # Consultar a API SICONFI
    dados_api = fetch_siconfi_RGF_data(an_exercicio, nr_periodo)
    # print("Dados da API:", dados_api)

    # Verificar se há dados retornados
    if dados_api:
        # Salvar todos os dados retornados da consulta no banco de dados
        for item in dados_api:
            novo_dado = SiconfiDataRGF(
                conta=item['conta'],
                cod_conta=item['cod_conta'],
                coluna=item['coluna'],
                valor=item['valor'],
                cod_ibge=item['cod_ibge'],
                populacao=item['populacao'],
                instituicao=item['instituicao'],
                data_busca=datetime.now()
            )
            db.session.add(novo_dado)

        # Commit das alterações no banco de dados
        db.session.commit()

        return 'Dados salvos com sucesso!'
    else:
        return 'Nenhum dado retornado da consulta à API SICONFI.'
    
@main.route('/download_next_report')
def download_next_report():
    download_next_focus_report()
    return redirect(url_for('main.index'))


@main.route('/anp')
def anp():
    data = fetch_anp_data()
    print(f"API response: {data}")  # Adiciona a resposta da API no log
    if data and 'response' in data and 'data' in data['response']:
        anp_data = data['response']['data']
    else:
        anp_data = None
    return render_template('anp.html', data=anp_data)
