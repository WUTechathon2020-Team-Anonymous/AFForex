from django.apps import AppConfig


class ForexproviderConfig(AppConfig):
    name = 'ForexProvider'

    def ready(self):
    	import ForexProvider.signals