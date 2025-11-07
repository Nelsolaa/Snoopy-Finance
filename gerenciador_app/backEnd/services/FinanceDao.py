from flask import url_for, jsonify
import pandas as pd
from datetime import datetime

from gerenciador_app import db
from ..models.GastoDb import Gasto
from ..models.EntradaDb import Entrada

class FinanceDao:

    @staticmethod
    def get_dashboard_data(user_id):
        gastos = Gasto.query.filter_by(user_id=user_id).order_by(Gasto.data.desc()).all()
        entradas = Entrada.query.filter_by(user_id=user_id).order_by(Entrada.data.desc()).all()
        
        total_entradas = sum(e.valor for e in entradas if e.concluido)
        total_gastos = sum(g.valor for g in gastos if g.concluido)
        saldo = total_entradas - total_gastos
        
        # Imagem inicial (o JS assume depois)
        snoopy_imagem = url_for('static', filename='images/snoopy_normal.gif')
        if saldo <= 0 and total_gastos > 0:
            snoopy_imagem = url_for('static', filename='images/snoopy_triste.gif')
        elif saldo > (total_entradas * 0.7) and total_entradas > 0:
             snoopy_imagem = url_for('static', filename='images/snoopy_feliz.gif')

        return {
            'gastos': gastos,
            'entradas': entradas,
            'total_entradas': total_entradas,
            'total_gastos': total_gastos,
            'saldo': saldo,
            'snoopy_imagem': snoopy_imagem
        }

    @staticmethod
    def get_totals_json(user_id):
        """ Calcula totais rápidos para AJAX """
        total_entradas = db.session.query(db.func.sum(Entrada.valor)).filter_by(user_id=user_id, concluido=True).scalar() or 0.0
        total_gastos = db.session.query(db.func.sum(Gasto.valor)).filter_by(user_id=user_id, concluido=True).scalar() or 0.0
        return {
            'total_entradas': total_entradas,
            'total_gastos': total_gastos,
            'saldo': total_entradas - total_gastos
        }

    @staticmethod
    def add_new_gasto(form_data, user_id):
        try:
            data = datetime.strptime(form_data.get('data'), '%Y-%m-%d')
            novo_gasto = Gasto(
                tipo_gasto=form_data.get('tipo_gasto'),
                categoria=form_data.get('categoria'),
                tipo_pagamento=form_data.get('tipo_pagamento'),
                banco=form_data.get('tipo_banco'),
                valor=float(form_data.get('valor')),
                data=data,
                user_id=user_id
            )
            db.session.add(novo_gasto)
            db.session.commit()
            return True, "Gasto adicionado com sucesso!"
        except Exception as e:
            db.session.rollback()
            return False, f"Erro: {e}"

    @staticmethod
    def add_new_entrada(form_data, user_id):
        try:
            data = datetime.strptime(form_data.get('data'), '%Y-%m-%d')
            nova_entrada = Entrada(nome=form_data.get('nome'), valor=float(form_data.get('valor')), data=data, user_id=user_id)
            db.session.add(nova_entrada)
            db.session.commit()
            return True, "Entrada adicionada!"
        except Exception as e:
            db.session.rollback()
            return False, f"Erro: {e}"

    @staticmethod
    def toggle_item_status(item_id, user_id, item_type):
        try:
            model = Gasto if item_type == 'gasto' else Entrada
            item = model.query.filter_by(id=item_id, user_id=user_id).first_or_404()
            item.concluido = not item.concluido
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def delete_item(item_id, user_id, item_type):
        try:
            model = Gasto if item_type == 'gasto' else Entrada
            item = model.query.filter_by(id=item_id, user_id=user_id).first_or_404()
            db.session.delete(item)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    @staticmethod
    def get_gasto_json(gasto_id, user_id):
        g = Gasto.query.filter_by(id=gasto_id, user_id=user_id).first_or_404()
        return {
            'id': g.id, 'data': g.data.strftime('%Y-%m-%d'), 'valor': g.valor,
            'categoria': g.categoria, 'tipo_gasto': g.tipo_gasto,
            'tipo_pagamento': g.tipo_pagamento, 'banco': g.banco
        }

    @staticmethod
    def get_entrada_json(entrada_id, user_id):
        e = Entrada.query.filter_by(id=entrada_id, user_id=user_id).first_or_404()
        return {'id': e.id, 'data': e.data.strftime('%Y-%m-%d'), 'valor': e.valor, 'nome': e.nome}

    @staticmethod
    def update_gasto(gasto_id, form_data, user_id):
        try:
            g = Gasto.query.filter_by(id=gasto_id, user_id=user_id).first_or_404()
            g.data = datetime.strptime(form_data.get('data'), '%Y-%m-%d')
            g.valor = float(form_data.get('valor'))
            g.categoria = form_data.get('categoria')
            g.tipo_gasto = form_data.get('tipo_gasto')
            g.tipo_pagamento = form_data.get('tipo_pagamento')
            g.banco = form_data.get('tipo_banco')
            db.session.commit()
            return True, "Gasto atualizado!"
        except Exception as e:
            db.session.rollback()
            return False, f"Erro: {e}"

    @staticmethod
    def update_entrada(entrada_id, form_data, user_id):
        try:
            e = Entrada.query.filter_by(id=entrada_id, user_id=user_id).first_or_404()
            e.data = datetime.strptime(form_data.get('data'), '%Y-%m-%d')
            e.valor = float(form_data.get('valor'))
            e.nome = form_data.get('nome')
            db.session.commit()
            return True, "Entrada atualizada!"
        except Exception as e:
            db.session.rollback()
            return False, f"Erro: {e}"

    @staticmethod
    def get_chart_data(user_id):
        gastos_pagos = Gasto.query.filter_by(concluido=True, user_id=user_id).all()
        if not gastos_pagos:
            return jsonify({'labels': [], 'data': []})
        
        dados_lista = [{'categoria': g.categoria or 'Outros', 'valor': g.valor} for g in gastos_pagos]
        df = pd.DataFrame(dados_lista)
        
        agrupado = df.groupby('categoria')['valor'].sum().reset_index()
        return jsonify({'labels': agrupado['categoria'].tolist(), 'data': agrupado['valor'].tolist()})

    @staticmethod
    def get_banco_chart_data(user_id):
        gastos_pagos = Gasto.query.filter_by(concluido=True, user_id=user_id).all()
        if not gastos_pagos:
            return jsonify({'labels': [], 'data': []})
            
        dados_lista = [{'banco': g.banco or 'Outros', 'valor': g.valor} for g in gastos_pagos]
        df = pd.DataFrame(dados_lista)
        
        bancos_agrupados = df.groupby('banco')['valor'].sum().reset_index()
        
        return jsonify({
            'labels': bancos_agrupados['banco'].tolist(),
            'data': bancos_agrupados['valor'].tolist()
        })