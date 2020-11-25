from rest_framework import serializers
from .models import ForexProvider,Buy_Cash_High,Buy_Cash_Low

class ForexPrviderSerializer(serializers.ModelSerializer):
	class Meta:
		model = ForexProvider
		fields = ('name',
				'site',
				'usd',
				'eur',
				'gbp',
				'aud',
				'lastupdated'
			)

class BuyCashHighSerializer(serializers.ModelSerializer):
	class meta:
		model = Buy_Cash_High
		fields = (
				'usd',
				'eur',
				'gbp',
				'aud',
				'date'
			)
			
class BuyCashLowSerializer(serializers.ModelSerializer):
	class meta:
		model = Buy_Cash_Low
		fields = (
				'usd',
				'eur',
				'gbp',
				'aud',
				'date'
			)