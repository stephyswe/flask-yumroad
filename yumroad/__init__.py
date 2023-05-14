import sentry_sdk
from flask import Flask, render_template
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from webassets.loaders import PythonLoader as PythonAssetsLoader

# We need this line for alembic to discover the models.
from yumroad import assets
from yumroad.blueprints.checkout import checkout_bp
from yumroad.blueprints.landing import landing_bp
from yumroad.blueprints.products import product_bp
from yumroad.blueprints.rq_dashboard import rq_blueprint
from yumroad.blueprints.stores import store_bp
from yumroad.blueprints.users import user_bp
from yumroad.config import configurations
from yumroad.extensions import (
    assets_env,
    cache,
    checkout,
    csrf,
    db,
    debug_toolbar,
    login_manager,
    mail,
    migrate,
    rq2,
)


def create_app(environment_name="dev"):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])
    db.init_app(app)
    csrf.init_app(app)
    # need render_as_batch to correctly generate migrations for sqlite
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    mail.init_app(app)
    checkout.init_app(app)
    assets_env.init_app(app)
    rq2.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)

    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    if app.config.get("SENTRY_DSN"):  # pragma: no cover
        sentry_sdk.init(
            dsn=app.config["SENTRY_DSN"],
            # send_default_pii=True,
            integrations=[FlaskIntegration(), SqlalchemyIntegration()],
            send_default_pii=True,
            traces_sample_rate=1.0,
        )

    @app.errorhandler(401)
    def unauthorized_error(error):
        return render_template("errors/401.html"), 401  # pragma: no cover

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("errors/500.html"), 500  # pragma: no cover

    app.register_blueprint(product_bp, url_prefix="/product")
    app.register_blueprint(store_bp, url_prefix="/store")
    app.register_blueprint(user_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(landing_bp)

    # Admin tools
    app.register_blueprint(rq_blueprint, url_prefix="/rq")
    csrf.exempt(rq_blueprint)

    return app
