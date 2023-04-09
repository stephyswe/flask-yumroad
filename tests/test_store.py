from flask import url_for
import pytest

from yumroad.models import db, Product, Store

def create_store(name="Example Store", num_products=0):
    store = Store(name=name)
    for index in range(num_products):
        product = Product(name="Product {}".format(index), description="example",
                          store=store)
        db.session.add(product)
    db.session.add(store)
    db.session.commit()
    return store

# Unit Tests
def test_store_creation(client, init_database):
    assert Store.query.count() == 0
    assert Product.query.count() == 0
    store = create_store(num_products=3)
    assert Store.query.count() == 1
    assert Product.query.count() == 3
    for product in Product.query.all():
        assert product.store == store

def test_name_validation(client, init_database):
    assert Store.query.count() == 0
    with pytest.raises(ValueError):
        create_store(name="bad")
    assert Store.query.count() == 0

# Functional Tests
def test_index_page(client, init_database):
    store = create_store(num_products=5)
    response = client.get(url_for('store.index'))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert store.name in str(response.data)

    expected_link = url_for('store.show', store_id=store.id)
    assert expected_link in str(response.data)
    for product in store.products[:3]:
        expected_link = url_for('product.details', product_id=product.id)
        assert expected_link in str(response.data)

    for product in store.products[3:5]:
        expected_link = url_for('product.details', product_id=product.id)
        assert expected_link not in str(response.data)

# TODO: Use a store fixture
def test_store_page(client, init_database):
    store = create_store(num_products=3)
    response = client.get(url_for('store.show', store_id=store.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert store.name in str(response.data)

    for product in store.products:
        expected_link = url_for('product.details', product_id=product.id)
        assert expected_link in str(response.data)
