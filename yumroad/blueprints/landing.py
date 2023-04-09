from flask import Blueprint, render_template
from flask_login import current_user
from sqlalchemy.orm import joinedload

from yumroad.extensions import cache
from yumroad.models import Store

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
@cache.cached(timeout=300, unless=lambda: current_user.is_authenticated)
def index():
    stores = Store.query.options(joinedload(Store.products)).limit(3).all()
    return render_template('landing/index.html', stores=stores)
