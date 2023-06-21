from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from visual_i_ching_app.models import Trigram, Hexagram, HexagramLine, LineType, Reading, UserCreditHistory, UserDetail


def count_readings(request):
    current_user_id = request.user.id
    count = Reading.objects.filter(user_id=current_user_id).count()
    return count

def count_ai_interpretations(request):
    current_user_id = request.user.id
    count = Reading.objects.filter(user_id=current_user_id, gpt_interpretation__isnull=False).count()
    return count

def get_user_details(request):
    current_user_id = request.user.id

    try:
        user_details = UserDetail.objects.get(user_id=current_user_id)
        credit_cnt = user_details.current_credits

        if credit_cnt == 1:
            current_credits = "1 credit"
        else:
            current_credits = f"{credit_cnt} credits"

        if credit_cnt == 0:
            purchase_btn_text = "Buy Credits"
        else:
            purchase_btn_text = "Buy More Credits"

    except UserDetail.DoesNotExist:
        current_credits = "0 credits"
        purchase_btn_text = "Buy Credits"

    return current_credits, purchase_btn_text

def home(request):
    context = {
        "hexagrams": Hexagram.objects.all()
    }

    return render(request, 'visual_i_ching_app/home.html', context=context)

def about(request):
    user_details = get_user_details(request)
    current_credits = user_details[0]
    purchase_btn_text = user_details[1]

    hexagrams = Hexagram.objects.all()

    context = {
        "current_credits": current_credits,
        "purchase_btn_text": purchase_btn_text,
        "hexagrams": hexagrams
    }

    return render(request, 'visual_i_ching_app/about.html', context=context)

@login_required
def purchase_credits(request):
    user_details = get_user_details(request)
    current_credits = user_details[0]
    purchase_btn_text = user_details[1]

    hexagrams = Hexagram.objects.all()

    context = {
        "current_credits": current_credits,
        "purchase_btn_text": purchase_btn_text,
        "hexagrams": hexagrams
    }

    return render(request, 'visual_i_ching_app/purchase_credits.html', context=context)

@login_required
def new_reading(request):
    return render(request, 'visual_i_ching_app/new_reading.html')

@login_required
def my_readings(request):
    readings = Reading.objects.all()
    context = {
        "readings": readings
    }
    return render(request, 'visual_i_ching_app/my_readings.html', context)

def view_reading(request, reading_id):
    reading = get_object_or_404(Reading, reading_id=reading_id)
    if request.user.id != reading.user.id:
        raise PermissionDenied

    context = {
        "reading": reading
    }
    return render(request, 'visual_i_ching_app/reading.html', context=context)

@login_required
def my_account(request):
    user_details = get_user_details(request)
    current_credits = user_details[0]
    purchase_btn_text = user_details[1]
    total_readings = count_readings(request)
    total_ai_interpretations = count_ai_interpretations(request)

    context = {
        "current_credits": current_credits,
        "purchase_btn_text": purchase_btn_text,
        "total_readings": total_readings,
        "total_ai_interpretations": total_ai_interpretations
    }

    return render(request, 'visual_i_ching_app/my_account.html', context=context)

@login_required
def delete_account(request):
    if request.method == 'POST':

        user = request.user
        user.delete()

        logout(request)

        return redirect('visual-i-ching-app-home')

    return render(request, 'my_account.html')


def page_not_found_view(request, exception):
    return render(request, 'visual_i_ching_app/404.html', status=404)


def page_forbidden_view(request, exception):
    return render(request, 'visual_i_ching_app/403.html', status=404)