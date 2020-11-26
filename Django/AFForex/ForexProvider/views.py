from django.shortcuts import render
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from .serializer import ForexPrviderSerializer,BuyCashHighSerializer,BuyCashLowSerializer

from collections import OrderedDict
import time, threading, sys, json
from datetime import date
import numpy as np

from .models import ForexProvider
from .forex_rates import ForexProviderRates, currency_index, payment_method_format
from .models import Buy_Cash_Low, Buy_Cash_High, Buy_Card_Low, Buy_Card_High
from .models import Sell_Cash_Low, Sell_Cash_High, Sell_Card_Low, Sell_Card_High
from .live_rates import LiveRates
from .chatbot_python_client import chat
from .load_database import load_min_max_table, load_currency_history_table


dbLock = False

# Create your views here.
@csrf_exempt
def AllCurrencies(request):
	if request.method == 'GET':
		providers = ForexProvider.objects.all()
		forex_provider_serializer = ForexPrviderSerializer(providers,many = True)
		return JsonResponse(forex_provider_serializer.data, safe = False)
	elif request.method == 'POST':
		provider_data = JSONParser().parse(request)
		forex_provider_serializer = ForexPrviderSerializer(data = provider_data)
		if forex_provider_serializer.is_valid():
			forex_provider_serializer.save()
			return JsonResponse("Added!!",safe = False)
		else:
			return JsonResponse("Failed!",safe = False)
	elif request.method == 'PUT':
		provider_data = JSONParser().parse(request)
		Forex_Provider = ForexProvider.objects.get(name = provider_data['name'])
		forex_provider_serializer = ForexPrviderSerializer(Forex_Provider,data = provider_data)
		if forex_provider_serializer.is_valid():
			forex_provider_serializer.save()
			return JsonResponse("Added PUT!!",safe = False)
		else:
			return JsonResponse("Failed PUT!!",safe = False)


def home(request):
	# print("*************")
	# currencies_name = list(currency_index.keys())
	# load_min_max_table(currencies_name)
	# load_currency_history_table(currencies_name)
	# print("*************")
	return render(request, 'ForexProvider/home.html')

@csrf_exempt
def forex(request):
	print("hello")
	# currency = str(request.POST['target_currency']).lower()
	# update_forex_rates()
	loadedJsonData = json.loads(request.body.decode('utf-8'))
	currency = loadedJsonData.get('target_currency')

	global dbLock

	while dbLock:
		pass	
	dbLock = True
	providers = ForexProvider.objects.values(currency, 'name', 'site', 'lastupdated')
	dbLock = False

	providers_list = []
	for provider in providers:
		provider_dict = OrderedDict()
		provider_dict['currency'] = provider[currency]
		keys = list(provider.keys())[1:]
		for key in keys:
			provider_dict[key] = provider[key]
		providers_list.append(provider_dict)


	context = {
		'providers': providers_list
	}
	print(context)
	return JsonResponse(context,safe=False)
	# return render(request, 'ForexProvider/forex.html', context)

def live_rates(request):
	currency_from = str(request.POST['currency_from']).lower()
	currency_to = str(request.POST['currency_to']).lower()

	live_rate = LiveRates()
	value = live_rate.get_live_rates(currency_from, currency_to)
	return render(request, 'ForexProvider/live_rates.html', {'value': value})

@csrf_exempt
def chatbot(request):
	message = str(request.POST['msg'])
	print(message)
	paramsPresent, amount, curr_from, curr_to, fulfillment_text,action = chat(message)
	context = {'response': fulfillment_text}
	return JsonResponse(context, safe=False)





class UpdateForexRates(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.number_of_currencies = len(currency_index)
		self.payment_options = len(payment_method_format)
		self.min_value, self.max_value = -1.0, 100000.0
		self.types = 2
		self.min_max_table = np.array([[self.max_value, self.min_value] * self.payment_options] * self.number_of_currencies)

	def run(self):
		print("in forex rates")
		print(time.ctime())

		global dbLock
		forex_provider_rates = ForexProviderRates()

		values = forex_provider_rates.scrape_bookmyforex()
		if len(values)>0:
			while dbLock:
				pass
			dbLock = True
			obj = ForexProvider.objects.get(name="BookMyForex")
			set_values_for_forex_provider(obj, values)
			obj.lastupdated = timezone.now()
			obj.save()
			dbLock = False
			compute_min_max_table(self.number_of_currencies, self.payment_options, values, self.min_max_table)

		values = forex_provider_rates.scrape_thomascook()
		if len(values)>0:
			while dbLock:
				pass
			dbLock = True
			obj = ForexProvider.objects.get(name="ThomasCook")
			set_values_for_forex_provider(obj, values)
			obj.lastupdated = timezone.now()
			obj.save()
			dbLock = False
			compute_min_max_table(self.number_of_currencies, self.payment_options, values, self.min_max_table)
			

		values = forex_provider_rates.scrape_currencykart()
		if len(values)>0:
			while dbLock:
				pass
			dbLock = True
			obj = ForexProvider.objects.get(name="CurrencyKart")
			set_values_for_forex_provider(obj, values)
			obj.lastupdated = timezone.now()
			obj.save()
			dbLock = False
			compute_min_max_table(self.number_of_currencies, self.payment_options, values, self.min_max_table)


		values = forex_provider_rates.scrape_zenithforex()
		if len(values)>0:
			while dbLock:
				pass
			dbLock = True
			obj = ForexProvider.objects.get(name="Zenith")
			set_values_for_forex_provider(obj, values)
			obj.lastupdated = timezone.now()
			obj.save()
			dbLock = False
			compute_min_max_table(self.number_of_currencies, self.payment_options, values, self.min_max_table)


		set_values_for_min_max_tables(self.min_value, self.max_value, self.min_max_table)

		print("\n\nEnd of Run\n\n")



def set_values_for_forex_provider(provider, values):
	currency_chart_fields = list(payment_method_format.keys())
	currency_chart_number_of_fields = len(currency_chart_fields)

	currency_values = values[currency_index['inr']]
	for key, value in zip(currency_chart_fields, currency_values):
		setattr(provider.inr, key, value)

	currency_values = values[currency_index['usd']]
	for key, value in zip(currency_chart_fields, currency_values):
		setattr(provider.usd, key, value)

	currency_values = values[currency_index['eur']]
	for key, value in zip(currency_chart_fields, currency_values):
		setattr(provider.eur, key, value)

	currency_values = values[currency_index['gbp']]
	for key, value in zip(currency_chart_fields, currency_values):
		setattr(provider.gbp, key, value)

	currency_values = values[currency_index['aud']]
	for key, value in zip(currency_chart_fields, currency_values):
		setattr(provider.aud, key, value)


def compute_min_max_table(rows, columns, values, table):
	print(values)
	print("-------")
	print(table)
	for i in range(rows):
		for j in range(columns):
			if values[i][j] != -1:
				if values[i][j] < table[i][j*2]:
					table[i][j*2] = values[i][j]
				if values[i][j] > table[i][(j*2) + 1]:
					table[i][(j*2) + 1] = values[i][j]


def set_values_for_min_max_tables(min_value, max_value, table):
	currencies_name = list(currency_index.keys())

	BuyCashLow, created = Buy_Cash_Low.objects.get_or_create(date=date.today())
	set_values_for_subtable(BuyCashLow, currencies_name, max_value, table[:, 0], -1)
	BuyCashLow.save()

	BuyCashHigh, created = Buy_Cash_High.objects.get_or_create(date=date.today())
	set_values_for_subtable(BuyCashHigh, currencies_name, min_value, table[:, 1], 1)
	BuyCashHigh.save()

	BuyCardLow, created = Buy_Card_Low.objects.get_or_create(date=date.today())
	set_values_for_subtable(BuyCardLow, currencies_name, max_value, table[:, 2], -1)
	BuyCardLow.save()

	BuyCardHigh, created = Buy_Card_High.objects.get_or_create(date=date.today())
	set_values_for_subtable(BuyCardHigh, currencies_name, min_value, table[:, 3], 1)
	BuyCardHigh.save()

	SellCashLow, created = Sell_Cash_Low.objects.get_or_create(date=date.today())
	set_values_for_subtable(SellCashLow, currencies_name, max_value, table[:, 4], -1)
	SellCashLow.save()

	SellCashHigh, created = Sell_Cash_High.objects.get_or_create(date=date.today())
	set_values_for_subtable(SellCashHigh, currencies_name, min_value, table[:, 5], 1)
	SellCashHigh.save()

	SellCardLow, created = Sell_Card_Low.objects.get_or_create(date=date.today())
	set_values_for_subtable(SellCardLow, currencies_name, max_value, table[:, 6], -1)
	SellCardLow.save()

	SellCardHigh, created = Sell_Card_High.objects.get_or_create(date=date.today())
	set_values_for_subtable(SellCardHigh, currencies_name, min_value, table[:, 7], 1)
	SellCardHigh.save()


def set_values_for_subtable(object_name, currencies_name, alternate_value, given_nparray, operator):
	print(object_name, currencies_name, alternate_value, given_nparray, operator)
	current_values = np.array([getattr(object_name.currencies, cname) for cname in currencies_name])
	current_values[current_values == -1] = alternate_value
	if operator == 1:
		compared_list = list([max(val1, val2) for val1, val2 in zip(given_nparray, current_values)])
	else:
		compared_list = list([min(val1, val2) for val1, val2 in zip(given_nparray, current_values)])
	for key, value in zip(currencies_name, compared_list):
		setattr(object_name.currencies, key, value)











def callback():
	while True:
		updaterates_object = UpdateForexRates()
		updaterates_object.start()
		if updaterates_object.is_alive():
			break
	threading.Timer(600, callback).start()

# callback()
