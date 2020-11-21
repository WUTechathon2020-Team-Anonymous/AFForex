from django.shortcuts import render
from django.utils import timezone
from .models import ForexProvider
from .forex_rates import ForexProviderRates
from collections import OrderedDict

# Create your views here.
def home(request):
	return render(request, 'ForexProvider/home.html')

def forex(request):
	currency = str(request.POST['target_currency']).lower()
	# update_forex_rates()
	
	providers = ForexProvider.objects.values('name', 'site', currency, 'lastupdated').order_by(currency)
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
	return render(request, 'ForexProvider/forex.html', context)

def update_forex_rates():
	forex_provider_rates = ForexProviderRates()

	values = forex_provider_rates.scrape_bookmyforex()
	if len(values)>0:
		obj = ForexProvider.objects.get(name="BookMyForex")
		obj.usd = values[0]
		obj.eur = values[1]
		obj.gbp = values[2]
		obj.aud = values[3]
		obj.lastupdated = timezone.now()
		obj.save()

	values = forex_provider_rates.scrape_thomascook()
	if len(values)>0:
		obj = ForexProvider.objects.get(name="ThomasCook")
		obj.usd = values[0]
		obj.eur = values[1]
		obj.gbp = values[2]
		obj.aud = values[3]
		obj.lastupdated = timezone.now()
		obj.save()

	values = forex_provider_rates.scrape_currencykart()
	if len(values)>0:
		obj = ForexProvider.objects.get(name="CurrencyKart")
		obj.usd = values[0]
		obj.eur = values[1]
		obj.gbp = values[2]
		obj.aud = values[3]
		obj.lastupdated = timezone.now()
		obj.save()

	values = forex_provider_rates.scrape_zenithforex()
	if len(values)>0:
		obj = ForexProvider.objects.get(name="Zenith")
		obj.usd = values[0]
		obj.eur = values[1]
		obj.gbp = values[2]
		obj.aud = values[3]
		obj.lastupdated = timezone.now()
		obj.save()

