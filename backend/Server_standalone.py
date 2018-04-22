"""
Routes and views for the flask application.
"""
import RPi.GPIO as GPIO
from datetime import datetime
from flask import render_template,jsonify,abort,request
from os import environ
from flask import Flask
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
now = datetime.now()

s_t = 0

def G_shake(on=True):
    GPIO.output(2,True)
    GPIO.output(3,on)

def G_light(on=True,r=False,b=False,q=False):
    GPIO.output(26,on)
    GPIO.output(19,r)
    GPIO.output(13,b)
    GPIO.output(6,q)

@app.before_request
def before_request():
    GPIO.setup(2,GPIO.OUT)
    GPIO.setup(3,GPIO.OUT)
    GPIO.setup(26,GPIO.OUT)
    GPIO.setup(19,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(6,GPIO.OUT)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return 'helloworld'

@app.route('/shake',methods=['POST'])
def shake():
    dstatus=dict()
    print('shake-----Get-----Data')
    if request.method == 'POST' and request.form['machine']=='shake':
        global s_t
        s_t+=1
        #print(s_t)
        G_shake(s_t%2)
        if(s_t%2):
            dstatus['Status']='Machine On'
        else:
            dstatus['Status']='Machine Off'
        return jsonify(dstatus)
    else:
        abort(400)

@app.route('/light',methods=['POST','GET'])
def light():
    dstatus=dict()
    print('shake-----Get-----Data')
    if request.method == 'POST' and request.form['machine']=='shake':
        data = {k: v for k, v in request.form.to_dict().items()}
        G_light(1, **data)
        dstatus['Status']='Machine On'
        return jsonify(dstatus)
    else:
        abort(400)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT)
