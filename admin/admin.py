# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort

admin = Blueprint('admin', __name__,
                        template_folder='templates')

@admin.route('/admin')
def index():
    return render_template('admin/admin.html')
