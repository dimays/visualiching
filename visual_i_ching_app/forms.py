from django import forms
from crispy_forms.helper import FormHelper
from .models import LineType

LINE_TYPE_6 = LineType.objects.get(line_value=6)
LINE_TYPE_7 = LineType.objects.get(line_value=7)
LINE_TYPE_8 = LineType.objects.get(line_value=8)
LINE_TYPE_9 = LineType.objects.get(line_value=9)

SAMPLE_PROMPTS = """I'm experiencing ... but I'm also thinking that ... What guidance do you have for me?"""

LINE_CHOICES = [
    (LINE_TYPE_6.line_value, str(LINE_TYPE_6)),
    (LINE_TYPE_7.line_value, str(LINE_TYPE_7)),
    (LINE_TYPE_8.line_value, str(LINE_TYPE_8)),
    (LINE_TYPE_9.line_value, str(LINE_TYPE_9)),
]

class ReadingForm(forms.Form):
    prompt = forms.CharField(
        label='Prompt', 
        widget=forms.Textarea(attrs={'placeholder':SAMPLE_PROMPTS})
        )
    line_6 = forms.ChoiceField(choices=LINE_CHOICES, label='Line 6')
    line_5 = forms.ChoiceField(choices=LINE_CHOICES, label='Line 5')
    line_4 = forms.ChoiceField(choices=LINE_CHOICES, label='Line 4')
    line_3 = forms.ChoiceField(choices=LINE_CHOICES, label='Line 3')
    line_2 = forms.ChoiceField(choices=LINE_CHOICES, label='Line 2')
    line_1 = forms.ChoiceField(choices=LINE_CHOICES, label='Line 1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['prompt'].label = False

class ReadingNotesForm(forms.Form):
    notes = forms.CharField(label='Notes', widget=forms.Textarea)

class ReadingVisibilityForm(forms.Form):
    is_public = forms.BooleanField(required=False)