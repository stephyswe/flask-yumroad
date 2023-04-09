import time
import json

from flask import url_for
import pytest
import stripe
import vcr

from yumroad.models import db, Product, Store, User
from yumroad.extensions import checkout

DUMMY_WEBHOOK_SECRET = 'whsec_test_secret'
DUMMY_CUSTOMER_ID = 'cus_Ng84CNRBTFHcJ2' # If you're making live requests, this should be a real customer ID
TEST_CUSTOMER_EMAIL = 'moonchildeverlasting@gmail.com' # This email should correspond to the email on file for the customer ID above

def generate_header(payload, secret=DUMMY_WEBHOOK_SECRET, **kwargs):
    timestamp = kwargs.get("timestamp", int(time.time()))
    scheme = kwargs.get("scheme", stripe.WebhookSignature.EXPECTED_SCHEME)
    signature = kwargs.get("signature", None)
    if signature is None:
        payload_to_sign = "%d.%s" % (timestamp, payload)
        signature = stripe.WebhookSignature._compute_signature(
            payload_to_sign, secret
        )
    header = "t=%d,%s=%s" % (timestamp, scheme, signature)
    return {'Stripe-Signature': header}

# Unit Tests
def mock_webhook(event_name, data=None, webhook_secret=DUMMY_WEBHOOK_SECRET):
    payload = {}
    payload['type'] = event_name
    payload['data'] = {}
    payload['data']['object'] = data or {}
    data = json.dumps(payload)
    return data, generate_header(payload=data, secret=webhook_secret)

def test_parse_webhook(app):
    app_webhook_secret = app.config.get('STRIPE_WEBHOOK_KEY', DUMMY_WEBHOOK_SECRET)
    data, headers = mock_webhook('checkout.session.completed', webhook_secret=app_webhook_secret)
    parsed_event = checkout.parse_webhook(data, headers)
    assert parsed_event.type == 'checkout.session.completed'

def test_parse_invalid_webhook(app):
    data, headers = mock_webhook('checkout.session.completed', webhook_secret='bad secret')
    with pytest.raises(stripe.error.SignatureVerificationError):
        checkout.parse_webhook(data, headers)

@vcr.use_cassette('tests/cassettes/test_get_customer.yaml',
                  filter_headers=['authorization'], record_mode='once')
def test_get_customer(app):
    response = checkout.get_customer(DUMMY_CUSTOMER_ID)
    assert response.email == TEST_CUSTOMER_EMAIL


# Functional Test
@vcr.use_cassette('tests/cassettes/test_get_customer.yaml',
                  filter_headers=['authorization'], record_mode='once')
def test_event_webhook(app, init_database, user_with_product, client, mail_outbox):
    product = user_with_product.store.products[0]
    sample_data = {
        'customer': DUMMY_CUSTOMER_ID,
        'client_reference_id': product.id,
    }
    webhook_data, headers = mock_webhook('checkout.session.completed', data=sample_data)
    response = client.post(url_for('checkout.stripe_webhook'),
                            data=webhook_data,
                            headers=headers,
                            follow_redirects=True)

    assert response.status_code == 200
    assert len(mail_outbox) == 1
    email = mail_outbox[0]

    assert email.subject.startswith('Your purchase of')
    assert email.cc == [user_with_product.email]
    assert email.recipients == [TEST_CUSTOMER_EMAIL]

@vcr.use_cassette('tests/cassettes/test_get_customer.yaml',
                  filter_headers=['authorization'], record_mode='once')
def test_invalid_webhook_without_reference(app, init_database, client):
    sample_data = {
        'customer': DUMMY_CUSTOMER_ID,
    }
    webhook_data, headers = mock_webhook('checkout.session.completed', data=sample_data)
    response = client.post(url_for('checkout.stripe_webhook'),
                            data=webhook_data,
                            headers=headers,
                            follow_redirects=True)
    assert response.status_code == 400

@vcr.use_cassette('tests/cassettes/test_get_customer.yaml',
                  filter_headers=['authorization'], record_mode='once')
def test_checkout_with_invalid_product_id(app, init_database, user_with_product, client):
    product = user_with_product.store.products[0]
    sample_data = {
        'customer': DUMMY_CUSTOMER_ID,
        'client_reference_id': product.id + 1,
    }
    webhook_data, headers = mock_webhook('checkout.session.completed', data=sample_data)
    response = client.post(url_for('checkout.stripe_webhook'),
                            data=webhook_data,
                            headers=headers,
                            follow_redirects=True)

    assert response.status_code == 400
