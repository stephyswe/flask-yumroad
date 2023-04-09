from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from yumroad.extensions import checkout
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
        price = form.price.data or 0
        product = Product(name=form.name.data,
                        description=form.description.data,
                        price_cents=int(price*100),
                        picture_url=form.picture_url.data,
                        creator=current_user,
                        store=current_user.store)
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
    stripe_publishable_key = checkout.publishable_key
    stripe_session = checkout.create_session(product) or {}
    session_id = stripe_session.get('id')

    return render_template('products/details.html',
                            product=product,
                            stripe_publishable_key=stripe_publishable_key,
                            checkout_session_id=session_id)

@product_bp.route('/<product_id>/post_checkout')
def post_checkout(product_id):
    product = Product.query.get_or_404(product_id)
    purchase_state = request.args.get('status')
    post_purchase_session_id = request.args.get('session_id')
    if purchase_state == 'success' and post_purchase_session_id:
        flash("Thanks for purchasing {}. You will receive an email shortly".format(product.name), 'success')
    elif purchase_state == 'cancel' and post_purchase_session_id:
        flash("There was an error while attempting to purchase this product. Try again", 'danger')
    return redirect(url_for('.details', product_id=product_id))

@product_bp.errorhandler(404)
def not_found(exception):
    return render_template('products/404.html'), 404