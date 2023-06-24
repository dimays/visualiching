from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from visual_i_ching_app.models import Trigram, Hexagram, HexagramLine, LineType, Reading, UserCreditHistory, UserDetail


# General Functions
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


# Home
def home(request):
    context = {
        "hexagrams": Hexagram.objects.all()
    }

    return render(request, 'visual_i_ching_app/home.html', context=context)

# About
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

# Purchase Credits
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

# Create New Reading


# My Readings (view all, and only, your own readings)
@method_decorator(login_required, name='dispatch')
class ReadingListView(ListView):
    model = Reading
    template_name = 'visual_i_ching_app/my_readings.html'
    context_object_name = 'readings'
    ordering = ['-created_at']


# View Single Reading
@method_decorator(login_required, name='dispatch')
class ReadingDetailView(DetailView):
    model = Reading
    template_name = 'visual_i_ching_app/reading.html'

    def dispatch(self, request, *args, **kwargs):
        reading = self.get_object()
        if request.user.id != reading.user.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reading = self.object
        prefaces = {
            '1': 'Line One',
            '2': 'Line Two',
            '3': 'Line Three',
            '4': 'Line Four',
            '5': 'Line Five',
            '6': 'Live Six'
        }
        user_details = UserDetail.objects.get(user_id=self.request.user.id)

        changing_lines = []
        idx = 0

        for character in reading.value_string:
            idx += 1

            if character in ('6', '9'):
                line_type = get_object_or_404(LineType, line_value=character)
                changing_line = get_object_or_404(HexagramLine, hexagram=reading.starting_hexagram, position=idx)
                changing_lines.append({'line_type': line_type, 'preface': prefaces[f'{idx}'], 'hexagram_line': changing_line})

        if len(changing_lines) == 6:
            context['fc_text'] = reading.starting_hexagram.full_change_text
            context['fc_interpretation'] = reading.starting_hexagram.full_change_interpretation

        context['changing_lines'] = changing_lines
        context['current_credits'] = user_details.current_credits

        return context


# New Reading
@login_required
def new_reading(request):
    return render(request, 'visual_i_ching_app/new_reading.html')


# My Account
@login_required
def count_readings(request):
    current_user_id = request.user.id
    count = Reading.objects.filter(user_id=current_user_id).count()
    return count

@login_required
def count_ai_interpretations(request):
    current_user_id = request.user.id
    count = Reading.objects.filter(user_id=current_user_id).exclude(gpt_interpretation='').count()
    return count

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


# Error Pages
def page_not_found_view(request, exception):
    return render(request, 'visual_i_ching_app/404.html', status=404)

def page_forbidden_view(request, exception):
    return render(request, 'visual_i_ching_app/403.html', status=404)