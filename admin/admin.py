# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,\
    abort, g, redirect, url_for, request, session
from werkzeug.utils import secure_filename

from utils import login_required, admin_only
from models import User, Img, db, serve, Password


admin = Blueprint('admin', __name__, template_folder='templates')

import os


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


def get_query_or_None():
    try:
        query = request.args['query']
        return query
    except:
        return None

@admin.route('/admin/workspace', methods=['GET', 'POST'])
@login_required
@admin_only
def workspace():
    query = get_query_or_None()
    data = {}
    
    if request.method == 'POST':
        if request.form['accion'] == 'eliminar':
            id = int(request.form['img_id'])
            img = Img.query.get(id)
            path = img.src
            db.session.delete(img)
            db.session.commit()
            os.remove('{0}/{1}'.format(serve.config['UPLOAD_FOLDER'], path))
            
        else:
            id = int(request.form['pass_id'])
            passw = Password.query.get(id)
            file = request.files['file']
            filename = secure_filename(file.filename)
            
            img = Img(filename, passw)
            db.session.add(img)
            db.session.commit()
            
            file.save(os.path.join(serve.config['UPLOAD_FOLDER'], filename))
    
    if query and query == 'estadistica':
        data['query'] = 'estadistica'
        data['usuarios'] = User.query.all()
    elif query and query == 'passwords':
        data['query'] = 'passwords'
    
    return render_template('admin/admin.html', data=data)

