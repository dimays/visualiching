from django.contrib import admin
from .models import Trigram, Hexagram, HexagramLine, LineType, Reading, UserDetail, UserCreditHistory, UserPayment, CreditBundle


admin.site.register(Trigram)
admin.site.register(Hexagram)
admin.site.register(HexagramLine)
admin.site.register(LineType)
admin.site.register(Reading)
admin.site.register(UserDetail)
admin.site.register(UserCreditHistory)
admin.site.register(UserPayment)
admin.site.register(CreditBundle)