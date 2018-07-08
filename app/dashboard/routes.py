from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as _l
from flask_babel import _
from flask_login import current_user, login_user, logout_user

from app.dashboard import bp
from ext import cache

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
import pandas as pd



# Create the main plot

def make_ajax_plot():
    source = AjaxDataSource(data_url=request.url_root + 'data/',
                            polling_interval=2000, mode='append')

    source.data = dict(x=[], y=[])

    plot = figure(plot_height=300, sizing_mode='scale_width')
    plot.line('x', 'y', source=source, line_width=4)

    script, div = components(plot)
    return script, div
def make_plot():
    plot = figure(plot_height=300, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div




@bp.route('/data/', methods=['POST'])
def data():
    global x
    x += 1
    y = 2**x
    return jsonify(x=x, y=y)

@bp.route('/', methods=['GET', 'POST'])
def  index():
	fig = figure(plot_width=600, plot_height=600)
	fig.vbar(
		x=[1, 2, 3, 4],
		width=0.5,
		bottom=0,
		top=[1.7, 2.2, 4.6, 3.9],
		color='navy'
	)
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	# render template
	script, div = components(fig)

	return render_template('dashboard/iris_index.html',plot_script=script,plot_div=div,js_resources=js_resources,css_resources=css_resources)
    # return render_template('dashboard/index.html', title=_('dashboard'), dashboard='active')

@cache.cached(timeout=50)
@bp.route('/order', methods=['GET', 'POST'])
def order():
    return render_template('dashboard/order.html', title=_('orderTracking'), dashboard='active')
