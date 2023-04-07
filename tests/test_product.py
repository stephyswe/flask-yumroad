from flask import url_for
import pytest

from yumroad.models import db, Product

@pytest.fixture
def sample_book(name="Sherlock Homes", description="a house hunting real estate agent"):
    book = Product(name=name, description=description)
    db.session.add(book)
    db.session.commit()
    return book

def test_product_creation(client, init_database, sample_book):
    assert Product.query.count() == 1
    assert Product.query.first().name == sample_book.name

def test_name_validation(client, init_database):
    with pytest.raises(ValueError):
        Product(name="", description="invalid book")

def test_index_page(client, init_database, sample_book):
    response = client.get(url_for('products.index'))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert sample_book.name in str(response.data)

    expected_link = url_for('products.details', product_id=sample_book.id)
    assert expected_link in str(response.data)

def test_details_page(client, init_database, sample_book):
    response = client.get(url_for('products.details', product_id=sample_book.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert b'Purchase coming soon' in response.data
    assert sample_book.name in str(response.data)

def test_non_existent_book(client, init_database, sample_book):
    response = client.get(url_for('products.details', product_id=sample_book.id+1))
    assert response.status_code == 404

def test_new_page(client, init_database):
    response = client.get(url_for('products.create'))

    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Create' in response.data

def test_creation(client, init_database):
    response = client.post(url_for('products.create'),
                            data=dict(name='test product', description='is persisted'),
                            follow_redirects=True)
    assert response.status_code == 200
    assert b'test product' in response.data
    assert b'Purchase' in response.data

def test_invalid_creation(client, init_database):
    response = client.post(url_for('products.create'),
                            data=dict(name='ab', description='is not valid'),
                            follow_redirects=True)
    assert response.status_code == 200
    assert b'is not valid' in response.data
    assert b'Field must be between' in response.data
    assert b'is-invalid' in response.data

def test_edit_page(client, init_database, sample_book):
    response = client.get(url_for('products.edit', product_id=sample_book.id))
    assert response.status_code == 200
    assert sample_book.description in str(response.data)
    assert sample_book.name in str(response.data)
    assert b'Edit' in response.data

def test_edit_submission(client, init_database, sample_book):
    old_description = sample_book.description
    old_name = sample_book.name
    response = client.post(url_for('products.edit', product_id=sample_book.id),
                            data={'name': 'test-change', 'description': 'is persisted'},
                            follow_redirects=True)
    assert response.status_code == 200
    assert 'test-change' in str(response.data)
    assert 'is persisted' in str(response.data)
    assert old_description not in str(response.data)
    assert old_name not in str(response.data)
    assert b'Yumroad All Products' not in response.data

def test_invalid_edit_submission(client, init_database, sample_book):
    old_description = sample_book.description
    old_name = sample_book.name
    response = client.post(url_for('products.edit', product_id=sample_book.id),
                            data=dict(name='br0', description='is persisted'),
                            follow_redirects=True)
    assert response.status_code == 200
    assert b'br0' in response.data
    assert b'Field must be between 4 and 60 characters long' in response.data
    assert Product.query.get(sample_book.id).description == old_description
    assert old_description not in str(response.data)
    assert old_name in str(response.data) # It's still in the page title
    assert b'Edit' in response.data

def test_delete_page(client, init_database, sample_book):
    response = client.post(url_for('products.delete', product_id=sample_book.id), follow_redirects=True)
    assert response.status_code == 200
    assert sample_book.description not in str(response.data)
    assert sample_book.name not in str(response.data)
    assert b'All Products' in response.data

def test_invalid_delete_page(client, init_database, sample_book):
    response = client.post(url_for('products.delete', product_id=sample_book.id+1), follow_redirects=True)
    assert response.status_code == 404
    assert b'Whoops' in response.data and \
       b"we couldn't find that product" in response.data