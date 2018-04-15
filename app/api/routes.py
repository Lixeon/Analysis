from flask import render_template, redirect, url_for, flash, request
from flask_restful import Resource, reqparse, fields, marshal
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from sqlalchemy import desc
from ext import api,db
from app.api import bp



ngrok_fields={
    "url":fields.String,
    'time':fields.String,
}
class NgrokAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, location='json')
        self.reqparse.add_argument('time', type=str, location='json')
        super(TaskAPI, self).__init__()

    def get(self):
        ngrok=Ngrok.query.order_by(desc(Ngrok.time))[0]
        ngrok_dict = {'url': ngrok.url,'time':ngrok.time}
        return {'Ngrok': marshal(ngrok_dict, ngrok_fields)}

    def post(self):

        t = {
        'url': None,
        'time':None
        }
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                t[k] = v
        ng = Ngrok(**t)
        db.session.add(ng)
        db.session.commit()
        return {'message': 'Connect Complete.'}


api.add_resource(NgrokAPI, '/api/ngrok', endpoint='ngrok')
@bp.route('/', methods=['GET', 'POST'])
def  index():
    return render_template('api/index.html', title=_('Api'),Api='active')
