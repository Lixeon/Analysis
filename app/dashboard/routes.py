from flask import render_template, redirect, url_for, flash, request
from flask_login import  login_user, logout_user, current_user
from flask_babel import  _, lazy_gettext as _l
from app.dashboard import bp

import numpy as np
from functools import reduce
@bp.route('/dashboard', methods=['GET', 'POST'])
def  index():
    x = np.linspace(0, 300, 300)
    
    Ax = [round(np.random.random_sample()*1000,2) for i in range(3)]
    Aw = [round(np.random.random_sample()*300, 2) for i in range(3)]
    # Ax= [np.random.random_sample()*100 for i in range(3) ]
    ys = [i*np.sin(2*np.pi*j*x) for i, j in zip(Ax, Aw)]
    y = reduce((lambda x, y: x + y), ys)
    fy = abs(np.fft.fft(y))/len(x)

    xr = [round(i,2) for i in x]
    x_data = [round(i,2) for i in range(300)]
    ori_data = [[round(i, 2) for i in y] for y in ys]
    mix_data = [round(i, 2) for i in y]
    fft_data = [round(i, 2) for i in fy[:len(x)//2]]
    
    return render_template('dashboard/index.html', title=_('dashboard'), dashboard='active', x_data=x_data, mix_data=mix_data, ori_data=ori_data, fft_data=fft_data, collection=zip(x_data, xr, mix_data, fft_data))
