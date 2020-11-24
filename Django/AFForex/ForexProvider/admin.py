from django.contrib import admin
from .models import ForexProvider, Currency_Chart, Currencies_List
from .models import Buy_Cash_Low, Buy_Cash_High, Buy_Card_Low, Buy_Card_High
from .models import Sell_Cash_Low, Sell_Cash_High, Sell_Card_Low, Sell_Card_High

# Register your models here.
admin.site.register(Currencies_List)
admin.site.register(Currency_Chart)
admin.site.register(ForexProvider)

admin.site.register(Buy_Cash_Low)
admin.site.register(Buy_Cash_High)
admin.site.register(Buy_Card_Low)
admin.site.register(Buy_Card_High)
admin.site.register(Sell_Cash_Low)
admin.site.register(Sell_Cash_High)
admin.site.register(Sell_Card_Low)
admin.site.register(Sell_Card_High)
