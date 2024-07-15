from flask import Blueprint, render_template, request,send_from_directory, current_app,redirect,url_for
from app.controllers.siconfi_controller import fetch_siconfi_RREO_data, fetch_siconfi_RGF_data
from app import db
# from app.models import SiconfiDataRREO, SiconfiDataRGF
from datetime import datetime
import pytz
import os
from app.controllers.anp_controller import fetch_anp_data
from app.controllers.ibge_controller import fetch_ipca_data, fetch_unemployment_data, download_caged_data
from app.utils.web_scraper import download_next_focus_report, convert_all_pdfs
from werkzeug.utils import secure_filename
from app.controllers.focus_controller import fetch_selic_data, fetch_pib_data, fetch_focus_ipca_data, fetch_focus_cambio_data
from flask_login import login_required


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
@login_required
def upload_siconfi():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Nenhum arquivo selecionado', 400
        
        file = request.files['file']
        
        if file.filename == '':
            return 'Nenhum arquivo selecionado', 400
        
        if file:
            # Salva o arquivo no diretório da área de trabalho do usuário atual
            filename = secure_filename(file.filename)
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            
            # Determine o diretório de upload com base no nome do arquivo
            if "finbraRREO" in filename:
                upload_folder = os.path.join(desktop_path, 'uploads', 'rreo')
            elif "finbraRGF" in filename:
                upload_folder = os.path.join(desktop_path, 'uploads', 'rgf')
            else:
                return 'Nome de arquivo não reconhecido', 400
            
            # Cria o diretório se não existir
            if not os.path.exists(upload_folder):
                try:
                    os.makedirs(upload_folder)
                except Exception as e:
                    return f"Erro ao criar o diretório: {e}", 500
            
            file_path = os.path.join(upload_folder, filename)
            
            try:
                file.save(file_path)
                from app.controllers.siconfi_controller import save_siconfi_data_to_db
                save_siconfi_data_to_db(current_app, file_path)
                return f'Upload realizado com sucesso. Arquivo salvo em: {file_path}', 200
            except Exception as e:
                return f"Erro ao salvar o arquivo: {e}", 500
    
    return render_template('upload_siconfi.html')

    
@main.route('/download_next_report')
def download_next_report():
    download_next_focus_report()
    convert_all_pdfs()
    return redirect(url_for('main.index'))

@main.route('/anp')
def anp():
    data = fetch_anp_data()
    return render_template('anp.html', data=data) 


@main.route('/ibge')
def ibge():
    return render_template('ibge.html')

@main.route('/ibge/ipca')
def ibge_ipca():
    try:
        data, variable_options, unit_options, value_options = fetch_ipca_data()
        return render_template('ibge_ipca.html', data=data, variable_options=variable_options, unit_options=unit_options, value_options=value_options)
    except Exception as e:
        current_app.logger.error(f"Erro ao obter dados do IPCA: {str(e)}")
        return f"Erro ao obter dados do IPCA: {str(e)}"


@main.route('/ibge/unemployment')
def ibge_unemployment():
    try:
        data = fetch_unemployment_data()
        return render_template('ibge_unemployment.html', data=data)
    except Exception as e:
        current_app.logger.error(f"Erro ao obter dados de Desemprego: {str(e)}")
        return f"Erro ao obter dados de Desemprego: {str(e)}"
    
@main.route('/download_caged_data')
def download_caged_data_route():
    try:
        file_path = download_caged_data()
        return f'Download realizado com sucesso. Arquivo salvo em: {file_path}'
    except Exception as e:
        return f'Erro ao baixar o arquivo: {str(e)}'
    
@main.route('/focus')
def focus():
    return render_template('focus.html')

@main.route('/focus/selic')
def focus_selic():
    data = fetch_selic_data()
    return render_template('focus_selic.html', selic_data=data)

@main.route('/focus/ipca')
def focus_ipca():
    data = fetch_focus_ipca_data()
    return render_template('focus_ipca.html', data=data)

@main.route('/focus/cambio')
def focus_cambio():
    data = fetch_focus_cambio_data()
    return render_template('focus_cambio.html', data=data)

@main.route('/focus/pib')
def focus_pib():
    data = fetch_pib_data()
    return render_template('focus_pib.html', pib_data=data)
