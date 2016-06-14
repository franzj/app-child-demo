# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory, g, session

from app.app import child
from admin.admin import admin
from models import serve, User

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media')
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

serve.config['SECRET_KEY'] = 'Top Secret'
serve.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

serve.register_blueprint(child)
serve.register_blueprint(admin)


def init_database():
    from utils import init_db
    init_db()

@serve.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(username=session['user_id']).first()

@serve.route('/media/<filename>')
def uploaded_file(filename):
    return send_from_directory(serve.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    init_database()
    serve.run(debug=True)

