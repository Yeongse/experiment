from django.contrib import admin
from .models import Subject, Choice, Player, Weight, Preference

# Register your models here.

admin.site.register(Subject)
admin.site.register(Choice)
admin.site.register(Player)
admin.site.register(Weight)
admin.site.register(Preference)