from flask import Flask, render_template

from yumroad.blueprints.products import products
from yumroad.config import configurations
from yumroad.extensions import (db)


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])
    db.init_app(app)
    app.register_blueprint(products, url_prefix="/product")
    return app

# FLASK_DEBUG=true FLASK_APP="yumroad:create_app" flask run