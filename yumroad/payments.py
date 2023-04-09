from urllib.parse import unquote
from flask import url_for
import stripe

class Checkout:
    def init_app(self, app):
        stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
        self.publishable_key = app.config.get('STRIPE_PUBLISHABLE_KEY')
        self.webhook_key = app.config.get('STRIPE_WEBHOOK_KEY')

    def create_session(self, product):
        if not product.price_cents:
            return
        success_url = unquote(url_for('product.post_checkout', product_id=product.id,
                              session_id='{CHECKOUT_SESSION_ID}',
                              status='success',
                              _external=True))
        failure_url = unquote(url_for('product.post_checkout', product_id=product.id,
                              session_id='{CHECKOUT_SESSION_ID}',
                              status='cancel',
                              _external=True))

         # http://localhost:8000/product/1/post-checkout?session_id={%7DCHECKOUT_SESSION_ID}&status=success/cancel

        # Find or create customer
        """ existing_customers = stripe.Customer.list(email=product.creator.email, limit=1).data
        if existing_customers:
            customer = existing_customers[0]
            print(f"Customer already exists: {customer.id}")
        else:
            customer = stripe.Customer.create(
                email=product.creator.email,
                payment_method="pm_card_visa",
            )
            print(f"Created customer: {customer.id}") """
        
        session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    client_reference_id=product.id,
                    line_items=[{
                        #'name': product.name,
                        #'description': product.description,
                        #'amount': product.price_cents,
                        #'currency': 'usd',
                        #'images': [product.primary_image_url],
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': product.name,
                                'description': product.description,
                                'images': [product.primary_image_url],
                            },
                            'unit_amount': product.price_cents,
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=success_url,
                    cancel_url=failure_url,
                    )
        return session

    def get_customer(self, customer_id):
        return stripe.Customer.retrieve(customer_id)

    def parse_webhook(self, payload, headers):
        received_sig = headers.get("Stripe-Signature", None)
        # This will raise an exception if it's invalid
        return stripe.Webhook.construct_event(
            payload, received_sig, self.webhook_key
        )