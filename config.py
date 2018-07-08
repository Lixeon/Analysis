import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                'you-will-never-assd'
    BOOTSTRAP_SERVE_LOCAL = True
    IMAGES_PATH = ["static/images"]

    
