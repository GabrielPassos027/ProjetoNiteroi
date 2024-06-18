import os
import datetime
import requests
import tabula

# Função para baixar o PDF a partir de um URL e salvar em um diretório
def download_focus_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF '{filename}' baixado com sucesso!")
        # Após baixar o PDF, converta-o para CSV
        convert_pdf_to_csv(filename)
    else:
        print(f"Falha ao baixar o PDF '{filename}'")

# Função para obter a data atual
def get_current_date():
    return datetime.date.today()

# Função para gerar a URL do próximo PDF do FOCUS
def generate_next_pdf_url(last_date):
    next_date = last_date + datetime.timedelta(days=7)
    next_pdf_date = next_date.strftime("%Y%m%d")
    pdf_url = f"https://www.bcb.gov.br/content/focus/focus/R{next_pdf_date}.pdf"
    return pdf_url, next_date

# Função para baixar o próximo relatório do FOCUS
def download_next_focus_report():
    # Encontrar a última data de relatório baixado
    last_date = find_last_downloaded_date()
    if last_date:
        pdf_url, next_date = generate_next_pdf_url(last_date)
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        focus_folder = os.path.join(desktop_path, 'FOCUS')
        year_folder = os.path.join(focus_folder, str(next_date.year))
        os.makedirs(year_folder, exist_ok=True)  # Cria o diretório se não existir
        pdf_filename = os.path.join(year_folder, f"{next_date.strftime('%Y%m%d')}.pdf")
        if not os.path.exists(pdf_filename):
            download_focus_pdf(pdf_url, pdf_filename)
        else:
            print(f"O relatório para {next_date.strftime('%Y-%m-%d')} já está baixado.")
    else:
        print("Nenhum relatório anterior encontrado. Não é possível baixar o próximo relatório.")

# Função para encontrar a última data de relatório baixado
def find_last_downloaded_date():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    focus_folder = os.path.join(desktop_path, 'FOCUS')
    if not os.path.exists(focus_folder):
        return None
    all_years = [year for year in os.listdir(focus_folder) if os.path.isdir(os.path.join(focus_folder, year))]
    if not all_years:
        return None
    last_year = max(all_years)
    last_year_folder = os.path.join(focus_folder, last_year)
    all_reports = [report for report in os.listdir(last_year_folder) if report.endswith('.pdf')]
    if not all_reports:
        return None
    last_report = max(all_reports)
    last_report_date = datetime.datetime.strptime(last_report[:-4], '%Y%m%d').date()
    return last_report_date

# Função para converter PDF para CSV
def convert_pdf_to_csv(pdf_path):
    csv_path = pdf_path.replace('.pdf', '.csv')
    try:
        dfs = tabula.read_pdf(pdf_path, stream=True, pages='all')
        if dfs:
            dfs[0].to_csv(csv_path, index=False)
            print(f"PDF '{pdf_path}' convertido para CSV '{csv_path}' com sucesso!")
        else:
            print(f"Nenhuma tabela encontrada no PDF '{pdf_path}'.")
    except NameError as e:
        print(f"Falha ao converter o PDF '{pdf_path}' para CSV: {str(e)}")
    except Exception as e:
        print(f"Outro erro ao converter o PDF '{pdf_path}' para CSV: {str(e)}")

# Função para converter todos os PDFs de um diretório para CSV
def convert_all_pdfs_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                convert_pdf_to_csv(pdf_path)

# Função principal para executar todas as conversões de PDF para CSV
def convert_all_pdfs():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    focus_folder = os.path.join(desktop_path, 'FOCUS')
    convert_all_pdfs_in_directory(focus_folder)

# Baixar o próximo relatório do FOCUS
download_next_focus_report()

# Converter todos os PDFs existentes para CSV
convert_all_pdfs()
