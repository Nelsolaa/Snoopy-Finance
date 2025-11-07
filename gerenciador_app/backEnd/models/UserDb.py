# gerenciador_app/backEnd/models/UserDb.py

from gerenciador_app import db
from flask_login import UserMixin

# O nome do arquivo é UserDb.py, mas a classe principal é User
class User(db.Model, UserMixin):
    __tablename__ = 'user' # Nome da tabela no banco
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Coluna para armazenar a senha HASHED (segura)
    password_hash = db.Column(db.String(128), nullable=False)

    # (Opcional, mas útil para o futuro)
    # Define a relação: "Um User pode ter muitos Gastos"
    # gastos = db.relationship('Gasto', back_populates='author')
    # entradas = db.relationship('Entrada', back_populates='author')

    def __repr__(self):
        return f'<User {self.username}>'