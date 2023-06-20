"""This module handles the Credits system, including creating
Stripe Checkout sessions and fulfilling Stripe orders by granting
credits, and inserting & maintaining records in user_details and
user_credit_history."""

import stripe
import os


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)