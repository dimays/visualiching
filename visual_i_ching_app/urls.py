from django.urls import path
from .views import ReadingListView, ReadingDetailView
from . import views


urlpatterns = [
    path('', views.home, name='visual-i-ching-app-home'),
    path('about/', views.about, name='visual-i-ching-app-about'),
    path('my_account/', views.my_account, name='visual-i-ching-app-my-account'),
    path('my_readings/', ReadingListView.as_view(), name='visual-i-ching-app-my-readings'),
    path('new_reading/', views.new_reading, name='visual-i-ching-app-new-reading'),
    path('reading/<int:pk>/', ReadingDetailView.as_view(), name='view_reading'),
    path('purchase_credits/', views.purchase_credits, name='visual-i-ching-app-purchase-credits'),
    path('delete_account', views.delete_account, name='visual-i-ching-app-delete-account'),
]
