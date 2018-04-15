from flask import render_template, redirect, url_for, flash, request
from flask_restful import Resource, reqparse, fields, marshal
from models import Ngrok
from sqlalchemy import desc
from ext import api,db
from app.api import bp


api.add_resource(NgrokAPI, '/api/ngrok',endpoint = 'ngrok')


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
        ngrok=Ngrok.query.order_by(desc(Ngrok.time))
        print(ngrok)
        return {'Ngrok': marshal(ngrok, ngrok_fields)}

    def post(self):
        
        t = {
        'public_url': None,
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

@bp.route('/', methods=['GET', 'POST'])
def  index():
    return render_template('api/index.html', title=_('Api'),Api='active')

