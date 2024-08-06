from datetime import datetime
from app import db
from flask_login import UserMixin

class SiconfiDataRREO(db.Model):
    __tablename__ = 'RREO_siconfi_anexo_14'

    idRREO_siconfi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instituicao = db.Column('Instituicao', db.String(255))
    codIBGE = db.Column('CodIBGE', db.String(45))
    uf = db.Column('UF', db.String(45))
    coluna = db.Column('Coluna', db.String(255))
    conta = db.Column('Conta', db.String(255))
    idConta = db.Column('IdConta', db.String(100))
    valor = db.Column('Valor', db.Float) 
    exercicio = db.Column('Exercicio', db.Integer) 
    periodo = db.Column('Periodo', db.String(45))
    anexo = db.Column('Anexo', db.String(255))
    # tabela = db.Column('Tabela', db.String(255))
    data_busca = db.Column(db.DateTime, default=datetime.utcnow)


class SiconfiDataRGF(db.Model):
    __tablename__ = 'RGF_siconfi_dados_novos'

    idRGF_siconfi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instituicao = db.Column('Instituicao', db.String(255))
    codIBGE = db.Column('CodIBGE', db.String(45))
    uf = db.Column('UF', db.String(45))
    coluna = db.Column('Coluna', db.String(255))
    conta = db.Column('Conta', db.String(255))
    idConta = db.Column('IdConta', db.String(100))
    valor = db.Column('Valor', db.Float) 
    exercicio = db.Column('Exercicio', db.Integer) 
    periodo = db.Column('Periodo', db.String(45))
    anexo = db.Column('Anexo', db.String(255))
    # tabela = db.Column('Tabela', db.String(255))
    data_busca = db.Column(db.DateTime, default=datetime.utcnow)


class BrentANP(db.Model):
    __tablename__ = 'Brent_ANP'
    idANP = db.Column(db.Integer, primary_key=True, autoincrement=True)
    period = db.Column('Periodo', db.String(45))
    product = db.Column('Produto', db.String(45))
    product_name = db.Column('Nome_Produto', db.String(45))
    value = db.Column('Valor', db.Float)
    units = db.Column('Unidades', db.String(45))

    def __repr__(self):
        return f'<BrentANP {self.period} - {self.product_name}>'
    
class Focus(db.Model):
    __tablename__ = 'Focus'
    idFocus = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column('Data', db.String(45))
    mediana = db.Column('Mediana', db.Float)
    indicador = db.Column('Indicador', db.String(45))
    dataRef = db.Column('DataReferencia', db.String(45))

    def __repr__(self):
        return f'<Focus {self.indicador} - {self.data} - {self.mediana}>'
    
class IPCA_IBGE(db.Model):
    __tablename__ = 'IPCA_IBGE'
    idIPCA_IBGE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    periodo = db.Column('Periodo', db.String(45))
    valor = db.Column('Valor', db.Float)
    itens = db.Column('Item', db.String(100))

    def __repr__(self):
        return f'<IPCA IBGE {self.periodo} - {self.valor}>'
    
class Desemprego_IBGE(db.Model):
    __tablename__ = 'Desemprego_IBGE'
    idDesemprego_IBGE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column('Valor', db.Float)
    data = db.Column('Data', db.String(45))

    def __repr__(self):
        return f'<IPCA IBGE {self.valor} - {self.data}>'
    

class CAGED_IBGE(db.Model):
    __tablename__ = 'CAGED_IBGE'
    idCAGED_IBGE = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UF = db.Column('UF', db.String(255))
    Cod_Municipio = db.Column('Cod_Municipio', db.Integer)  
    Municipio = db.Column('Municipio', db.String(45))
    Mes = db.Column('Mes', db.String(45))
    Estoque = db.Column('Estoque', db.Integer)  
    Admissoes = db.Column('Admissoes', db.Integer)  
    Desligamentos = db.Column('Desligamentos', db.Integer)  
    Saldos = db.Column('Saldos', db.Integer)  
    Variacao = db.Column('Variacao', db.Float)  

class RGF_SICONFI(db.Model):
    __tablename__ = 'RGF_siconfi'
    idRGF_siconfi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instituicao = db.Column('Instituicao', db.String(255))
    codIBGE = db.Column('CodIBGE', db.String(45))
    uf = db.Column('UF', db.String(45))
    coluna = db.Column('Coluna', db.String(255))
    conta = db.Column('Conta', db.String(255))
    idConta = db.Column('IdConta', db.String(100))
    valor = db.Column('Valor', db.Float) 
    exercicio = db.Column('Exercicio', db.Integer) 
    periodo = db.Column('Periodo', db.String(45))
    anexo = db.Column('Anexo', db.String(255))
    tabela = db.Column('Tabela', db.String(255))

class RREO_SICONFI(db.Model):
    __tablename__ = 'RREO_siconfi'
    idRREO_siconfi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instituicao = db.Column('Instituicao', db.String(255))
    codIBGE = db.Column('CodIBGE', db.String(45))
    uf = db.Column('UF', db.String(45))
    coluna = db.Column('Coluna', db.String(45))
    conta = db.Column('Conta', db.String(255))
    idConta = db.Column('IdConta', db.String(255))
    valor = db.Column('Valor', db.Float) 
    exercicio = db.Column('Exercicio', db.Integer) 
    periodo = db.Column('Periodo', db.String(45))
    anexo = db.Column('Anexo', db.String(255))
    tabela = db.Column('Tabela', db.String(255))

class PatrimonioFER(db.Model):
    __tablename__ = 'patrimonio_fer'
    id_patrimonio_fer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ano = db.Column('ano', db.Integer)
    mes = db.Column('mes', db.String(10))
    aportes = db.Column('aportes', db.Numeric(20,2))
    rendimentos = db.Column('rendimentos', db.Numeric(20,2))
    patrimonio_fer = db.Column('patriomonio',db.Numeric(20,2))

class RentabilidadeFER(db.Model):
    __tablename__ = 'rentabilidade_fer'
    id_patrimonio_fer = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ano = db.Column('ano', db.String(10))
    liquida = db.Column('liquida', db.Float)
    relativa = db.Column('relativa(%)', db.Float)
    #total_liquida = db.Column('total_liquida',db.Float)
    #total_relativa = db.Column('total_relativa(%)',db.Float)
    
class IndicadoresDimensoes(db.Model):
    __tablename__ = 'indicadores_dimensoes_uff'
    id_indicadores_dimensoes_uff = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ano = db.Column('ano', db.String(10))
    emprego = db.Column('emprego', db.Numeric(20,4))
    receitas = db.Column('receitas', db.Numeric(20,4))
    atividade_geral = db.Column('atividade_geral', db.Numeric(20,4))
    logistica = db.Column('logistica', db.Numeric(20,4))

class IndicadorComposto(db.Model):
    __tablename__ = 'indicador_composto_uff'
    id_indicador_composto_uff = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ano = db.Column('ano', db.String(10))
    indicador_composto = db.Column('indicador_composto', db.Numeric(20,4))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.id)  # Converte o ID para string, se necessário

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True  # Ou adicione a lógica para verificar se o usuário está autenticado

    def is_anonymous(self):
        return False
