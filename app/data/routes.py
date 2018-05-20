from functools import reduce

import numpy as np
from flask import json, jsonify, render_template, request
from flask_babel import lazy_gettext as _l
from flask_babel import _
from flask_login import current_user, login_user, logout_user

from app.data import bp
from app.models import Ngrok
from ext import cache, desc


def gen_vibration(t, sampling_rate, fft_size):
    x = np.sin(2*np.pi*156.25*t) + 2*np.sin(2*np.pi*234.375*t)
    xs = x[:fft_size]
    # xf = np.fft.rfft(xs)/fft_size
    # freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
    # xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
    # xfp2 = np.clip(np.abs(xf), 1e-20, 1e100)
    return xs      


def gen_speed(t, sampling_rate, fft_size):
    A = [round(np.random.random_sample()*1000, 2) for i in range(3)]
    W = [round(np.random.random_sample()*300, 2) for i in range(3)]
    ys = [i*np.sin(2*np.pi*j*t) for i, j in zip(A, W)]
    x = reduce((lambda x, y: x + y), ys)
    xs = x[:fft_size]
    return xs                                            

@cache.cached(timeout=50)
@bp.route('/', methods=['GET', 'POST'])
def  index():
    # data_set=dict()
    sampling_rate = 8000
    fft_size = 512
    t = np.arange(0, 1.0, 1.0/sampling_rate)
    tr = [round(i, 4) for i in t]
    x = np.linspace(0, 300, 256)
    xr = [round(i, 2) for i in x]

    y1 = [round(i, 2) for i in gen_speed(t, sampling_rate, fft_size)]
    y2 = [round(i, 2) for i in gen_vibration(t, sampling_rate, fft_size)]
    # fft_data = [round(i, 2) for i in fy]

    # data_set['orig'] = [{'i': i, 'x': x, 'y': x}
    #                     for i,(x, y) in enumerate(zip(xr, mix_data))]
    # data_set['ana'] = [{'i': i, 'x': x, 'y': x}
    #                    for i, (x, y) in enumerate(zip(xr, fft_data))]

    if request.method == 'POST':
        return jsonify({
            't':    tr,
            'x':    xr,
            'y1':   y1,
            'y2':   y2
        })
    if request.method == 'GET':
        return render_template('data/index.html', title=_('Data'), data='active')
    


@bp.route('/fft', methods=['GET', 'POST'])
def fft():

    if request.method == 'POST':
        x = json.loads(request.form['x'])
        y = np.asarray(json.loads(request.form['y']), dtype=float)
        # print(y.shape)
        fy = [20*np.log10(np.clip(np.abs(abs(np.fft.fft(i)) /
                                         len(x)), 1e-20, 1e100)) for i in y]
        fft_data = [[round(i, 2) for i in p] for p in fy]
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
