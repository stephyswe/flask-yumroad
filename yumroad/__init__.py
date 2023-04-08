from flask import Flask, redirect, url_for

from yumroad.blueprints.products import product_bp
from yumroad.blueprints.users import user_bp
from yumroad.blueprints.stores import store_bp
from yumroad.config import configurations
from yumroad.extensions import (db, csrf, login_manager, migrate, mail)
# We need this line for alembic to discover the models.
import yumroad.models


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])
    db.init_app(app)
    csrf.init_app(app)
    # need render_as_batch to correctly generate migrations for sqlite
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    mail.init_app(app)

    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(store_bp, url_prefix='/store')
    app.register_blueprint(user_bp)

    @app.route('/')
    def home():
        return redirect(url_for('store.index'))
    return app
    

# FLASK_DEBUG=true FLASK_APP="yumroad:create_app" flask run