from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('forex/', views.forex, name='forex'),
	path('live_rates/', views.live_rates, name='live_rates'),
]