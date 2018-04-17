from flask import render_template, redirect, url_for, flash, request,abort,jsonify
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from app.api import bp

import json
import requests

@bp.route('/', methods=['GET', 'POST'])
def index():
    ngroks = Ngrok.query.all()
    api_list=list(map(lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns},ngroks))
    return render_template('api/index.html', title=_('Api'),Api='active',api_list=api_list)

@bp.route('/csrf', methods=['POST'])
def csrf():
    headers = {'Content-Type': 'application/json'}
    if request.method == 'POST':
        target = request.form['url']+'/'+request.form['machine']
        # target = 'http://feb34695.ngrok.io' +'/'+request.form['machine']
        data = { k:v for k,v in request.form.to_dict().items() }
        print(type(data))

        print(target)
        print(data)
        r= requests.post(target,data=data,headers=headers)
        print(r.content)
        if r.status_code != 200:
            return _('Error: the translation service failed.')
        # xx =json.loads(r.content.decode('utf-8-sig'))
        # print(xx)
        return jsonify(data)
    else:
        abort(400)
