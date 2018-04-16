from flask import render_template, redirect, url_for, flash, request
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from app.api import bp



@bp.route('/', methods=['GET', 'POST'])
def  index():
    ngroks = Ngrok.query.all()
    api_list=list(map(lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns},ngroks))
    return render_template('api/index.html', title=_('Api'),Api='active',api_list=api_list)
