from flask import url_for
import pytest

# Functional Tests


def test_guest_index_page(client, init_database, user_with_product):
    store = user_with_product.store
    response = client.get(url_for("landing.index"))
    assert response.status_code == 200
    assert b"Yumroad" in response.data
    assert b"The easiest way" in response.data
    assert b"Create a store" in response.data
    assert store.name in str(response.data)


def test_logged_in_index_page(client, init_database, authenticated_request):
    authed_user = authenticated_request
    response = client.get(url_for("landing.index"))

    assert response.status_code == 200
    assert b"Yumroad" in response.data
    assert b"The easiest way" in response.data
    assert b"Create a store" not in response.data
    assert authed_user.store.name in str(response.data)
    assert "Logout" in str(response.data)
