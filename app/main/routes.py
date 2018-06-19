from flask import flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as _l
from flask_babel import _
from flask_images import resized_img_src
from flask_login import current_user, login_user, logout_user

from app.main import bp
from ext import cache


@cache.cached(timeout=50)
@bp.route('/')
def start():
    return redirect(url_for('show.index'))


@cache.cached(timeout=50)
@bp.route('/main', methods=['GET', 'POST'])
def  index():
    return render_template('main/index.html', title=_('Home'),main='active')
