from django.urls import path
from .views import ReadingListView, ReadingDetailView, NewReadingView
from . import views


urlpatterns = [
    path('', views.home, name='visual-i-ching-app-home'),
    path('about/', views.about, name='visual-i-ching-app-about'),
    path('my_account/', views.my_account, name='visual-i-ching-app-my-account'),
    path('my_readings/', ReadingListView.as_view(), name='visual-i-ching-app-my-readings'),
    path('new_reading/', NewReadingView.as_view(), name='visual-i-ching-app-new-reading'),
    path('reading/<int:pk>/', ReadingDetailView.as_view(), name='visual-i-ching-app-reading'),
    path('delete_reading/<int:reading_id>/', views.delete_reading, name='visual-i-ching-app-delete-reading'),
    path('delete_account', views.delete_account, name='visual-i-ching-app-delete-account'),
    path('reading/<int:pk>/edit_notes/', views.update_notes, name='visual-i-ching-app-edit-notes'),
    path('reading/<int:reading_id>/update_interpretation/', views.update_interpretation, name='visual-i-ching-app-update-interpretation'),
    path('redeem_credit_offer/', views.redeem_credit_offer, name='visual-i-ching-app-redeem-credit-offer'),
    path('purchase_credits/', views.purchase_credits, name='visual-i-ching-app-purchase-credits'),
    path('checkout/', views.checkout, name='visual-i-ching-app-product-checkout'),
    path('payment_successful/', views.payment_successful, name='visual-i-ching-app-payment-successful'),
    path('payment_cancelled/', views.payment_cancelled, name='visual-i-ching-app-payment-cancelled'),
    path('stripe_webhook/', views.stripe_webhook, name='visual-i-ching-app-stripe-webhook'),
]
