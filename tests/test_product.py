from flask import url_for
import pytest

from yumroad.models import db, Product, User

def create_product(name="Sherlock Homes", description="a house hunting real estate agent", user=None, store=None):
    user = user or User.create("owner@example.com", "test")
    product = Product(name="Sherlock Homes", description="a house hunting detective")
    db.session.add(product)
    db.session.commit()
    return product

# Unit Tests
def test_product_creation(client, init_database):
    assert Product.query.count() == 0
    create_product()
    assert Product.query.count() == 1

def test_name_validation(client, init_database):
    assert Product.query.count() == 0
    with pytest.raises(ValueError):
        Product(name="bad", description="should be an invalid name")
    assert Product.query.count() == 0

# Functional Tests
def test_index_page(client, init_database):
    product = create_product()
    response = client.get(url_for('product.index'))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert product.name in str(response.data)
    expected_link = url_for('product.details', product_id=product.id)
    assert expected_link in str(response.data)

def test_details_page(client, init_database):
    product = create_product()
    response = client.get(url_for('product.details', product_id=product.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert b'Purchase coming soon' in response.data
    assert product.name in str(response.data)

def test_non_existent_book(client, init_database):
    product = create_product()
    response = client.get(url_for('product.details', product_id=product.id+1))
    assert response.status_code == 404

def test_unauthed_new_page(client, init_database):
    response = client.get(url_for('product.create'))
    assert response.status_code == 302
    assert response.location == '/login'
    #assert response.location == url_for('user.login', _external=True)

def test_new_page(client, init_database, authenticated_request):
    import flask
    print(flask.session)
    response = client.get(url_for('product.create'))

    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Create' in response.data

def test_creation(client, init_database, authenticated_request):
    response = client.post(url_for('product.create'),
                            data=dict(name='test product', description='is persisted'),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'test product' in response.data
    assert b'Purchase' in response.data

def test_invalid_creation(client, init_database, authenticated_request):
    response = client.post(url_for('product.create'),
                            data=dict(name='ab', description='is not valid'),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'is not valid' in response.data
    assert b'Field must be between' in response.data
    assert b'is-invalid' in response.data

def test_edit_page(client, init_database):
    product = create_product()
    response = client.get(url_for('product.edit', product_id=product.id))
    assert response.status_code == 200
    assert product.description in str(response.data)
    assert product.name in str(response.data)
    assert b'Edit' in response.data

def test_edit_submission(client, init_database):
    product = create_product()
    old_description = product.description
    old_name = product.name
    response = client.post(url_for('product.edit', product_id=product.id),
                            data={'name': 'test-change', 'description': 'is persisted'},
                            follow_redirects=True)
    assert response.status_code == 200
    assert 'test-change' in str(response.data)
    assert 'is persisted' in str(response.data)
    assert old_description not in str(response.data)
    assert old_name not in str(response.data)
    assert b'Yumroad All Products' not in response.data

def test_invalid_edit_submission(client, init_database):
    product = create_product()
    old_description = product.description
    old_name = product.name
    response = client.post(url_for('product.edit', product_id=product.id),
                            data=dict(name='br0', description='is persisted'),
                            follow_redirects=True)
    assert response.status_code == 200
    assert b'br0' in response.data
    assert b'Field must be between 4 and 60 characters long' in response.data
    assert Product.query.get(product.id).description == old_description
    assert old_description not in str(response.data)
    assert old_name in str(response.data) # It's still in the page title
    assert b'Edit' in response.data

def test_delete_page(client, init_database):
    product = create_product()
    response = client.post(url_for('product.delete', product_id=product.id), follow_redirects=True)
    assert response.status_code == 200
    assert product.description not in str(response.data)
    assert product.name not in str(response.data)
    assert b'All Products' in response.data

def test_invalid_delete_page(client, init_database):
    product = create_product()
    response = client.post(url_for('product.delete', product_id=product.id+1), follow_redirects=True)
    assert response.status_code == 404
    assert b'Whoops' in response.data and \
       b"we couldn't find that product" in response.data