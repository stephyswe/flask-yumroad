from flask import render_template
from flask_mail import Message

from yumroad.extensions import mail
from yumroad.jobs import mailer

DEFAULT_FROM = ('Yumroad', 'yumroad@example.com')

def send_basic_welcome_message(recipient_email):
    subject = 'Welcome to yumroad'
    body = "Thanks for joining. Let us know if you have any questions!"
    recipients = [recipient_email]
    mailer.send_email.queue(subject, DEFAULT_FROM, recipients, body, text_body=body)

def send_welcome_message(user):
    store = user.store
    subject = 'Welcome to yumroad {}'.format(store.name)
    body = render_template('emails/welcome_basic.html', store=store)
    recipients = [user.email]
    mailer.send_email.queue(subject, DEFAULT_FROM, recipients, body)

def send_pretty_welcome_message(user):
    store = user.store
    subject = 'Welcome to yumroad {}'.format(store.name)
    body = render_template('emails/welcome_pretty.html', store=store)
    recipients = [user.email]
    mailer.send_email.queue(subject, DEFAULT_FROM, recipients, body)

def send_purchase_email(email, product):
    store = product.store
    subject = 'Your purchase of {} from {}'.format(product.name, store.name)
    recipients = [email]
    cc_recipients = [store.user.email]
    body = render_template('emails/welcome_pretty.html', store=store)
    mailer.send_email.queue(subject, DEFAULT_FROM, recipients, body, cc=cc_recipients)
