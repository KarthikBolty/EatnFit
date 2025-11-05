

# Register your models here.
from django.contrib import admin
from .models import Meal, QuickFood, BodyWeightEntry

admin.site.register(Meal)
admin.site.register(QuickFood)
admin.site.register(BodyWeightEntry)
