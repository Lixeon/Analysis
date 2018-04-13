from flask import Blueprint

bp = Blueprint('show', __name__)

from app.show import routes