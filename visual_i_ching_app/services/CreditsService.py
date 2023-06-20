"""This module handles the Credits system, including creating
Stripe Checkout sessions and fulfilling Stripe orders by granting
credits, and inserting & maintaining records in user_details and
user_credit_history."""

import stripe
import os


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')