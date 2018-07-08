from flask import render_template, redirect, url_for, flash, request,abort,jsonify
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from app.api import bp
from ext import db,desc

import json
import requests
import pprint

def union(x,y):
    x=set(x)
    y=set(y)
    return list(x.union(y))
def slave_check(servers):
    rq_job = current_app.task_queue.enqueue('app.tasks.query_servers',servers,
                                            *args, **kwargs)


# def get_tasks_in_progress():
#     return Ngrok.query.filter_by(complete=False).all()

# def get_task_in_progress(slave_id):
#     return Ngrok.query.filter_by(id=slave_id,complete=False).first()
    
# def rs_get(urls,ids):
#     rs = (grequests.get(u, timeout=2.6) for u in urls)
#     print(urls,ids)
#     temp = grequests.map(rs)
#     print(temp)
#     return dict(zip(ids,map(lambda x:x.status_code if x else 404,temp)))

# def rs_post(urls,data):
#     rs = (grequests.post(u, data=data,timeout=3) for u in urls)
#     return grequests.map(rs)
@bp.route('/', methods=['GET', 'POST'])
def index():
    ngroks = Ngrok.query.all()
    # ngroks = union(Ngrok.query.filter_by(status='200'), Ngrok.query.order_by(desc(Ngrok.time)))
    print('1,',ngroks)
    #object => dict
    api_list = list(map(lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns},ngroks))
    if(len(api_list)>5):
        api_list = api_list[:5]
    for i in api_list:
        if 'info' not in i.keys():
            i['info'] = 'unkown'
    if request.method == 'GET':
        cache = rs_get([i['pub'] for i in api_list], [i['id']
                                                        for i in api_list])
        # print('cache',cache)
        for i in range(len(cache)):
            ngroks[i].status = cache[str(ngroks[i].id)]
        db.session.commit()
        
    if request.method == 'POST':
        api = list(filter(lambda i: i['id'] == request.form['id'], api_list))[0]
        target = api['pub']+'/'+request.form['machine']
        data = {k: v for k, v in request.form.to_dict().items()}
        print(data)
        rs = rs_post([target], data)[0]
        ng = Ngrok.query.filter_by(id=api['id'])
        ng.status = rs.status_code
        db.session.commit()
        if rs.status_code==200:
            api['status'] = rs.status_code
            api['info'] = rs.json()['info']
            return jsonify(api)
        api['info']='error'
        return jsonify(api)
    return render_template('api/index.html', title=_('Api'),Api='active',api_list=api_list)

# @bp.route('/csrf', methods=['POST'])
# def csrf():
#     if request.method == 'POST':
#         ngroks = Ngrok.query.all()
#         api_list = list(map(lambda r: {c.name: str(
#             getattr(r, c.name)) for c in r.__table__.columns}, ngroks))
#         # print(request.get_json(force=True))
#         api = list(filter(lambda i: i['id'] ==
#                           request.form['id'], api_list))[0]
#         target = api['pub']+'/'+request.form['machine']
#         print(target)
#         # target = 'http://feb34695.ngrok.io' +'/'+request.form['machine']
#         data = { k:v for k,v in request.form.to_dict().items() }
#         print(type(data))
#         print(data)

#         r = requests.post(target, data=data)
#         print("content", r.content, type(r.content))
#         print("json", r.json(), type(r.json()))

#         if not r.ok:
#             return _('Error: the translation service failed.')
#         # xx =json.loads(r.content.decode('utf-8-sig'))
#         # print(xx)
#         return jsonify(r.json())
#     else:
#         abort(400)
