from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Currency_Chart, Currencies_List, ForexProvider
from .models import Buy_Cash_Low, Buy_Cash_High, Buy_Card_Low, Buy_Card_High
from .models import Sell_Cash_Low, Sell_Cash_High, Sell_Card_Low, Sell_Card_High
from .models import Daily_Currencies_Value

@receiver(pre_save, sender=ForexProvider)
def create_forexprovider(sender, instance, **kwargs):
	if instance.id is None:
		instance.inr = Currency_Chart.objects.create(name=instance.name+'_inr')
		instance.usd = Currency_Chart.objects.create(name=instance.name+'_usd')
		instance.eur = Currency_Chart.objects.create(name=instance.name+'_eur')
		instance.gbp = Currency_Chart.objects.create(name=instance.name+'_gbp')
		instance.aud = Currency_Chart.objects.create(name=instance.name+'_aud')
	else:
		instance.inr.save()
		instance.usd.save()
		instance.eur.save()
		instance.gbp.save()
		instance.aud.save()


@receiver(pre_save, sender=Buy_Cash_Low)
@receiver(pre_save, sender=Buy_Cash_High)
@receiver(pre_save, sender=Buy_Card_Low)
@receiver(pre_save, sender=Buy_Card_High)
@receiver(pre_save, sender=Sell_Cash_Low)
@receiver(pre_save, sender=Sell_Cash_High)
@receiver(pre_save, sender=Sell_Card_Low)
@receiver(pre_save, sender=Sell_Card_High)
@receiver(pre_save, sender=Daily_Currencies_Value)
def create_min_max_tables(sender, instance, **kwargs):
	if instance.id is None:
		instance.currencies = Currencies_List.objects.create()
	else:
		instance.currencies.save()
		

# @receiver(post_save, sender=ForexProvider)
# def save_profile(sender, instance, **kwargs):
# 	print("*****In Save*****")
# 	print("Sender = " + str(sender))
# 	# sender.eur = Currency_Chart.objects.create(name="FromSave")
# 	print("Instance = " + str(instance))
# 	print("Type = " + str(type(instance)))
# 	# instance.eur = Currency_Chart.objects.create(name="insSave")
# 	# instance.usd.save()