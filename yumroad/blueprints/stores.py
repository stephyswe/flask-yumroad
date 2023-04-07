from flask import Blueprint, render_template
from yumroad.models import Store, db

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def index():
    stores = Store.query.all()
    return render_template('stores/index.html', stores=stores)

@store_bp.route('/<store_id>')
def show(store_id):
    store = Store.query.get_or_404(store_id)
    products = store.products
    return render_template('stores/show.html', store=store, products=products)
