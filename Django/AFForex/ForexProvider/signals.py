from django.db.models.signals import post_save, pre_save
# from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Currency_Chart, ForexProvider

@receiver(pre_save, sender=ForexProvider)
def create_profile(sender, instance, **kwargs):
	if instance.id is None:
		instance.usd = Currency_Chart.objects.create(name=instance.name+'_usd')
		instance.eur = Currency_Chart.objects.create(name=instance.name+'_eur')
		instance.gbp = Currency_Chart.objects.create(name=instance.name+'_gbp')
		instance.aud = Currency_Chart.objects.create(name=instance.name+'_aud')

# @receiver(post_save, sender=ForexProvider)
# def save_profile(sender, instance, **kwargs):
# 	print("*****In Save*****")
# 	print("Sender = " + str(sender))
# 	# sender.eur = Currency_Chart.objects.create(name="FromSave")
# 	print("Instance = " + str(instance))
# 	print("Type = " + str(type(instance)))
# 	# instance.eur = Currency_Chart.objects.create(name="insSave")
# 	# instance.usd.save()