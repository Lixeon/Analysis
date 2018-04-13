import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                'you-will-never-assd'
    BOOTSTRAP_SERVE_LOCAL = True
    IMAGES_PATH = ["static/images"]
