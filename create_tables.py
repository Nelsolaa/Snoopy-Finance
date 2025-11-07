from gerenciador_app import create_app, db
import os

try:
    from gerenciador_app.backEnd.models.UserDb import User
    from gerenciador_app.backEnd.models.GastoDb import Gasto
    from gerenciador_app.backEnd.models.EntradaDb import Entrada
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Verifique os nomes dos arquivos e classes em 'backEnd/models/'")
    exit()

print("Iniciando a criação das tabelas...")

app = create_app()

with app.app_context():
    print(f"Conectando ao banco: {app.config['SQLALCHEMY_DATABASE_URI']}")

    print("Dropando tabelas antigas...")
    db.drop_all()
    print("Tabelas dropadas.")

    print("Criando novas tabelas...")
    db.create_all()
    print("Tabelas criadas com sucesso!")

print("Processo concluído.")