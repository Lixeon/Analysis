from flask import render_template, redirect, url_for, flash, request
from flask_login import  login_user, logout_user, current_user
from flask_babel import  _, lazy_gettext as _l
from app.data import bp

@bp.route('/data', methods=['GET', 'POST'])
def  index():
    return render_template('data/index.html', title=_('Data'),data='active')

