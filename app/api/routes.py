from flask import render_template, redirect, url_for, flash, request,abort,jsonify
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from app.api import bp

import json
import requests
import grequests



def rs_ask(urls,ids):
    rs = (grequests.get(u, timeout=3) for u in urls)
    return dict(zip(ids,map(lambda x:x.status_code,grequests.map(rs))))
@bp.route('/', methods=['GET', 'POST'])
def index():
    ngroks = Ngrok.query.all()
    api_list=list(map(lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns},ngroks))
    for i in api_list:
        if 'status' not in i.keys():
            i['status']= 0
        if 'info' not in i.keys():
            i['info'] = 'unkown'
        if 'control' not in i.keys():
            i['control'] = 'button'
    cache = rs_ask([i['pub'] for i in api_list], [i['id'] for i in api_list])
    for api in api_list:
        api['status'] = cache[api['id']]
    if request.method == 'POST':
        return jsonify(api_list[int(request.form['id'])+1])
    return render_template('api/index.html', title=_('Api'),Api='active',api_list=api_list)

@bp.route('/csrf', methods=['POST'])
def csrf():
    headers = {'Content-Type': 'application/json'}
    if request.method == 'POST':
        # print(request.get_json(force=True))
        target = request.form['pub']+'/'+request.form['machine']
        print(target)
        # target = 'http://feb34695.ngrok.io' +'/'+request.form['machine']
        data = { k:v for k,v in request.form.to_dict().items() }
        print(type(data))
        print(data)

        r = requests.post(target, data=data)
        print("content", r.content, type(r.content))
        print("json", r.json(), type(r.json()))

        if not r.ok:
            return _('Error: the translation service failed.')
        # xx =json.loads(r.content.decode('utf-8-sig'))
        # print(xx)
        return jsonify(r.json())
    else:
        abort(400)
