from app.models import IndicadoresDimensoes, IndicadorComposto, db
import pandas as pd

def save_uff_to_db(app, file_path):
    # Inicializar o contexto do aplicativo
    with app.app_context():
        IndicadoresDimensoes.query.delete()
        IndicadorComposto.query.delete()
        db.session.commit()

        # Processar a primeira aba: A_INDICADORES_DIMENSÕES
        sheet_name_1 = 'A_INDICADORES_DIMENSÕES'
        df1 = pd.read_excel(file_path, sheet_name=sheet_name_1)
        df1 = df1.iloc[:, :5]
        df1.dropna(inplace=True)
        df1.columns = ['Ano', 'Emprego', 'Receitas', 'Atividade Geral', 'Logistica']
        df1 = df1[~df1['Ano'].str.contains('Indicador', na=False)]
        df1['Ano'] = pd.to_datetime(df1['Ano']).dt.strftime('%d-%m-%Y')

        # Salvar os dados na tabela IndicadoresDimensoes
        for index, row in df1.iterrows():
            record = IndicadoresDimensoes(
                ano=row['Ano'],
                emprego=row['Emprego'],
                receitas=row['Receitas'],
                atividade_geral=row['Atividade Geral'],
                logistica=row['Logistica']
            )
            db.session.add(record)

        # Processar a segunda aba: B_INDICADOR_COMPOSTO
        sheet_name_2 = 'B_INDICADOR_COMPOSTO'
        df2 = pd.read_excel(file_path, sheet_name=sheet_name_2)
        df2 = df2.iloc[:, :2]
        df2.dropna(inplace=True)
        df2.columns = ['Ano', 'Indicador Composto']
        df2['Ano'] = pd.to_datetime(df2['Ano']).dt.strftime('%d-%m-%Y')

        # Salvar os dados na tabela IndicadorComposto
        for index, row in df2.iterrows():
            record = IndicadorComposto(
                ano=row['Ano'],
                indicador_composto=row['Indicador Composto']
            )
            db.session.add(record)

        # Commit dos dados no banco
        db.session.commit()
        print("Dados UFF salvos no banco de dados")
