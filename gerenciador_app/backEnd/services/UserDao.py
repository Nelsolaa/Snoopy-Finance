# gerenciador_app/backEnd/services/UserDao.py

from gerenciador_app import db, bcrypt
from ..models.UserDb import User # Importa a classe User do seu modelo

class UserDao:

    @staticmethod
    def register_user(username, email, password):
        """
        Serviço para registrar um novo usuário.
        Faz o hash da senha e salva no banco.
        """
        try:
            # 1. Gerar o hash da senha
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            # 2. Criar a nova instância do usuário
            new_user = User(
                username=username, 
                email=email, 
                password_hash=hashed_password
            )
            
            # 3. Salvar no banco
            db.session.add(new_user)
            db.session.commit()
            return new_user, "Usuário registrado com sucesso."
        
        except Exception as e:
            db.session.rollback() # Desfaz a transação em caso de erro
            # (Provavelmente o email ou username já existem)
            print(f"Erro no DAO ao registrar: {e}")
            return None, "Erro ao registrar. Email ou usuário já pode existir."

    @staticmethod
    def check_login(email, password):
        """
        Serviço para verificar o login.
        Busca o usuário e compara o hash da senha.
        """
        try:
            # 1. Encontrar o usuário pelo email
            user = User.query.filter_by(email=email).first()
            
            # 2. Se o usuário existir E a senha bater com o hash...
            if user and bcrypt.check_password_hash(user.password_hash, password):
                return user # Retorna o objeto User
            
            return None # Senha ou usuário incorretos
        except Exception as e:
            print(f"Erro no DAO ao checar login: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Serviço para o Flask-Login carregar o usuário da sessão.
        """
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            print(f"Erro no DAO ao buscar user por ID: {e}")
            return None