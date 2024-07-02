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
