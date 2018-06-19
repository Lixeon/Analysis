import os
from flask import Flask, request, current_app
from flask_restful import Api
from ext import db,migrate,bootstrap,babel,Config,images,cache
from app.models import NgrokAPI

def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config['SECRET_KEY']='dai3hoahudhiuahduiah'
    # app.config['BABEL_DEFAULT_LOCALE'] = 'zh_Hans_CN'
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    babel.init_app(app)
    images.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.show import bp as show_bp
    app.register_blueprint(show_bp, url_prefix='/start')

    from app.contact import bp as contact_bp
    app.register_blueprint(contact_bp, url_prefix='/contact')

    from app.api import bp as api_bp
    api = Api(api_bp)
    api.add_resource(NgrokAPI, '/ngrok')
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.data import bp as data_bp
    app.register_blueprint(data_bp, url_prefix='/data')

    from app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app




from app import models
