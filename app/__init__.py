import os
from flask import Flask, request, current_app
from ext import bootstrap,babel,Config,images




def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config['SECRET_KEY']='dai3hoahudhiuahduiah'
    # app.config['BABEL_DEFAULT_LOCALE'] = 'zh_Hans_CN'
    app.config.from_object(config_class)


    bootstrap.init_app(app)
    babel.init_app(app)
    images.init_app(app)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.show import bp as show_bp
    app.register_blueprint(show_bp, url_prefix='/start')

    from app.contact import bp as contact_bp
    app.register_blueprint(contact_bp, url_prefix='/contact')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.data import bp as data_bp
    app.register_blueprint(data_bp)

   
    return app




from app import models
