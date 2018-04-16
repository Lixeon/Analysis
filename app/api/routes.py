from flask import render_template, redirect, url_for, flash, request,abort
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from app.api import bp

import requests

@bp.route('/', methods=['GET', 'POST'])
def index():
    ngroks = Ngrok.query.all()
    api_list=list(map(lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns},ngroks))
    return render_template('api/index.html', title=_('Api'),Api='active',api_list=api_list)

@bp.route('/csrf', methods=['POST'])
def csrf():
    if request.method == 'POST':
        #target = request.form['url']
        target = 'https://0eb0a388.ngrok.io'
        data = request.form
        print(target)
        print(data)
        r= requests.post(target,data=data)
        if(r.status_code == requests.codes.ok):
            return r.json()
        else:
            abort(r.status_code)
    else:
        abort(400)
