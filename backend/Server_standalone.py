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
    GPIO.output(14, on)
    GPIO.output(15,on)

def G_light(on=True,r=False,b=False,q=False):
    GPIO.output(26,on)
    GPIO.output(19,r)
    GPIO.output(13,b)
    GPIO.output(6,q)

@app.before_request
def before_request():

    GPIO.setup(14,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)
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
            dstatus['info']='Machine On'
        else:
            dstatus['info'] = 'Machine Off'
        return jsonify(dstatus)
    else:
        abort(400)

@app.route('/light',methods=['POST','GET'])
def light():
    dstatus=dict()
    print('shake-----Get-----Data')
    if request.method == 'POST' and request.form['machine']=='light':
        data = {k: v for k, v in request.form.to_dict().items()}
        G_light(1, **data)
        dstatus['info'] = 'Machine On'
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

# import time
# import RPi.GPIO as GPIO

# chan1 = 13
# chan2 = 26

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(chan1, GPIO.OUT)
# GPIO.setup(chan2, GPIO.OUT)

# p = GPIO.PWM(chan1, 50)
# q = GPIO.PWM(chan2, 50)


# def start():
#     p.start(50)
#     q.start(50)


# def ch(freq):
#     p.ChangeFrequency(freq)
#     q.ChangeFrequency(freq)


# def cd(dc):
#     p.ChangeDutyCycle(dc)
#     q.ChangeDutyCycle(dc)

# def stop():
#     q.stop()
#     p.stop()


# import smbus
# import time
# bus = smbus.SMBus(1)
# address = 0x04


# def writeNumber(value):
#     bus.write_byte(address, value)
#     return -1


# def readNumber():
#     number = bus.read_byte(address)
#     return number


# var = input("Enter1–9:")
# writeNumber(var)
# print("RPI: Hi Arduino, I sent you ", var)
# # sleep one second
# time.sleep(1)
# number = readNumber()
# print("Arduino: Hey RPI,I received a digit", number)
# print("======================================\n")
