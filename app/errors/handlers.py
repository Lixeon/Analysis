from flask import render_template
from flask_babel import lazy_gettext as _l
from flask_babel import _

from app.errors import bp
from ext import cache


@cache.cached(timeout=50)
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@cache.cached(timeout=50)
@bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
