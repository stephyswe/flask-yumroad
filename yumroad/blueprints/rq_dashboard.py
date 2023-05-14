import rq_dashboard
from flask import current_app
from flask_login import current_user

rq_blueprint = rq_dashboard.blueprint


@rq_blueprint.before_request
def authenticate(*args, **kwargs):  # pragma: no cover
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
