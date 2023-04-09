from flask import Blueprint, render_template

from yumroad.models import Store, Product, db

store_bp = Blueprint('store', __name__)

@store_bp.route('/')
def index():
    stores = Store.query.all()
    return render_template('stores/index.html', stores=stores)

@store_bp.route('/store/<store_id>')
@store_bp.route('/store/<store_id>/<int:page>')
def show(store_id, page=1):
    store = Store.query.get_or_404(store_id)
    per_page = 9
    products = Product.query.filter_by(store=store).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('stores/show.html', store=store, products=products)
