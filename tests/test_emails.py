from flask import url_for
import pytest

from yumroad.models import db, Product, Store, User
from yumroad.extensions import mail

from yumroad.email import send_basic_welcome_message, send_welcome_message, send_pretty_welcome_message

def test_basic_email(app, init_database, mail_outbox):
    send_basic_welcome_message('test@example.com')
    assert len(mail_outbox) == 1
    assert mail_outbox[0].subject == "Welcome to yumroad"

def test_template_email(app, init_database, mail_outbox, authenticated_request):
    user = User.query.first()
    send_welcome_message(user)
    assert len(mail_outbox) == 1
    assert mail_outbox[0].subject == "Welcome to yumroad Test Store"

def test_formatted_template_email(app, init_database, mail_outbox, authenticated_request):
    user = User.query.first()
    send_pretty_welcome_message(user)
    assert len(mail_outbox) == 1
    assert mail_outbox[0].subject == "Welcome to yumroad Test Store"
    assert 'btn-primary' in mail_outbox[0].html