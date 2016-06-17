# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media')

serve = Flask(__name__)
serve.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
serve.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(serve)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    
    child = db.relationship("Child", uselist=False, backref="user")
    
    def __init__(self, username, password, is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin
    
    def __repr__(self):
        return '<User {0}>'.format(self.username)
    
    def verify_password(self, password):
        return password == self.password


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departamento = db.Column(db.String(15), nullable=False)
    provincia = db.Column(db.String(15), nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    birthdate = db.Column(db.Date(), nullable=False)
    colours = db.Column(db.String(25), nullable=False)
    ingresos = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, user, departamento, provincia,
                 sex, birthdate, colours, ingresos=1):
        self.user = user
        self.departamento = departamento
        self.provincia = provincia
        self.sex = sex
        self.birthdate = birthdate
        self.colours = colours
        self.ingresos = ingresos;

    def __repr__(self):
        return '<Child {0}>'.format(self.user)


class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Password {0}>'.format(self.name)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String, nullable=False)

    password_id = db.Column(db.Integer, db.ForeignKey('password.id'))
    password = db.relationship('Password',
        backref=db.backref('imgs', lazy='dynamic'))

    def __init__(self, src, password):
        self.src = src
        self.password = password

    def __repr__(self):
        return '<Img {0}>'.format(self.src)

