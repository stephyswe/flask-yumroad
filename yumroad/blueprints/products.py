from flask import Blueprint, render_template, redirect, request, url_for, abort

from yumroad.models import Product, db
from yumroad.forms import ProductForm

products = Blueprint('products', __name__)

@products.route('/')
def index():
    all_products = Product.query.all()
    return render_template('products/index.html', products=all_products)

@products.route('/create', methods=['GET', 'POST'])
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.details', product_id=product.id))
    return render_template('products/new.html', form=form)

@products.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    # Equivalent to:
    # product = Product.query.get(product_id)
    # if not product:
    #    abort(404)
    return render_template('products/details.html', product=product)

@products.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404