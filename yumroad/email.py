from flask import render_template
from flask_mail import Message
from yumroad.extensions import mail

DEFAULT_FROM = ('Yumroad', 'yumroad@example.com')

def send_basic_welcome_message(recipient_email):
    message = Message('Welcome to yumroad',
                      sender=DEFAULT_FROM,
                      recipients=[recipient_email],
                      body="Thanks for joining. Let us know if you have any questions!")
    mail.send(message)

def send_welcome_message(user):
    message = Message('Welcome to yumroad {}'.format(user.store.name),
                      sender='to@example.com',
                      recipients=[user.email])

    message.html = render_template('emails/welcome_basic.html', store=user.store)
    mail.send(message)

def send_pretty_welcome_message(user):
    message = Message('Welcome to yumroad {}'.format(user.store.name),
                      sender=DEFAULT_FROM,
                      recipients=[user.email])

    message.html = render_template('emails/welcome_pretty.html', store=user.store)
    mail.send(message)

def send_purchase_email(email, product):
    store = product.store
    message = Message('Your purchase of {} from {}'.format(product.name, store.name),
                      sender=DEFAULT_FROM,
                      cc=[store.user.email],
                      recipients=[email])

    message.html = render_template('emails/purchase.html', product=product)
    mail.send(message)