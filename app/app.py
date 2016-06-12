# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, abort, request,
        redirect, url_for, jsonify)
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from models import db, Child, Password

child = Blueprint('child', __name__, template_folder='templates')

def is_ajax():
    try:
        if request.headers['X-Requested-With'] == 'XMLHttpRequest':
            return True
        return False
    except KeyError as e:
        False

@child.route('/')
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
    username = request.form['username']
    password = request.form['password']
    departamento = request.form['departamento']
    provincia = request.form['provincia']
    sex = request.form['sex']
    birthdate = request.form['birthdate']
    colours = request.form['colours']
    
    child = Child(username, password, departamento, 
                  provincia, sex, birthdate, colours)
    
    db.session.add(child)
    db.session.commit()
    
    return redirect(url_for('child.play'))  


@child.route('/userchild/<username>', methods=['GET', 'POST'])
def userchild(username):
    return render_template('child/child.html')


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
            child = Child.query.filter_by(username=username).one()
        except NoResultFound:
            return jsonify(status=404, mensaje='El nombre esta disponible')
        except KeyError:
            return jsonify(status=400, mensaje='Consulta mal formulada')

        return jsonify(status=302, mensaje='Lo sentimos {0} ya existe :('\
                    .format(username))
    return jsonify(status=400, mensaje='Error no es ajax')


@child.route('/passwords', methods=['GET'])
def passwords():
    if is_ajax():
        passwords = Password.query.all()
        data = []
        for password in passwords:
            temp = []
            for img in password.imgs.all():
                temp.append({
                    'id': img.id,
                    'src': '/media/{0}'.format(img.src)
                })
            data.append({
                'id': password.id,
                'name': password.name,
                'imgs': temp
            })
        return jsonify(passwords=data)

    return jsonify(status=400, mensaje='Error no es ajax')


@child.route('/play', methods=['GET'])
def play():
    return render_template('child/play.html')

