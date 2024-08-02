from app.models import PatrimonioFER,RentabilidadeFER, db
import pandas as pd
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

def save_fer_patrimonio_data_to_db(app, file_path):
    with app.app_context():
        try:
            PatrimonioFER.query.delete()
            db.session.commit()
            # Definir nomes das colunas esperadas
            columns = ['ANO', 'MÊS', 'APORTES', 'RENDIMENTOS', 'PATRIMÔNIO FER']

            # Carregar o arquivo CSV
            df = pd.read_csv(file_path, names=columns, sep=';', encoding='latin-1', header=None, skiprows=2)

            df = df.dropna(subset=['RENDIMENTOS', 'PATRIMÔNIO FER'])

            # Função para limpar e converter colunas monetárias
            def clean_and_convert(column):
                column = column.str.replace('R$', '')  # Remove o símbolo 'R$'
                column = column.str.replace('.', '')  # Remove os pontos
                column = column.str.replace(',', '.')  # Substitui a vírgula por ponto
                column = column.str.strip()  # Remove espaços em branco
                column = column.replace('-', 0)  # Substitui '-' por NaN
                return column

            # Limpar e converter as colunas
            df['APORTES'] = clean_and_convert(df['APORTES'])
            df['RENDIMENTOS'] = clean_and_convert(df['RENDIMENTOS'])
            df['PATRIMÔNIO FER'] = clean_and_convert(df['PATRIMÔNIO FER'])

            df['ANO'] = pd.to_numeric(df['ANO'], errors='coerce').astype(int)
            for _, row in df.iterrows():
                try:
                    patrimonio = PatrimonioFER(
                        ano=int(row['ANO']),
                        mes=row['MÊS'].strip(),
                        aportes=Decimal(row['APORTES']) if not pd.isna(row['APORTES']) else None,
                        rendimentos=Decimal(row['RENDIMENTOS']),
                        patrimonio_fer=Decimal(row['PATRIMÔNIO FER'])
                    )
                    db.session.add(patrimonio)
                    db.session.commit()
                except IntegrityError as ie:
                    db.session.rollback()
                    app.logger.error(f"Erro de integridade: {row} - {ie}")
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(f"Erro ao salvar a linha {row}: {e}")
            print("Dados FER Patrimonio salvos!")
        except Exception as e:
            app.logger.error(f"Erro ao processar o arquivo: {e}")



def save_fer_rentabilidade_data_to_db(app, file_path):
    with app.app_context():
        RentabilidadeFER.query.delete()
        db.session.commit()
        try:
            columns = ['Ano', 'Líquida', 'Relativa']
            df = pd.read_csv(file_path, names=columns, sep=';', encoding='latin-1', header=None, skiprows=3)
            df = df.dropna(subset=['Ano', 'Líquida', 'Relativa'])
            df['Relativa'] = df['Relativa'].str.replace('%', '').str.replace(',', '.').astype(float)
            df['Líquida'] = df['Líquida'].str.replace('R$', '').str.replace(',', '.').astype(float)

            # Separar as linhas totais das linhas de dados anuais
            
            # df = df[df['Ano'] != 'Total']

            for _, row in df.iterrows():
                entry = RentabilidadeFER(
                    ano=(row['Ano']),
                    liquida=row['Líquida'],
                    relativa=row['Relativa'],
                )
                db.session.add(entry)
            db.session.commit()
            print("Dados FER Rentabilidade salvos!")
        except Exception as e:
            app.logger.error(f"Erro ao processar o arquivo: {e}")