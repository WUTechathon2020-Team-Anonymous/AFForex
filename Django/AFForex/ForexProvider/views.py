from django.shortcuts import render
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from django.conf import settings

from .serializer import ForexPrviderSerializer,BuyCashHighSerializer,BuyCashLowSerializer
from django.core import serializers

from collections import OrderedDict
import time, threading, sys, json, os
from datetime import date, timedelta
import numpy as np
import socket, pickle

from .models import ForexProvider
from .forex_rates import ForexProviderRates, currency_index, payment_method_format
from .models import Buy_Cash_Low, Buy_Cash_High, Buy_Card_Low, Buy_Card_High
from .models import Sell_Cash_Low, Sell_Cash_High, Sell_Card_Low, Sell_Card_High
from .models import Daily_Currencies_Value,Subscriber
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
	# # send_mail('Subject here', 'Here is the message.', 'wutechathon2020@gmail.com', ['gautamgodbole99@gmail.com', 'saumitrasapre69@gmail.com'])
	# # currencies_name = list(currency_index.keys())
	# # load_min_max_table(currencies_name)
	# # load_currency_history_table(currencies_name)
	# print("*************")
	return render(request, 'ForexProvider/home.html')

@csrf_exempt
def forex(request):
	print("hello")
	# currency = str(request.POST['target_currency']).lower()
	# update_forex_rates()
	loadedJsonData = json.loads(request.body.decode('utf-8'))
	currency_from = loadedJsonData.get('currency_from')
	currency_to = loadedJsonData.get('currency_to')
	payment_options = list(payment_method_format.keys())

	global dbLock

	while dbLock:
		pass	
	dbLock = True
	# providers = ForexProvider.objects.values('name', 'site', 'lastupdated')
	providers_list = []
	allProviders = ForexProvider.objects.all()
	for provider in allProviders:
		provider_dict = OrderedDict()
		provider_dict['name'] = provider.name
		provider_dict['site'] = provider.site
		provider_dict['lastupdated'] = provider.lastupdated
		input_currencies = [currency_from, currency_to]
		currency_objects = list([getattr(provider, cname) for cname in input_currencies])
		currency_from_values = list([getattr(currency_objects[0], opt) for opt in payment_options])
		currency_to_values = list([getattr(currency_objects[1], opt) for opt in payment_options])
		values = [(from_value / to_value) if from_value != -1 and to_value != -1 else -1 for from_value, to_value in zip(currency_from_values, currency_to_values)]
		length = len(values)
		for i in range(length):
			provider_dict[payment_options[i]] = values[i]
		providers_list.append(provider_dict)
	dbLock = False

	# providers_list = []
	# for provider in providers:
	# 	provider_dict = OrderedDict()
	# 	provider_dict['currency'] = provider[currency]
	# 	keys = list(provider.keys())[1:]
	# 	for key in keys:
	# 		provider_dict[key] = provider[key]
	# 	providers_list.append(provider_dict)


	context = {
		'providers': providers_list
	}
	print(context)
	return JsonResponse(context,safe=False)
	# return render(request, 'ForexProvider/forex.html', context)

@csrf_exempt
def live_rates(request):
	loadedJsonData = json.loads(request.body.decode('utf-8'))
	currency_from = loadedJsonData.get('currency_from')
	currency_to = loadedJsonData.get('currency_to')
	input_currencies = [currency_from, currency_to]
	number_of_days = 7

	if currency_from != '' and currency_to !='':
		values = []
		dates = []

		global dbLock

		while dbLock:
			pass

		dbLock = True
		for i in range(number_of_days):
			try:
				obj = Daily_Currencies_Value.objects.get(date=date.today() - timedelta(days=i))
				dates.insert(0, str(obj.date))
				from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
				values.insert(0, (from_value / to_value))
			except Exception:
				pass
		dbLock = False

		predicted_values, future_dates = predict(currency_from, currency_to)
		values.extend(predicted_values)
		dates.extend(future_dates)

		context = {
			'currency_value': values,
			'dates': dates
		}
	else:
		context = {
			'currency_value': [],
			'dates': []
		}
	return JsonResponse(context, safe=False)
	# return render(request, 'ForexProvider/live_rates.html', {'value': value})

def predict(from_currency, to_currency):
	# loadedJsonData = json.loads(request.body.decode('utf-8'))
	currency_from = from_currency #loadedJsonData.get('currency_from')
	currency_to = to_currency #loadedJsonData.get('currency_to')
	number_of_days_to_predict = 5#loadedJsonData.get('days')
	
	prediction_model_ip = '192.168.1.11'
	prediction_model_port = 4444
	prediction_socket = socket.socket()
	input_currencies = list([currency_from, currency_to])
	number_of_days = 7
	values = []
	dates = []

	for i in range(number_of_days_to_predict):
		dates.append(date.today() + timedelta(days=(1+i)))

	global dbLock

	while dbLock:
		pass
	dbLock = True
	for i in range(number_of_days):
		try:
			obj = Daily_Currencies_Value.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			values.insert(0, (from_value / to_value))
		except Exception:
			pass
	dbLock = False
	values.append(number_of_days_to_predict)
	values.insert(0, currency_to)
	values.insert(0, currency_from)

	prediction_socket.connect((prediction_model_ip, prediction_model_port))
	prediction_socket.send(pickle.dumps(values))
	predicted_values = pickle.loads(prediction_socket.recv(1024))
	prediction_socket.close()

	return [predicted_values, dates]

@csrf_exempt
def email(request):
	loadedJsonData = json.loads(request.body.decode('utf-8'))
	subscriber_email = loadedJsonData.get('email')
	global dbLock
	while dbLock:
		pass
	dbLock = True
	obj = Subscriber.objects.create(email = subscriber_email)
	dbLock = False




@csrf_exempt
def chatbot(request):
	loadedJsonData = json.loads(request.body.decode('utf-8'))
	message = loadedJsonData.get('msg')
	# message = str(request.POST['msg'])
	print(message)
	paramsPresent, amount, curr_from, curr_to, fulfillment_text,action = chat(message)
	if paramsPresent == "True" and action!="input.welcome":
		obj = Daily_Currencies_Value.objects.get(date=date.today())
		input_currencies = [curr_from.lower(), curr_to.lower()]
		from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies ]
		rate = from_value/to_value
		total_value = float(amount) * rate
		predicted_values = predict(curr_from.lower(),curr_to.lower())
		fulfillment_text += "\n The exchange rate is {0}. \n The converted value is {1}.\n The predicted values for the next 5 days are:\n {2}".format(rate,total_value,str(predicted_values))
	context = {'response': fulfillment_text}
	return JsonResponse(context, safe=False)

@csrf_exempt
def min_max_values(request):
	loadedJsonData = json.loads(request.body.decode('utf-8'))
	currency_from = loadedJsonData.get('currency_from')
	currency_to = loadedJsonData.get('currency_to')
	input_currencies = [currency_from, currency_to]
	payment_options = list(payment_method_format.keys())
	types = ['min', 'max']
	payment_options_length = len(payment_options)
	types_length = len(types)

	number_of_days = 7
	categories = payment_options_length * types_length
	labels = []
	dates = []
	history = np.zeros([categories, number_of_days])

	global dbLock

	for i in range(payment_options_length):
		for j in range(types_length):
			labels.append(payment_options[i] + '_' + types[j])

	for i in range(number_of_days):
		dates.insert(0, str(date.today() - timedelta(days=i)))

	while dbLock:
		pass

	dbLock = True
	for i in range(number_of_days):
		try:
			obj = Buy_Cash_Low.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			history[0][number_of_days-1-i] = (from_value/to_value)

			obj = Buy_Cash_High.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			history[1][number_of_days-1-i] = (from_value/to_value)

			obj = Buy_Card_Low.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			history[2][number_of_days-1-i] = (from_value/to_value)

			obj = Buy_Card_High.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			history[3][number_of_days-1-i] = (from_value/to_value)

			obj = Sell_Cash_Low.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			history[4][number_of_days-1-i] = (from_value/to_value)

			obj = Sell_Cash_High.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			history[5][number_of_days-1-i] = (from_value/to_value)

			obj = Sell_Card_Low.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			history[6][number_of_days-1-i] = (from_value/to_value)

			obj = Sell_Card_High.objects.get(date=date.today() - timedelta(days=i))
			from_value, to_value = [getattr(obj.currencies, cname) for cname in input_currencies]
			history[7][number_of_days-1-i] = (from_value/to_value)

		except Exception:
			pass

	for i in range(0, categories, 2):
		for j in range(number_of_days):
			if history[i][j] > history[i+1][j]:
				history[i][j], history[i+1][j] = history[i+1][j], history[i]


	dbLock = False

	context = {}
	for i in range(categories):
		context[labels[i]] = list(history[i])
	context['dates'] = dates
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
		# forex_provider_rates = ForexProviderRates()

		# values = forex_provider_rates.scrape_bookmyforex()
		# if len(values)>0:
		# 	while dbLock:
		# 		pass
		# 	dbLock = True
		# 	obj = ForexProvider.objects.get(name="BookMyForex")
		# 	set_values_for_forex_provider(obj, values)
		# 	obj.lastupdated = timezone.now()
		# 	obj.save()
		# 	dbLock = False
		# 	compute_min_max_table(self.number_of_currencies, self.payment_options, values, self.min_max_table)

		# values = forex_provider_rates.scrape_thomascook()
		# if len(values)>0:
		# 	while dbLock:
		# 		pass
		# 	dbLock = True
		# 	obj = ForexProvider.objects.get(name="ThomasCook")
		# 	set_values_for_forex_provider(obj, values)
		# 	obj.lastupdated = timezone.now()
		# 	obj.save()
		# 	dbLock = False
		# 	compute_min_max_table(self.number_of_currencies, self.payment_options, values, self.min_max_table)
			

		# values = forex_provider_rates.scrape_currencykart()
		# if len(values)>0:
		# 	while dbLock:
		# 		pass
		# 	dbLock = True
		# 	obj = ForexProvider.objects.get(name="CurrencyKart")
		# 	set_values_for_forex_provider(obj, values)
		# 	obj.lastupdated = timezone.now()
		# 	obj.save()
		# 	dbLock = False
		# 	compute_min_max_table(self.number_of_currencies, self.payment_options, values, self.min_max_table)


		# values = forex_provider_rates.scrape_zenithforex()
		# if len(values)>0:
		# 	while dbLock:
		# 		pass
		# 	dbLock = True
		# 	obj = ForexProvider.objects.get(name="Zenith")
		# 	set_values_for_forex_provider(obj, values)
		# 	obj.lastupdated = timezone.now()
		# 	obj.save()
		# 	dbLock = False
		# 	compute_min_max_table(self.number_of_currencies, self.payment_options, values, self.min_max_table)


		# set_values_for_min_max_tables(self.min_value, self.max_value, self.min_max_table)
		# update_currency_exchange_values()
		# send_mail_to_subscriber()
		print(predict('usd','inr'))
		print("\n\nEnd of Run\n\n")


def send_mail_to_subscriber():
	global dbLock
	while dbLock:
		pass
	dbLock = True
	objects_list = Subscriber.objects.all()
	emails = []
	for object in objects_list:
		emails.append(str(object.email))
	currencies_name = list(currency_index.keys())
	currencies_name_length = len(currencies_name)
	payment_options = list(payment_method_format.keys())
	types = ['min', 'max']
	payment_options_length = len(payment_options)
	types_length = len(types)
	categories = payment_options_length * types_length
	history = np.zeros([currencies_name_length, categories])

	header = []
	for i in range(payment_options_length):
		for j in range(types_length):
			header.append(payment_options[i] + '_' + types[j])
	header.insert(0, "Currency")
	obj = Buy_Cash_Low.objects.get(date=date.today())
	history[:, 0] = [getattr(obj.currencies, cname) for cname in currencies_name]

	obj = Buy_Cash_High.objects.get(date=date.today())
	history[:, 1] = [getattr(obj.currencies, cname) for cname in currencies_name]

	obj = Buy_Card_Low.objects.get(date=date.today())
	history[:, 2] = [getattr(obj.currencies, cname) for cname in currencies_name]

	obj = Buy_Card_High.objects.get(date=date.today())
	history[:, 3] = [getattr(obj.currencies, cname) for cname in currencies_name]

	obj = Sell_Cash_Low.objects.get(date=date.today())
	history[:, 4] = [getattr(obj.currencies, cname) for cname in currencies_name]

	obj = Sell_Cash_High.objects.get(date=date.today())
	history[:, 5] = [getattr(obj.currencies, cname) for cname in currencies_name]

	obj = Sell_Card_Low.objects.get(date=date.today())
	history[:, 6] = [getattr(obj.currencies, cname) for cname in currencies_name]

	obj = Sell_Card_High.objects.get(date=date.today())
	history[:, 7] = [getattr(obj.currencies, cname) for cname in currencies_name]
	dbLock = False
	with open(os.path.join(settings.BASE_DIR, 'Resources/day_'+ str(date.today()) +'.csv'), 'w') as csvfile:
		for i in range(currencies_name_length):
			if i == 0:
				for val in header:
					csvfile.write(val + ",")
				csvfile.write("\n")
				csvfile.flush()
			temp = list(history[i])
			temp.insert(0, currencies_name[i])
			for j in range(categories+1):
				csvfile.write(str(temp[j]) + ",")
			csvfile.write("\n")
			csvfile.flush()

	email = EmailMessage(
        str(date.today()) + ' Forex Sheet',
        'Dear Subscriber,\n\nFind today\'s Forex Sheet here\n\n*All The Rates are relative to INR',
        'wutechathon2020@gmail.com',
        emails,
    )
	email.attach_file(os.path.join(settings.BASE_DIR, 'Resources/day_'+ str(date.today()) +'.csv'))
	email.send()

def update_currency_exchange_values():
	currencies_name = list(currency_index.keys())
	base_currency = 'inr'

	live_rate = LiveRates()
	values = [1]
	for currency in currencies_name[1:]:
		values.append(live_rate.get_live_rates(currency, base_currency))

	obj, created = Daily_Currencies_Value.objects.get_or_create(date=date.today())
	for key, value in zip(currencies_name, values):
		setattr(obj.currencies, key, value)
	obj.save()


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

callback()
