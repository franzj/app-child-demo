# -*- coding: utf-8 -*-
from flask import request, g, abort
from models import db, Password, Img, User, Child
from functools import wraps

import json
import datetime

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        abort(401)
    return decorated_view

def admin_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if g.user.is_admin:
            return func(*args, **kwargs)
        abort(401)
    return decorated_view

def is_ajax():
    try:
        if request.headers['X-Requested-With'] == 'XMLHttpRequest':
            return True
        return False
    except KeyError:
        False

def init_db():
    """ Funcion que crea las tablas en la base de datos si no existe
        y luego insertamos los datos del archivo 'data.json' y
        los insertamos en la base de datos
    """
    # Eliminamos todas la tablas
    db.drop_all()
    # Creamos todas la tablas
    db.create_all()

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())['data']

        # Optenemos todas las comtraseñas y las insertamos en la base de datos
        for password in data['password']:
            db.session.add(Password(password))
        # comfirmamos la inserción
        db.session.commit()

        # Optenemos todas las imágenes y las insertamos en la base de datos
        for img in data['imgs']:
            psw = Password.query.get(img['password_id'])
            db.session.add(Img(img['img'], psw))
        db.session.commit()

        # Optenemos todos los usuario niños y las insertamos en la base de datos
        for child in data['userchild']:
            username = child['username']
            password = child['password']
            
            user = User(username, password, False)
            
            date = child['birthdate'].split("/")
            
            birthdate = datetime.date(
                year=int(date[2]),
                month=int(date[1]),
                day=int(date[0])
            )
            
            departamento = child['departamento']
            provincia = child['provincia']
            sex = child['sex']
            colours = ','.join(child['colours'])
            ingresos = child['ingresos']
            
            db.session.add(
                Child(user, departamento, provincia,
                      sex, birthdate, colours, ingresos)
            )

        db.session.commit()

        # Agregamos usuarios administrador
        for admin in data['useradmin']:
            db.session.add(User(admin['username'], admin['password'], True))
        db.session.commit()

