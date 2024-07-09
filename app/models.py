from datetime import datetime
from app import db


class SiconfiDataRREO(db.Model):
    __tablename__ = 'siconfi_data_RREO'

    id = db.Column(db.Integer, primary_key=True)
    conta = db.Column(db.String(255))
    cod_conta = db.Column(db.String(255))
    coluna = db.Column(db.String(255))
    valor = db.Column(db.Float)
    exercicio = db.Column(db.Integer)
    instituicao = db.Column(db.String(255))
    data_busca = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SiconfiDataRREO id={self.id}, conta={self.conta}, coluna={self.coluna}, valor={self.valor}>"

class SiconfiDataRGF(db.Model):
    __tablename__ = 'siconfi_data_RGF'

    id = db.Column(db.Integer, primary_key=True)
    conta = db.Column(db.String(255))
    cod_conta = db.Column(db.String(255))
    coluna = db.Column(db.String(255))
    valor = db.Column(db.Float)
    cod_ibge = db.Column(db.Integer)
    populacao = db.Column(db.Integer)
    instituicao = db.Column(db.String(255))
    data_busca = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SiconfiDataRGF id={self.id}, conta={self.conta}, coluna={self.coluna}, valor={self.valor}>"

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

class RGF_SICONFI:
    __tablename__ = 'RGF_siconfi'
    idRGF_siconfi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instituicao = db.Column('Instituicao', db.String(45))
    codIBGE = db.Column('CodIBGE', db.String(45))
    uf = db.Column('UF', db.String(45))
    coluna = db.Column('Coluna', db.String(45))
    conta = db.Column('Conta', db.String(45))
    idConta = db.Column('IdConta', db.String(100))
    valor = db.Column('Valor', db.Float) 
    exercicio = db.Column('Exercicio', db.Integer) 
    periodo = db.Column('Periodo', db.String(45))
    anexo = db.Column('Anexo', db.String(45))
    tabela = db.Column('Tabela', db.String(45))

class RREO_SICONFI:
    __tablename__ = 'RREO_siconfi'
    idRREO_siconfi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    instituicao = db.Column('Instituicao', db.String(45))
    codIBGE = db.Column('CodIBGE', db.String(45))
    uf = db.Column('UF', db.String(45))
    coluna = db.Column('Coluna', db.String(45))
    conta = db.Column('Conta', db.String(45))
    idConta = db.Column('IdConta', db.String(100))
    valor = db.Column('Valor', db.Float) 
    exercicio = db.Column('Exercicio', db.Integer) 
    periodo = db.Column('Periodo', db.String(45))
    anexo = db.Column('Anexo', db.String(45))
    tabela = db.Column('Tabela', db.String(45))
    
