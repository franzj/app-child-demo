# -*- coding: utf-8 -*-
from models import db, Password, Img, UserAdmin, Child

import json

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
            db.session.add(Child(child['username'], child['password']))
        db.session.commit()

        # Agregamos usuarios administrador
        for admin in data['useradmin']:
            db.session.add(UserAdmin(admin['username'], admin['password']))
        db.session.commit()
