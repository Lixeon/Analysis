from flask import render_template, redirect, url_for, flash, request,abort,jsonify
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from app.api import bp

import json
import requests
import grequests
import pprint


def rs_get(urls,ids):
    rs = (grequests.get(u, timeout=1) for u in urls)
    print(urls,ids)
    temp = grequests.map(rs)
    print(temp)
    return dict(zip(ids,map(lambda x:x.status_code if x else 404,temp)))

def rs_post(urls,data):
    rs = (grequests.post(u, data=data,timeout=3) for u in urls)
    return grequests.map(rs)
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
    pprint.pprint(api_list)
    cache = rs_get([i['pub'] for i in api_list], [i['id']
                                                      for i in api_list])
    for api in api_list:
        api['status'] = cache[api['id']]
    if request.method == 'POST':
        api = list(filter(lambda i: i['id'] == request.form['id'], api_list))[0]
        target = api['pub']+'/'+request.form['machine']
        data = {k: v for k, v in request.form.to_dict().items()}
        print(data)
        rs = rs_post([target], data)[0]
        if rs.status_code==200:
            api['status'] = rs.status_code
            api['info'] = rs.json()['info']
            return jsonify(api)
        api['info']='error'
        return jsonify(api)
    return render_template('api/index.html', title=_('Api'),Api='active',api_list=api_list)

@bp.route('/csrf', methods=['POST'])
def csrf():
    if request.method == 'POST':
        ngroks = Ngrok.query.all()
        api_list = list(map(lambda r: {c.name: str(
            getattr(r, c.name)) for c in r.__table__.columns}, ngroks))
        # print(request.get_json(force=True))
        api = list(filter(lambda i: i['id'] ==
                          request.form['id'], api_list))[0]
        target = api['pub']+'/'+request.form['machine']
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
