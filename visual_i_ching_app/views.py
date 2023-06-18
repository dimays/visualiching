from django.shortcuts import render
from visual_i_ching_app.models import Trigram, Hexagram, HexagramLine, LineType, Reading

def home(request):
    context = {
        "hexagrams": Hexagram.objects.all()
    }

    return render(request, 'visual_i_ching_app/home.html', context=context)

def about(request):
    context = {
        "hexagrams": Hexagram.objects.all()
    }

    return render(request, 'visual_i_ching_app/about.html', context=context)