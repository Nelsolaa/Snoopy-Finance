# gerenciador_app/routes.py
from . import db
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
import pandas as pd  # Adicione a importação do pandas
from .models import Gasto, Entrada

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    print("\n--- [LOG] Rota /dashboard acessada (GET) ---")
    try:
        gastos = Gasto.query.order_by(Gasto.data.desc()).all()
        entradas = Entrada.query.order_by(Entrada.data.desc()).all()
        print(f"--- [LOG] Encontrados {len(gastos)} gastos e {len(entradas)} entradas.")
        
        total_entradas = sum(e.valor for e in entradas if e.concluido)
        total_gastos = sum(g.valor for g in gastos if g.concluido)
        saldo = total_entradas - total_gastos
        print(f"--- [LOG] Cálculos: Entradas={total_entradas}, Gastos={total_gastos}, Saldo={saldo}")

        snoopy_estado = 'normal'
        snoopy_imagem = url_for('static', filename='images/snoopy_normal.gif')

        if saldo <= 0 and total_gastos > 0:
            snoopy_estado = 'triste'
            snoopy_imagem = url_for('static', filename='images/snoopy_triste.gif')
        elif saldo > (total_entradas * 0.7) and total_entradas > 0:
            snoopy_estado = 'feliz'
            snoopy_imagem = url_for('static', filename='images/snoopy_feliz.gif')
        
        print(f"--- [LOG] Estado do Snoopy: {snoopy_estado}")
        print("--- [LOG] Renderizando o template dashboard.html...")
        return render_template('pages/dashboard.html',
                               gastos=gastos,
                               entradas=entradas,
                               total_entradas=total_entradas,
                               total_gastos=total_gastos,
                               saldo=saldo,
                               snoopy_estado=snoopy_estado,
                               snoopy_imagem=snoopy_imagem)
    except Exception as e:
        print(f"!!! ERRO CRÍTICO no dashboard: {e} !!!")
        return f"Ocorreu um erro no servidor: {e}"


@bp.route('/add_entrada', methods=['POST'])
def add_entrada():
    print("\n--- [LOG] Rota /add_entrada acessada (POST) ---")
    if request.method == 'POST':
        try:
            print("--- [LOG] Dados recebidos do formulário:")
            print(f"--- [LOG] Nome: {request.form.get('nome')}")
            print(f"--- [LOG] Valor: {request.form.get('valor')}")
            print(f"--- [LOG] Data: {request.form.get('data')}")

            nome = request.form.get('nome')
            valor_str = request.form.get('valor')
            data_str = request.form.get('data')

            if not nome or not valor_str or not data_str:
                print("--- [LOG] ERRO: Campos obrigatórios faltando.")
                raise ValueError("Preencha todos os campos obrigatórios.")

            print("--- [LOG] Convertendo dados...")
            valor = float(valor_str)
            data = datetime.strptime(data_str, '%Y-%m-%d')
            print("--- [LOG] Conversão de dados OK.")
            
            nova_entrada = Entrada(nome=nome, valor=valor, data=data)
            print("--- [LOG] Objeto Entrada criado.")
            
            db.session.add(nova_entrada)
            print("--- [LOG] db.session.add(nova_entrada) - OK")
            db.session.commit()
            print("--- [LOG] db.session.commit() - OK. Entrada salva!")
            
            flash('Entrada adicionada com sucesso!', 'success')
            print("--- [LOG] Flash de sucesso enviado.")
            
        except Exception as e:
            print(f"!!! ERRO NO BLOCO /add_entrada: {e} !!!")
            flash(f'Erro ao adicionar entrada: {e}', 'danger')
            print("--- [LOG] Flash de erro enviado.")

    print("--- [LOG] Redirecionando para /dashboard")
    return redirect(url_for('main.dashboard'))


@bp.route('/add_gasto', methods=['POST'])
def add_gasto():
    print("\n--- [LOG] Rota /add_gasto acessada (POST) ---")
    if request.method == 'POST':
        try:
            print("--- [LOG] Dados recebidos do formulário:")
            print(f"--- [LOG] Categoria: {request.form.get('categoria')}")
            print(f"--- [LOG] Valor: {request.form.get('valor')}")
            print(f"--- [LOG] Data: {request.form.get('data')}")
            print(f"--- [LOG] Tipo Gasto: {request.form.get('tipo_gasto')}")
            print(f"--- [LOG] Tipo Pagamento: {request.form.get('tipo_pagamento')}")
            print(f"--- [LOG] Tipo Banco: {request.form.get('tipo_banco')}")

            categoria = request.form.get('categoria')
            valor_str = request.form.get('valor')
            data_str = request.form.get('data')
            tipo_gasto = request.form.get('tipo_gasto')
            tipo_pagamento = request.form.get('tipo_pagamento')
            tipo_banco = request.form.get('tipo_banco')

            if not categoria or not valor_str or not data_str:
                print("--- [LOG] ERRO: Campos obrigatórios faltando.")
                raise ValueError("Campos 'Categoria', 'Valor' e 'Data' são obrigatórios.")

            print("--- [LOG] Convertendo dados...")
            valor = float(valor_str)
            data = datetime.strptime(data_str, '%Y-%m-%d')
            print("--- [LOG] Conversão de dados OK.")
            
            novo_gasto = Gasto(
                tipo_gasto=tipo_gasto,
                categoria=categoria,
                tipo_pagamento=tipo_pagamento,
                tipo_banco=tipo_banco,
                valor=valor,
                data=data
            )
            print("--- [LOG] Objeto Gasto criado.")
            
            db.session.add(novo_gasto)
            print("--- [LOG] db.session.add(novo_gasto) - OK")
            db.session.commit()
            print("--- [LOG] db.session.commit() - OK. Gasto salvo!")
            
            flash('Gasto adicionado com sucesso!', 'success')
            print("--- [LOG] Flash de sucesso enviado.")
            
        except Exception as e:
            print(f"!!! ERRO NO BLOCO /add_gasto: {e} !!!")
            flash(f'Erro ao adicionar gasto: {e}', 'danger')
            print("--- [LOG] Flash de erro enviado.")
            
    print("--- [LOG] Redirecionando para /dashboard")
    return redirect(url_for('main.dashboard'))


# --- ROTAS DE TOGGLE (Checkboxes) ---

@bp.route('/toggle_entrada/<int:id>', methods=['POST'])
def toggle_entrada(id):
    print(f"\n--- [LOG] Rota /toggle_entrada/{id} acessada (POST) ---")
    try:
        entrada = Entrada.query.get_or_404(id)
        print(f"--- [LOG] Entrada encontrada: {entrada.nome}")
        print(f"--- [LOG] Status ANTES do toggle: {entrada.concluido}")
        
        entrada.concluido = not entrada.concluido
        
        print(f"--- [LOG] Status DEPOIS do toggle: {entrada.concluido}")
        
        db.session.commit()
        print("--- [LOG] db.session.commit() - OK. Status salvo!")
    except Exception as e:
        print(f"!!! ERRO NO BLOCO /toggle_entrada: {e} !!!")
        
    print("--- [LOG] Redirecionando para /dashboard")
    return redirect(url_for('main.dashboard'))


@bp.route('/toggle_gasto/<int:id>', methods=['POST'])
def toggle_gasto(id):
    print(f"\n--- [LOG] Rota /toggle_gasto/{id} acessada (POST) ---")
    try:
        gasto = Gasto.query.get_or_404(id)
        print(f"--- [LOG] Gasto encontrado: {gasto.categoria}")
        print(f"--- [LOG] Status ANTES do toggle: {gasto.concluido}")
        
        gasto.concluido = not gasto.concluido
        
        print(f"--- [LOG] Status DEPOIS do toggle: {gasto.concluido}")
        
        db.session.commit()
        print("--- [LOG] db.session.commit() - OK. Status salvo!")
    except Exception as e:
        print(f"!!! ERRO NO BLOCO /toggle_gasto: {e} !!!")
        
    print("--- [LOG] Redirecionando para /dashboard")
    return redirect(url_for('main.dashboard'))

@bp.route('/api/gastos_por_categoria')
def api_gastos_por_categoria():
    print("\n--- [LOG] Rota /api/gastos_por_categoria acessada (GET) ---")
    try:
        # 1. Buscamos apenas os gastos que foram marcados como "Pagos"
        gastos_pagos = Gasto.query.filter_by(concluido=True).all()
        
        if not gastos_pagos:
            print("--- [LOG] Nenhum gasto pago encontrado para o gráfico.")
            return jsonify({'labels': [], 'data': []})

        print(f"--- [LOG] Encontrados {len(gastos_pagos)} gastos pagos.")
        
        # 2. Convertemos os dados do SQLAlchemy para um formato que o Pandas entende
        dados_lista = [{
            'categoria': g.categoria,
            'valor': g.valor
        } for g in gastos_pagos]
        
        # 3. (Aqui entra o Pandas!) Criamos o DataFrame
        df = pd.DataFrame(dados_lista)
        
        # 4. Usamos o Pandas para agrupar por 'categoria' e somar o 'valor'
        gastos_agrupados = df.groupby('categoria')['valor'].sum().reset_index()
        
        print("--- [LOG] Dados agrupados pelo Pandas:")
        print(gastos_agrupados)
        
        # 5. Preparamos os dados para o formato JSON que o Chart.js gosta
        labels = gastos_agrupados['categoria'].tolist()
        data = gastos_agrupados['valor'].tolist()
        
        print("--- [LOG] Enviando dados JSON para o frontend.")
        return jsonify({'labels': labels, 'data': data})
        
    except Exception as e:
        print(f"!!! ERRO NO BLOCO /api/gastos_por_categoria: {e} !!!")
        return jsonify({'error': str(e)}), 500
    

@bp.route('/delete_gasto/<int:id>', methods=['POST'])
def delete_gasto(id):
    """ Controlador para deletar um gasto """
    print(f"\n--- [LOG] Rota /delete_gasto/{id} acessada (POST) ---")
    try:
        # Encontra o gasto pelo ID ou retorna 404 (Not Found)
        gasto_para_deletar = Gasto.query.get_or_404(id)
        print(f"--- [LOG] Encontrado gasto para deletar: {gasto_para_deletar.categoria}")
        
        # Deleta o item da sessão do banco
        db.session.delete(gasto_para_deletar)
        # Salva a mudança
        db.session.commit()
        print("--- [LOG] Gasto deletado com sucesso.")
        
        flash('Gasto deletado com sucesso.', 'success')
        
    except Exception as e:
        print(f"!!! ERRO NO BLOCO /delete_gasto: {e} !!!")
        flash('Erro ao deletar gasto.', 'danger')
        
    # Redireciona de volta para o dashboard
    return redirect(url_for('main.dashboard'))


@bp.route('/delete_entrada/<int:id>', methods=['POST'])
def delete_entrada(id):
    """ Controlador para deletar uma entrada """
    print(f"\n--- [LOG] Rota /delete_entrada/{id} acessada (POST) ---")
    try:
        entrada_para_deletar = Entrada.query.get_or_404(id)
        print(f"--- [LOG] Encontrada entrada para deletar: {entrada_para_deletar.nome}")
        
        db.session.delete(entrada_para_deletar)
        db.session.commit()
        print("--- [LOG] Entrada deletada com sucesso.")
        
        flash('Entrada deletada com sucesso.', 'success')
        
    except Exception as e:
        print(f"!!! ERRO NO BLOCO /delete_entrada: {e} !!!")
        flash('Erro ao deletar entrada.', 'danger')
            
    return redirect(url_for('main.dashboard'))