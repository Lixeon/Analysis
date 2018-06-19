from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as _l
from flask_babel import _
from flask_login import current_user, login_user, logout_user

from app.dashboard import bp
from ext import cache


@cache.cached(timeout=50)
@bp.route('/dashboard', methods=['GET', 'POST'])
def  index():
    return render_template('dashboard/index.html', title=_('dashboard'), dashboard='active')

@cache.cached(timeout=50)
@bp.route('/dashboard/order', methods=['GET', 'POST'])
def order():
    return render_template('dashboard/order.html', title=_('orderTracking'), dashboard='active')
