from flask import Blueprint

bp = Blueprint('dashbord', __name__)

from app.dashbord import routes