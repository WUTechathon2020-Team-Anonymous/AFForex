from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from .models import ForexProvider, Buy_Cash_Low,Buy_Cash_High
from .forex_rates import ForexProviderRates, currency_index, output_format
from .serializer import ForexPrviderSerializer,BuyCashHighSerializer,BuyCashLowSerializer

from collections import OrderedDict
import time, threading,sys,json
from datetime import date


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
	providers = ForexProvider.objects.values('name', 'site', currency, 'lastupdated').order_by(currency)
	dbLock = False

	providers_list = []
	for provider in providers:
		provider_dict = OrderedDict()
		provider_dict[provider['name']] = provider['site']
		keys = list(provider.keys())[2:]
		for key in keys:
			provider_dict[key] = provider[key]
		providers_list.append(provider_dict)

	context = {
		'providers': providers_list
	}
	print(context)
	return JsonResponse(context,safe=False)
	# return render(request, 'ForexProvider/forex.html', context)

class UpdateForexRates(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		print("in forex rates")
		print(time.ctime())
		forex_provider_rates = ForexProviderRates()

		min_USD, min_GBP, min_AUD, min_EUR = 100000,100000,100000,100000
		max_USD, max_GBP, max_AUD, max_EUR = -1,-1,-1,-1
		print(min_USD)

		global dbLock

		values = forex_provider_rates.scrape_bookmyforex()
		if len(values)>0:
			while dbLock:
				pass
			dbLock = True
			obj = ForexProvider.objects.get(name="BookMyForex")
			obj.usd = values[0]
			obj.eur = values[1]
			obj.gbp = values[2]
			obj.aud = values[3]
			obj.lastupdated = timezone.now()
			obj.save()
			dbLock = False

			min_USD = min(values[0],min_USD)
			min_EUR = min(values[1],min_EUR)
			min_GBP = min(values[2],min_GBP)
			min_AUD = min(values[3],min_AUD)

			max_USD = max(values[0],max_USD)
			max_EUR = max(values[1],max_EUR)
			max_GBP = max(values[2],max_GBP)
			max_AUD = max(values[3],max_AUD)

			print(min_USD)

		values = forex_provider_rates.scrape_thomascook()
		if len(values)>0:
			while dbLock:
				pass
			dbLock = True
			obj = ForexProvider.objects.get(name="ThomasCook")
			obj.usd = values[0]
			obj.eur = values[1]
			obj.gbp = values[2]
			obj.aud = values[3]
			
			obj.lastupdated = timezone.now()
			obj.save()
			dbLock = False

			min_USD = min(values[0],min_USD)
			min_EUR = min(values[1],min_EUR)
			min_GBP = min(values[2],min_GBP)
			min_AUD = min(values[3],min_AUD)

			max_USD = max(values[0],max_USD)
			max_EUR = max(values[1],max_EUR)
			max_GBP = max(values[2],max_GBP)
			max_AUD = max(values[3],max_AUD)

		values = forex_provider_rates.scrape_currencykart()
		if len(values)>0:
			while dbLock:
				pass
			dbLock = True
			obj = ForexProvider.objects.get(name="CurrencyKart")
			obj.usd = values[0]
			obj.eur = values[1]
			obj.gbp = values[2]
			obj.aud = values[3]		
			obj.lastupdated = timezone.now()
			obj.save()
			dbLock = False

			min_USD = min(values[0],min_USD)
			min_EUR = min(values[1],min_EUR)
			min_GBP = min(values[2],min_GBP)
			min_AUD = min(values[3],min_AUD)

			max_USD = max(values[0],max_USD)
			max_EUR = max(values[1],max_EUR)
			max_GBP = max(values[2],max_GBP)
			max_AUD = max(values[3],max_AUD)

		values = forex_provider_rates.scrape_zenithforex()
		if len(values)>0:
			while dbLock:
				pass
			dbLock = True
			obj = ForexProvider.objects.get(name="Zenith")
			obj.usd = values[0]
			obj.eur = values[1]
			obj.gbp = values[2]
			obj.aud = values[3]
			obj.lastupdated = timezone.now()
			obj.save()
			dbLock = False

			min_USD = min(values[0],min_USD)
			min_EUR = min(values[1],min_EUR)
			min_GBP = min(values[2],min_GBP)
			min_AUD = min(values[3],min_AUD)

			max_USD = max(values[0],max_USD)
			max_EUR = max(values[1],max_EUR)
			max_GBP = max(values[2],max_GBP)
			max_AUD = max(values[3],max_AUD)

		BuyCashLow = Buy_Cash_Low.objects.filter(date = str(date.today()))
		if len(BuyCashLow)>0:
			BuyCashLow = Buy_Cash_Low.objects.get(date = str(date.today()))
			BuyCashLow.usd = min(BuyCashLow.usd,min_USD)
			BuyCashLow.eur = min(BuyCashLow.eur,min_EUR)
			BuyCashLow.gbp = min(BuyCashLow.gbp,min_GBP)
			BuyCashLow.aud = min(BuyCashLow.aud,min_AUD)
			BuyCashLow.save()
		else:
			BuyCashLow = Buy_Cash_Low(usd = min_USD,eur = min_EUR,gbp = min_GBP,aud = min_AUD)
			BuyCashLow.save()
		

		BuyCashHigh = Buy_Cash_High.objects.filter(date = str(date.today()))
		if len(BuyCashHigh)>0:
			BuyCashHigh = Buy_Cash_High.objects.get(date = str(date.today()))
			BuyCashHigh.usd = max(BuyCashHigh.usd,max_USD)
			BuyCashHigh.eur = max(BuyCashHigh.eur,max_EUR)
			BuyCashHigh.gbp = max(BuyCashHigh.gbp,max_GBP)
			BuyCashHigh.aud = max(BuyCashHigh.aud,max_AUD)
			BuyCashHigh.save()
		else:
			BuyCashHigh = Buy_Cash_High(usd = max_USD,eur = max_EUR,gbp = max_GBP,aud = max_AUD )
			BuyCashHigh.save()

		print("\n\nEnd of Run\n\n")

def callback():
	UpdateForexRates().start()
	threading.Timer(300, callback).start()

# callback()
