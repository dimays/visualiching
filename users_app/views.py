from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from .forms import UserRegisterForm
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You may now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users_app/register.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https'
        context['domain'] = 'www.visualiching.com'
        print(context)
        return context
    
    def form_valid(self, form):
        self.request.session['protocol'] = 'https'
        self.request.session['domain'] = 'www.visualiching.com'
        
        return super().form_valid(form)