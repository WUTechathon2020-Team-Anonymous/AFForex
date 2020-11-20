from django.shortcuts import render
from django.utils import timezone
from .models import ForexProvider
from .forex_rates import ForexProviderRates

# Create your views here.
def home(request):
	return render(request, 'ForexProvider/home.html')

def forex(request):
	currency = str(request.POST['target_currency']).lower()
	update_forex_rates()
	providers = ForexProvider.objects.values('name', 'site', currency, 'lastupdated').order_by(currency)
	context = {
		'providers': providers
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

	if len(values)>0:
		values = forex_provider_rates.scrape_thomascook()
		obj = ForexProvider.objects.get(name="ThomasCook")
		obj.usd = values[0]
		obj.eur = values[1]
		obj.gbp = values[2]
		obj.aud = values[3]
		obj.lastupdated = timezone.now()
		obj.save()

	if len(values)>0:
		values = forex_provider_rates.scrape_currencykart()
		obj = ForexProvider.objects.get(name="CurrencyKart")
		obj.usd = values[0]
		obj.eur = values[1]
		obj.gbp = values[2]
		obj.aud = values[3]
		obj.lastupdated = timezone.now()
		obj.save()

	if len(values)>0:
		values = forex_provider_rates.scrape_zenithforex()
		obj = ForexProvider.objects.get(name="Zenith")
		obj.usd = values[0]
		obj.eur = values[1]
		obj.gbp = values[2]
		obj.aud = values[3]
		obj.lastupdated = timezone.now()
		obj.save()

