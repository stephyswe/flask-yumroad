from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from yumroad.models import Product, db
from yumroad.forms import ProductForm

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def index():
    all_products = Product.query.all()
    return render_template('products/index.html', products=all_products)

@product_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('.details', product_id=product.id))
    return render_template('products/new.html', form=form)

@product_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
def edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        # db edit data
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('products/edit.html', product=product, form=form)

@product_bp.route('/<int:product_id>/delete', methods=['GET', 'POST', 'DELETE'])
def delete(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    product.name = form.name.data
    product.description = form.description.data
    # db delete data
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('.index'))

@product_bp.route('/<int:product_id>')
def details(product_id):
    product = Product.query.get_or_404(product_id)
    # Equivalent to:
    # product = Product.query.get(product_id)
    # if not product:
    #    abort(404)
    return render_template('products/details.html', product=product)

@product_bp.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404