# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,\
    abort, g, redirect, url_for, request, session

from utils import login_required, admin_only
from models import User

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/admin', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            error = 'Usuario Incorecto'
        elif not user.is_admin:
            error = 'Usuario Incorecto'
        elif not user.verify_password(request.form['password']):
            error = 'Contraseña Incorecta'
        else:
            session['user_id'] = user.username
            return redirect(url_for('admin.workspace'))
        return render_template('admin/login.html', error=error)
    
    if g.user is None:
        return render_template('admin/login.html')
    return redirect(url_for('admin.workspace'))


@admin.route('/admin/workspace', methods=['GET'])
@login_required
@admin_only
def workspace():
    return render_template('admin/admin.html')

