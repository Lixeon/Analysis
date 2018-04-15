from flask import render_template, redirect, url_for, flash, request
from flask_babel import  _, lazy_gettext as _l
from app.api import bp


@bp.route('/', methods=['GET', 'POST'])
def  index():
    return render_template('api/index.html', title=_('Api'),Api='active')
