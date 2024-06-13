from app import db
from datetime import datetime
import pytz

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