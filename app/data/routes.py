from flask import render_template, redirect, url_for, flash, request
from flask_login import  login_user, logout_user, current_user
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from app.data import bp
from ext import desc


@bp.route('/data', methods=['GET', 'POST'])
def  index():
    ngrok = Ngrok.query.order_by(desc(Ngrok.time)).first()
    if(ngrok):
        res = ngrok[0].id
        target = ngrok[0].pub
    else:
        res=None
        target=None
    return render_template('data/index.html', title=_('Data'), data='active', res=res, target=target)
