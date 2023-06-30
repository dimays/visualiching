import stripe
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse
from visual_i_ching_app.models import Hexagram, Trigram, HexagramLine, LineType, Reading, UserDetail, UserPayment, CreditBundle, UserCreditHistory
from visual_i_ching_app.forms import ReadingForm, ReadingNotesForm
from visual_i_ching_app.services import AIService, CreditsService
from random import randint


# General Functions
def throw_coins():
    value = randint(2,3) + randint(2,3) + randint(2,3)
    return value

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

def user_has_no_credit_history(request):
    user_id = request.user.id
    user_credit_history_exists = UserCreditHistory.objects.filter(user_id=user_id).exists()
    return not user_credit_history_exists

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

    trigrams = Trigram.objects.all()

    context = {
        "current_credits": current_credits,
        "purchase_btn_text": purchase_btn_text,
        "trigrams": trigrams
    }

    return render(request, 'visual_i_ching_app/about.html', context=context)

# Purchase Credits
@login_required
def redeem_credit_offer(request):
    no_credit_history = user_has_no_credit_history(request)

    if no_credit_history:
        CreditsService.redeem_credit_offer(request.user)
    else:
        messages.warning(request, "You have past credit activity and are not eligible for this credit offer.")

    return redirect('visual-i-ching-app-my-account')


@login_required
def purchase_credits(request):
    user_details = get_user_details(request)
    current_credits = user_details[0]
    purchase_btn_text = user_details[1]
    no_credit_history = user_has_no_credit_history(request)

    hexagrams = Hexagram.objects.all()

    context = {
        "current_credits": current_credits,
        "purchase_btn_text": purchase_btn_text,
        "hexagrams": hexagrams,
        "no_credit_history": no_credit_history
    }

    if settings.WORKING_ENV == 'dev':
        context['price_id_1'] = 'price_1NKpAOCJ0XLbd0Hfp66vUE5U'
        context['price_id_2'] = 'price_1NKpAOCJ0XLbd0Hfp66vUE5U'
        context['price_id_3'] = 'price_1NKpAOCJ0XLbd0Hfp66vUE5U'
        context['price_id_4'] = 'price_1NKpAOCJ0XLbd0Hfp66vUE5U'
        context['price_id_5'] = 'price_1NKpAOCJ0XLbd0Hfp66vUE5U'
    else:
        context['price_id_1'] = 'price_1NNRdOCJ0XLbd0HfW7N4tujj'
        context['price_id_2'] = 'price_1NNRhRCJ0XLbd0Hfm6key1a2'
        context['price_id_3'] = 'price_1NNRlbCJ0XLbd0HfmSonkoTu'
        context['price_id_4'] = 'price_1NNRoLCJ0XLbd0HfOQouXRln'
        context['price_id_5'] = 'price_1NNRshCJ0XLbd0HfVilbcXws'

    return render(request, 'visual_i_ching_app/purchase_credits.html', context=context)

@login_required
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    price_id = request.GET.get('price_id')
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
        line_items=[
                {
                    'price': f'{price_id}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url = settings.REDIRECT_DOMAIN + 'payment_successful/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = settings.REDIRECT_DOMAIN + 'payment_cancelled/',
        )
        return redirect(checkout_session.url, code=303)
    
    context = {
        "price_id": price_id,
        "price_id_1": "price_1NNRdOCJ0XLbd0HfW7N4tujj",
        "price_id_2": "price_1NNRhRCJ0XLbd0Hfm6key1a2",
        "price_id_3": "price_1NNRlbCJ0XLbd0HfmSonkoTu",
        "price_id_4": "price_1NNRoLCJ0XLbd0HfOQouXRln",
        "price_id_5": "price_1NNRshCJ0XLbd0HfVilbcXws"
    }

    return render(request, 'visual_i_ching_app/checkout.html', context=context)

@login_required
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_payment = UserPayment.objects.create(
        user=request.user,
        is_success=True,
        stripe_checkout_id=checkout_session_id
        )
    
    user = request.user
    line_items = stripe.checkout.Session.list_line_items(checkout_session_id, limit=1)
    price_id = line_items['data'][0]['price']['id']

    credit_bundle = CreditBundle.objects.get(stripe_price_id=price_id)

    CreditsService.add_credits(
        user, 
        credit_bundle.num_credits, 
        'Purchase',
        user_payment
    )

    return render(request, 'visual_i_ching_app/payment_successful.html', {'customer': customer})

@login_required
def payment_cancelled(request):
    messages.info(request, "Your payment has been cancelled.")

    return purchase_credits(request)

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']

    if settings.WORKING_ENV == 'dev':
        webhook_secret = settings.STRIPE_LOCAL_LISTENER_SECRET
    else:
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, webhook_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Success!")
    
    return HttpResponse(status=200)


# My Readings (view all, and only, your own readings)
@method_decorator(login_required, name='dispatch')
class ReadingListView(ListView):
    model = Reading
    template_name = 'visual_i_ching_app/my_readings.html'
    context_object_name = 'readings'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.user.id
        queryset = queryset.filter(user_id=user_id)
        return queryset

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
        context['notes_form'] = ReadingNotesForm(initial={'notes': self.object.user_notes})

        return context

# Create New Reading
@method_decorator(login_required, name='dispatch')
class NewReadingView(View):
    template_name = 'visual_i_ching_app/new_reading.html'

    def get(self, request):
        user_details = get_user_details(request)
        current_credits = int(user_details[0].split(" ")[0])
        form = ReadingForm()
        context = {
            'form': form,
            'current_credits': current_credits
        }
        print(current_credits)
        return render(request, self.template_name, context)

    def post(self, request):
        print(f"Request method: {request.method}")
        print(f"Request headers: {request.headers}")
        print(f"Request body: {request.POST}")

        form = ReadingForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            line_values = [
                form.cleaned_data['line_1'],
                form.cleaned_data['line_2'],
                form.cleaned_data['line_3'],
                form.cleaned_data['line_4'],
                form.cleaned_data['line_5'],
                form.cleaned_data['line_6'],
            ]

            if request.POST['line_method'] == 'throw_coins':
                mutable_post = request.POST.copy()
                line_values = [str(throw_coins()) for _ in range(6)]
                for i, line_value in enumerate(line_values):
                    mutable_post[f'line_{i+1}'] = str(line_value)
                form = ReadingForm(mutable_post)

            line_types = []
            for line_value in line_values:
                line_type = LineType.objects.get(line_value=int(line_value))
                line_types.append(line_type)

            starting_binary_str = ""
            resulting_binary_str = ""
            has_no_changing_lines = True

            for line_type in line_types:
                starting_binary_str += str(line_type.binary_value)
                if line_type.is_changing:
                    resulting_binary_str += str(line_type.binary_value ^ 1)
                    has_no_changing_lines = False
                else:
                    resulting_binary_str += str(line_type.binary_value)

            starting_hexagram = Hexagram.objects.get(binary_value_string=starting_binary_str)
            resulting_hexagram = Hexagram.objects.get(binary_value_string=resulting_binary_str)

            if has_no_changing_lines:
                reading = Reading(
                    user=request.user,
                    starting_hexagram=starting_hexagram,
                    value_string=''.join(line_values),
                    prompt=prompt
                )
            else:
                reading = Reading(
                    user=request.user,
                    starting_hexagram=starting_hexagram,
                    resulting_hexagram=resulting_hexagram,
                    value_string=''.join(line_values),
                    prompt=prompt
                )
            reading.save()

            ai_checked = 'ai_assist_checkbox' in request.POST

            if ai_checked:
                ai_interpretation = AIService.generate_interpretation(reading)
                reading.gpt_interpretation = ai_interpretation
                reading.save()
                
                CreditsService.deduct_credit(request.user)
            
            return redirect('visual-i-ching-app-reading', pk=reading.reading_id)


        context = {
            'form': form,
        }
        
        return render(request, self.template_name, context)

# Delete Reading
@login_required
def delete_reading(request, reading_id):
    if request.method == 'POST':
        reading = get_object_or_404(Reading, reading_id=reading_id)

        if request.user.id != reading.user_id:
            raise PermissionDenied

        reading.delete()

        return redirect('visual-i-ching-app-my-readings')
    
    return render(request, 'my_readings.html')
    

# Add AI Interpretation to Reading
@login_required
def update_interpretation(request, reading_id):
    reading = Reading.objects.get(reading_id=reading_id)
    ai_interpretation = AIService.generate_interpretation(reading)
    reading.gpt_interpretation = ai_interpretation
    reading.save()

    CreditsService.deduct_credit(request.user)

    return redirect('visual-i-ching-app-reading', pk=reading.reading_id)

# Edit Notes
@login_required
def update_notes(request, pk):
    reading = get_object_or_404(Reading, reading_id=pk)
    
    if request.method == 'POST':
        form = ReadingNotesForm(request.POST)
        print(f'form.is_valid(): {form.is_valid() == True}')
        if form.is_valid():
            reading.user_notes = form.cleaned_data['notes']
            reading.save()
            return redirect('visual-i-ching-app-reading', pk=pk)
    else:
        form = ReadingNotesForm(initial={'notes': reading.user_notes})

    return render(request, 'update_notes.html', {'form': form, 'reading': reading})

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
    no_credit_history = user_has_no_credit_history(request)

    context = {
        "current_credits": current_credits,
        "purchase_btn_text": purchase_btn_text,
        "total_readings": total_readings,
        "total_ai_interpretations": total_ai_interpretations,
        "no_credit_history": no_credit_history
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