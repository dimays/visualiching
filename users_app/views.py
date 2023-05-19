from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


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
