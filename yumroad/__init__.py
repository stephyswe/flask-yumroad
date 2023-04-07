from flask import Flask, render_template

from yumroad.blueprints.products import product_bp
from yumroad.blueprints.users import user_bp
from yumroad.config import configurations
from yumroad.extensions import (db, csrf, login_manager)


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(user_bp)
    return app

# FLASK_DEBUG=true FLASK_APP="yumroad:create_app" flask run