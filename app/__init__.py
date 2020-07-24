from flask import Flask, render_template
# from flask.ext.bootstrap import Bootstrap
# from flask.ext.moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config


# bootstrap = Bootstrap()
# moment = Moment()
db = SQLAlchemy()

def create_app(config_name):

    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # bootstrap.init_app(app)
    # moment.init_app(app)
    
    db.init_app(app)

   
    # Blueprints for view pages
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    
    
    return app