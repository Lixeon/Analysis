
from flask import abort,url_for
from flask_restful import Resource, reqparse, fields, marshal
from passlib.apps import custom_app_context as pwd_context
from ext import db, desc

ngrok_fields={
    "url":fields.String,
    'time':fields.String,
}

class Ngrok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), index=True, unique=True)
    time = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Server {}>'.format(self.url)
    @staticmethod
    def _asdict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d

class NgrokAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, location='json')
        self.reqparse.add_argument('time', type=str, location='json')
        super(NgrokAPI, self).__init__()

    def get(self):
        ngrok=Ngrok.query.order_by(desc(Ngrok.time))[0]
        return {'Ngrok': marshal(Ngrok._asdict(ngrok), ngrok_fields)}

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
        if(t['url'] and Ngrok.query.filter_by(url=t['url']).first() is None):
            db.session.add(ng)
            db.session.commit()
        return {'message': 'Connect Complete.'}
    

