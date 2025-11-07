# gerenciador_app/backEnd/controller/UsuarioController.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from ..services.UserDao import UserDao

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user, message = UserDao.register_user(username, email, password)

        if user:
            flash(message, 'success')
            return redirect(url_for('auth.login')) 
        else:
            flash(message, 'danger')
            # Se falhar, renderiza a página de registro de novo
            return render_template('pages/auth_page.html', is_login_page=False)
    
    # Se for GET, mostra a página de registro
    return render_template('pages/auth_page.html', is_login_page=False)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserDao.check_login(email, password)
        
        if user:
            login_user(user) 
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login falhou. Verifique seu email e senha.', 'danger')
            # Se falhar, renderiza a página de login de novo
            return render_template('pages/auth_page.html', is_login_page=True)

    # Se for GET, mostra a página de login
    return render_template('pages/auth_page.html', is_login_page=True)


@bp.route('/logout')
@login_required 
def logout():
    logout_user() 
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('auth.login'))