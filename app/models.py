
from flask import abort,url_for
from flask_restful import Resource, reqparse, fields, marshal
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import desc
from ext import db

class Ngrok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), index=True, unique=True)
    time = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Server {}>'.format(self.url)   

ngrok_fields={
    "url":fields.String,
    'time':fields.String,
}

class NgrokAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, location='json')
        self.reqparse.add_argument('time', type=str, location='json')
        super(NgrokAPI, self).__init__()

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
        if(t['url']):
            db.session.add(ng)
            db.session.commit()
        return {'message': 'Connect Complete.'}

