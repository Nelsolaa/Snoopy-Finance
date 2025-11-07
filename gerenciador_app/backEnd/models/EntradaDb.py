# gerenciador_app/backEnd/models/EntradaDb.py
from gerenciador_app import db
from datetime import datetime

class Entrada(db.Model):
    __tablename__ = 'entrada' # Nome da tabela
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    concluido = db.Column(db.Boolean, default=False)

    # --- NOVA LINHA ---
    # Isso linka esta Entrada ao 'id' da tabela 'user'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Entrada('{self.nome}', 'R${self.valor}')"