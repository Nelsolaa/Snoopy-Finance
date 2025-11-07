# gerenciador_app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'


# --- Este é o Callback do Flask-Login ---
# Ele usa o seu DAO para carregar o usuário a cada requisição
@login_manager.user_loader
def load_user(user_id):
    # Importa aqui dentro para evitar importação circular
    from .backEnd.services.UserDao import UserDao
    return UserDao.get_user_by_id(user_id)


def create_app(config_class=Config):
    app = Flask(__name__,
                # Diz ao Flask onde encontrar os templates
                template_folder='frontEnd/templates',
                # Diz ao Flask onde encontrar o CSS/Imagens
                static_folder='frontEnd/static'
            )
    app.config.from_object(config_class)

    # Inicializa as extensões
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # --- Registrar os Blueprints (Controllers) ---
    
    # 1. Registrar o Controller Principal (Dashboard)
    # (Supondo que você renomeou o 'routes.py' para 'dashboard_controller.py'
    # e manteve o blueprint como 'main')
    from .backEnd.controller.DashboardController import bp as main_bp
    app.register_blueprint(main_bp)

    # 2. Registrar o Controller de Autenticação (Login)
    from .backEnd.controller.UserController import bp as auth_bp
    app.register_blueprint(auth_bp) # O prefixo '/auth' já foi definido no arquivo


    # --- Criar as tabelas do DB (Importante) ---
    # Precisamos importar os modelos aqui para que o SQLAlchemy saiba sobre eles
    from .backEnd.models import UserDb, GastoDb, EntradaDb 
    
    with app.app_context():
        db.create_all() # Cria as tabelas (User, Gasto, Entrada) se não existirem

    return app