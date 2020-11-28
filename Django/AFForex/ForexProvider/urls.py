from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('forex/', views.forex, name='forex'),
	path('live_rates/', views.live_rates, name='live_rates'),
	path('chatbot/', views.chatbot, name='chatbot'),
	path('min_max_values/', views.min_max_values, name='min_max_values'),
	path('api/',views.AllCurrencies),
	path('email/', views.email, name='email'),
]
