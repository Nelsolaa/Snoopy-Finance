# gerenciador_app/backEnd/controller/DashboardController.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user 
from ..services.FinanceDao import FinanceDao

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    context_data = FinanceDao.get_dashboard_data(current_user.id)
    return render_template('pages/dashboard.html', **context_data)

@bp.route('/add_entrada', methods=['POST'])
@login_required
def add_entrada():
    success, message = FinanceDao.add_new_entrada(request.form, current_user.id)
    if success: flash(message, 'success')
    else: flash(message, 'danger')
    return redirect(url_for('main.dashboard'))

@bp.route('/add_gasto', methods=['POST'])
@login_required
def add_gasto():
    success, message = FinanceDao.add_new_gasto(request.form, current_user.id)
    if success: flash(message, 'success')
    else: flash(message, 'danger')
    return redirect(url_for('main.dashboard'))

# --- ROTAS OTIMIZADAS (RETORNAM JSON) ---
@bp.route('/toggle_entrada/<int:id>', methods=['POST'])
@login_required
def toggle_entrada(id):
    FinanceDao.toggle_item_status(id, current_user.id, 'entrada')
    # Retorna os novos totais para o JS atualizar a tela sem reload
    return jsonify(FinanceDao.get_totals_json(current_user.id))

@bp.route('/toggle_gasto/<int:id>', methods=['POST'])
@login_required
def toggle_gasto(id):
    FinanceDao.toggle_item_status(id, current_user.id, 'gasto')
    return jsonify(FinanceDao.get_totals_json(current_user.id))

@bp.route('/delete_gasto/<int:id>', methods=['POST'])
@login_required
def delete_gasto(id):
    # Deleta e retorna os novos totais em JSON imediatamente
    FinanceDao.delete_item(id, current_user.id, 'gasto')
    return jsonify(FinanceDao.get_totals_json(current_user.id))

@bp.route('/delete_entrada/<int:id>', methods=['POST'])
@login_required
def delete_entrada(id):
    FinanceDao.delete_item(id, current_user.id, 'entrada')
    return jsonify(FinanceDao.get_totals_json(current_user.id))

@bp.route('/api/get_gasto/<int:id>')
@login_required
def api_get_gasto(id):
    return jsonify(FinanceDao.get_gasto_json(id, current_user.id))

@bp.route('/api/get_entrada/<int:id>')
@login_required
def api_get_entrada(id):
    return jsonify(FinanceDao.get_entrada_json(id, current_user.id))

@bp.route('/edit_gasto/<int:id>', methods=['POST'])
@login_required
def edit_gasto(id):
    success, message = FinanceDao.update_gasto(id, request.form, current_user.id)
    if success: flash(message, 'success')
    else: flash(message, 'danger')
    return redirect(url_for('main.dashboard'))

@bp.route('/edit_entrada/<int:id>', methods=['POST'])
@login_required
def edit_entrada(id):
    success, message = FinanceDao.update_entrada(id, request.form, current_user.id)
    if success: flash(message, 'success')
    else: flash(message, 'danger')
    return redirect(url_for('main.dashboard'))

@bp.route('/api/gastos_por_categoria')
@login_required
def api_gastos_por_categoria():
    return FinanceDao.get_chart_data(current_user.id)

# ... (outras rotas) ...

@bp.route('/api/gastos_por_banco')
@login_required
def api_gastos_por_banco():
    return FinanceDao.get_banco_chart_data(current_user.id)

