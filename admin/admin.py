# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,\
    abort, g, redirect, url_for, request

from utils import login_required, admin_only

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/admin', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
        
    if g.user is None:
        return render_template('admin/login.html')
    return redirect(url_for('admin.workspace'))


@admin.route('/admin/workspace', methods=['GET'])
@login_required
@admin_only
def workspace():
    return render_template('admin/admin.html')

