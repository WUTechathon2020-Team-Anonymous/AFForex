from django.contrib import admin
from .models import ForexProvider,Buy_Cash_Low,Buy_Cash_High, Currency_Chart

# Register your models here.
admin.site.register(Currency_Chart)
admin.site.register(ForexProvider)
admin.site.register(Buy_Cash_Low)
admin.site.register(Buy_Cash_High)
