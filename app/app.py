# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, abort, request,
    redirect, url_for, jsonify, session, flash, g)
from sqlalchemy.orm.exc import NoResultFound

from models import db, User, Child, Password, Img
from utils import is_ajax, login_required

import datetime
import random

child = Blueprint('child', __name__, template_folder='templates')


def rand_passwords(password_valid):
    pos, data, pws = random.randrange(5), [i for i in range(5)], Img.query.all()
    data[pos] = password_valid
    
    for i in range(5):
        if i != pos:
            rand = random.randrange(len(pws))
            data[i] = pws[rand].src
    return data


@child.route('/', methods=['GET'])
def index():
    return render_template('child/index.html')


@child.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = {'username': username, 'password': password}
        return render_template('child/continue.html', data=data)

    return render_template('child/register.html')


@child.route('/register/continue', methods=['POST'])
def cuntinue_register():
    year, month, day = request.form['birthdate'].split("-")
    
    birthdate = datetime.date(
        year=int(year), 
        month=int(month), 
        day=int(day)
    )
    
    username = request.form['username']
    password = request.form['password']
    
    user = User(username, password, False)
    
    departamento = request.form['departamento']
    provincia = request.form['provincia']
    sex = request.form['sex']
    colours = request.form['colours']
    
    child = Child(user, departamento,provincia,
                  sex, birthdate, colours)
    
    db.session.add(child)
    db.session.commit()
    
    session['user_id'] = user.username
    
    return redirect(url_for('child.play'))


@child.route('/verificar', methods=['GET',])
def verificarnombre():
    """ Verifica si el usurio ya existe si no enviar
        un mensaje de error, la peticion debe contener
        en las cabeceras el X-Requested-With con XMLHttpRequest
        para verificar que es ajax.
    """
    if is_ajax():
        try:
            username = username=request.args['nombre']
            child = User.query.filter_by(username=username).first()
            
            if child is None:
                return jsonify(status=404, mensaje='El nombre esta disponible')
        except KeyError:
            return jsonify(status=400, mensaje='Consulta mal formulada')

        return jsonify(status=302, mensaje='Lo sentimos {0} ya existe :('\
                    .format(username))
    return jsonify(status=400, mensaje='Error no es ajax')


@child.route('/passwords', methods=['GET'])
def passwords():
    if is_ajax():
        try:
            username = request.args['username']
            user = User.query.filter_by(username=username).first()
            
            if user is None:
                return jsonify(mensaje='Consulta mal formulada')
            
            passwords = rand_passwords(user.password)
            return jsonify(passwords=passwords)

        except KeyError:
            pass
        passwords = Password.query.all()
        data = []
        for password in passwords:
            temp = []
            for img in password.imgs.all():
                temp.append({
                    'id': img.id,
                    'src': img.src
                })
            data.append({
                'id': password.id,
                'name': password.name,
                'imgs': temp
            })
        return jsonify(passwords=data)

    return jsonify(status=400, mensaje='Error no es ajax')


@child.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('child.play'))
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            error = 'Invalid username'
        elif not user.verify_password(request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user.username
            user.child.ingresos = user.child.ingresos + 1
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('child.play'))
    return render_template('child/login.html', error=error)


@child.route('/userchild/<username>', methods=['GET', 'POST'])
@login_required
def userchild(username):
    return render_template('child/child.html')


@child.route('/logout')
@login_required
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('child.index'))


@child.route('/play', methods=['GET'])
@login_required
def play():
    return render_template('child/play.html')

