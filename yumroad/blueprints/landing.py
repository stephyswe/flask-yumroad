from flask import Blueprint, render_template

from yumroad.models import Store

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/')
def index():
    # This is a bad query, we'll optimize it later
    stores = Store.query.limit(3).all()
    return render_template('landing/index.html', stores=stores)
