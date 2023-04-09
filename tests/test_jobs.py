from flask import url_for
import pytest

# Functional Tests
def test_get_rq_admin(client, init_database):
    response = client.get(url_for('rq_dashboard.overview'))
    assert response.status_code == 302

def test_get_rq_admin_authed(client, init_database, authenticated_request):
    authed_user = authenticated_request
    response = client.get(url_for('rq_dashboard.overview'))

    assert response.status_code == 200
    assert b'RQ Instances' in response.data
