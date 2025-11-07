from . import db
from datetime import datetime

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    concluido = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Entrada('{self.nome}', 'R${self.valor}', '{self.concluido}')"

class Gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_gasto = db.Column(db.String(20), nullable=False, default='variavel')
    categoria = db.Column(db.String(100), nullable=False)
    tipo_pagamento = db.Column(db.String(50), nullable=True)
    tipo_banco = db.Column(db.String(50), nullable=True)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    concluido = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"Gasto('{self.categoria}', 'R${self.valor}', '{self.concluido}')"