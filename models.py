# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

serve = Flask(__name__)
serve.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(serve)


class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), nullable=False)
    departamento = db.Column(db.String(15), nullable=False)
    provincia = db.Column(db.String(15), nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    birthdate = db.Column(db.Date(), nullable=False)
    colours = db.Column(db.String(25), nullable=False)

    def __init__(self, username, password, departamento, 
                 provincia, sex, birthdate, colours):
        self.username = username
        self.password = password
        self.departamento = departamento
        self.provincia = provincia
        self.sex = sex
        self.birthdate = birthdate
        self.colours = colours

    def __repr__(self):
        return '<Child %r>' % self.username

    def verify_password(self, password):
        return password == self.password


class UserAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<UserAdmin {0}>'.format(self.username)


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

