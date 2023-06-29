from django.contrib import admin
from django.urls import path, include
from users_app import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('visual_i_ching_app.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users_app/logout.html'), name='logout'),
    path('password-reset/', user_views.CustomPasswordResetView.as_view(template_name='users_app/password_reset.html', html_email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users_app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users_app/password_reset_complete.html'), name='password_reset_complete'),
    path('admin/', admin.site.urls),
]

handler404 = "visual_i_ching_app.views.page_not_found_view"
handler403 = "visual_i_ching_app.views.page_forbidden_view"