"""This module handles the Credits system, including granting
and deducting credits, which modifies records in user_details
and user_credit_history."""

from visual_i_ching_app.models import UserCreditHistory, UserDetail

def add_credits(user, num_credits, event_type, user_payment=None):
    user_details = UserDetail.objects.get(user_id=user.id)
    current_credits = user_details.current_credits

    user_details.current_credits = current_credits + num_credits
    user_details.save()

    UserCreditHistory.objects.create(
        user=user,
        history_type=event_type,
        credits_amount=num_credits,
        user_payment=user_payment
    )

    return

def deduct_credit(user):
    add_credits(user, -1, 'Redemption')

    return

def redeem_credit_offer(user):
    add_credits(user, 1, 'Credit Offer')