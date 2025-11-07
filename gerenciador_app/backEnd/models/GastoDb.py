# gerenciador_app/backEnd/models/GastoDb.py
from gerenciador_app import db
from datetime import datetime

class Gasto(db.Model):
    __tablename__ = 'gasto'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_gasto = db.Column(db.String(20), nullable=False, default='variavel') 
    categoria = db.Column(db.String(100), nullable=False)
    tipo_pagamento = db.Column(db.String(50), nullable=True)
    
    # --- NOVA COLUNA PARA O BANCO ---
    banco = db.Column(db.String(50), nullable=True)
    
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    concluido = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Gasto('{self.categoria}', 'R${self.valor}')"