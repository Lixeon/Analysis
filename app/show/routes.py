from flask import flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as _l
from flask_babel import _
from flask_login import current_user, login_user, logout_user

from app.show import bp
from ext import cache


@cache.cached(timeout=50)
@bp.route('/', methods=['GET', 'POST'])
def  index():
    return render_template('show/index.html', title=_('Start'))
