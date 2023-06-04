from django.contrib import admin

from .models import Trigram, Hexagram, HexagramLine, LineType, Reading

admin.site.register(Trigram)
admin.site.register(Hexagram)
admin.site.register(HexagramLine)
admin.site.register(LineType)
admin.site.register(Reading)
