from django.shortcuts import render

def home(request):
    return render(request, 'visual_i_ching_app/home.html')
