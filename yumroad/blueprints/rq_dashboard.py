from flask import abort, current_app, request
from flask_login import current_user

from yumroad.models import User

import rq_dashboard
rq_blueprint = rq_dashboard.blueprint

@rq_blueprint.before_request
def authenticate(*args, **kwargs):  # pragma: no cover
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    # TODO: You should layer in some auth here
    # if not current_user == User.query.get(1):
    #     abort(401)
    pass