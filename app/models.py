
from passlib.apps import custom_app_context as pwd_context
from flask import abort,url_for
from ext import db

class Ngrok(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128), index=True, unique=True)
    time = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Server {}>'.format(self.url)   


