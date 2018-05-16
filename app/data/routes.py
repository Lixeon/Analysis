from flask import render_template, jsonify, request,json
from flask_login import  login_user, logout_user, current_user
from flask_babel import  _, lazy_gettext as _l
from app.models import Ngrok
from app.data import bp
from ext import desc,cache
from functools import reduce
import numpy as np

@cache.cached(timeout=50)
@bp.route('/', methods=['GET', 'POST'])
def  index():
    data_set=dict()
    x = np.linspace(0, 300, 300)

    A = [round(np.random.random_sample()*1000, 2) for i in range(3)]
    W = [round(np.random.random_sample()*300, 2) for i in range(3)] # yi=A*sin(2*pi*W*x)
    # Ax= [np.random.random_sample()*100 for i in range(3) ]
    ys = [i*np.sin(2*np.pi*j*x) for i, j in zip(A, W)]              # y=sum(yi)

    y = reduce((lambda x, y: x + y), ys)
    ys = list(map(lambda x: x.tolist(), ys))

    print(type(y))
    fy = abs(np.fft.fft(y))/len(x)

    xr = [round(i, 2) for i in x]
    mix_data = [round(i, 2) for i in y]
    fft_data = [round(i, 2) for i in fy]

    data_set['orig'] = [{'i': i, 'x': x, 'y': x}
                        for i,(x, y) in enumerate(zip(xr, mix_data))]
    data_set['ana'] = [{'i': i, 'x': x, 'y': x}
                       for i, (x, y) in enumerate(zip(xr, fft_data))]
    if request.method == 'POST':
        return jsonify({
            'x':    xr,
            'y': mix_data,
            'ys': ys
        })
    if request.method == 'GET':
        return render_template('data/index.html', title=_('Data'), data='active', data_set=data_set)
    

@cache.cached(timeout=50)
@bp.route('/fft', methods=['GET', 'POST'])
def fft():

    if request.method == 'POST':
        x = json.loads(request.form['x'])
        y = np.asarray(json.loads(request.form['y']), dtype=float)
        # print(type(y))
        fy = abs(np.fft.fft(y))/len(x)
        fft_data = [round(i, 2) for i in fy]
        return jsonify(
            {
                'x': x,
                'y': fft_data
            }
        )


@bp.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        x = request.form['x']
        y = request.form['y']
        fy = abs(np.fft.fft(y))/len(x)
        fft_data = [round(i, 2) for i in fy]
        return jsonify(
            {
                'x':x,
                'fft': fft_data
            }
        )


@cache.cached(timeout=50)
@bp.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        x = request.form['x']
        y = request.form['y']
        fy = abs(np.fft.fft(y))/len(x)
        fft_data = [round(i, 2) for i in fy]
        return jsonify(
            {
                'x':x,
                'fft': fft_data
            }
        )
