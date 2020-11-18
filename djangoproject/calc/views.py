from django.shortcuts import render
from django.http import HttpResponse
from .models import Cur
from django.utils import timezone
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.support.ui import Select


# Create your views here.

def home(request):
	return render(request,'home.html',{'test':'check'})

def conv(request):
	# val1 = request.POST['base_currency']	
	val2 = request.POST['target_currency']

	cur = Cur.objects.values()
	cur.query = pickle.loads(pickle.dumps(cur.query))

	#updateData()
	# currency_detail1 = Cur.objects.get(currency_name = val1)
	currency_detail2 = Cur.objects.get(currency_name = val2)

	# rate = currency_detail2.rate1/currency_detail1.rate1
	rate = currency_detail2.rate1
	return render(request,'convert.html',{'tcurr':val2 ,'cur':currency_detail2, 'rate':rate})

def updateData():
	# var1 = scrapedatabmf()
	# print("len in conv fun")
	# print(len(var1))

	# var4 = scrapedatazenth()
	# print(len(var4))

	# var3 = scrapedatacrcykrt()
	# print(len(var3))

	var2 = scrapedatatmsck()
	print(var2)
	count = 0
	for v in var2:
		print(count)
		print(v)
		print("--------")
		count += 1
	# count = 0

	# if len(var1)>0:
	# 	USD_rate_bmf = var1[0].split(" ")
	# 	currency_detail_USD = Cur.objects.get(currency_name = 'USD')
	# 	currency_detail_USD.rate1 = USD_rate_bmf[4]
	# 	currency_detail_USD.lastupdated = timezone.now()
	# 	currency_detail_USD.save()

	# 	EUR_rate_bmf = var1[1].split(" ")
	# 	currency_detail_EUR = Cur.objects.get(currency_name = 'EUR')
	# 	currency_detail_EUR.rate1 = EUR_rate_bmf[4]
	# 	currency_detail_EUR.lastupdated = timezone.now()
	# 	currency_detail_EUR.save()

	# 	GBP_rate_bmf = var1[2].split(" ")
	# 	currency_detail_GBP = Cur.objects.get(currency_name = 'GBP')
	# 	currency_detail_GBP.rate1 = GBP_rate_bmf[4]
	# 	currency_detail_GBP.lastupdated = timezone.now()
	# 	currency_detail_GBP.save()

	# 	AUD_rate_bmf = var1[3].split(" ")
	# 	currency_detail_AUD = Cur.objects.get(currency_name = 'AUD')
	# 	currency_detail_AUD.rate1 = AUD_rate_bmf[4]
	# 	currency_detail_AUD.lastupdated = timezone.now()
	# 	currency_detail_AUD.save()

	if len(var2)>0:
		currency_detail_USD = Cur.objects.get(currency_name = 'USD')
		currency_detail_USD.rate2 = var2[2]
		currency_detail_USD.lastupdated = timezone.now()
		currency_detail_USD.save()

		currency_detail_EUR = Cur.objects.get(currency_name = 'EUR')
		currency_detail_EUR.rate2 = var2[7]
		currency_detail_EUR.lastupdated = timezone.now()
		currency_detail_EUR.save()

		currency_detail_GBP = Cur.objects.get(currency_name = 'GBP')
		currency_detail_GBP.rate2 = var2[12]
		currency_detail_GBP.lastupdated = timezone.now()
		currency_detail_GBP.save()

		currency_detail_AUD = Cur.objects.get(currency_name = 'AUD')
		currency_detail_AUD.rate2 = var2[47]
		currency_detail_AUD.lastupdated = timezone.now()
		currency_detail_AUD.save()

	# if len(var3)>0:
	# 	USD_rate_bmf = var3[3].split(" ")
	# 	currency_detail_USD = Cur.objects.get(currency_name = 'USD')
	# 	currency_detail_USD.rate3 = USD_rate_bmf[3]
	# 	currency_detail_USD.lastupdated = timezone.now()
	# 	currency_detail_USD.save()

	# 	EUR_rate_bmf = var3[4].split(" ")
	# 	currency_detail_EUR = Cur.objects.get(currency_name = 'EUR')
	# 	currency_detail_EUR.rate3 = EUR_rate_bmf[3]
	# 	currency_detail_EUR.lastupdated = timezone.now()
	# 	currency_detail_EUR.save()

	# 	GBP_rate_bmf = var3[5].split(" ")
	# 	currency_detail_GBP = Cur.objects.get(currency_name = 'GBP')
	# 	currency_detail_GBP.rate3 = GBP_rate_bmf[3]
	# 	currency_detail_GBP.lastupdated = timezone.now()
	# 	currency_detail_GBP.save()

	# 	AUD_rate_bmf = var3[7].split(" ")
	# 	currency_detail_AUD = Cur.objects.get(currency_name = 'AUD')
	# 	currency_detail_AUD.rate3 = AUD_rate_bmf[3]
	# 	currency_detail_AUD.lastupdated = timezone.now()
	# 	currency_detail_AUD.save()

	# if len(var4)>0:
	# 	USD_rate_bmf = var4[0].split(" ")
	# 	currency_detail_USD = Cur.objects.get(currency_name = 'USD')
	# 	currency_detail_USD.rate4 = USD_rate_bmf[4]
	# 	currency_detail_USD.lastupdated = timezone.now()
	# 	currency_detail_USD.save()

	# 	EUR_rate_bmf = var4[1].split(" ")
	# 	currency_detail_EUR = Cur.objects.get(currency_name = 'EUR')
	# 	currency_detail_EUR.rate4 = EUR_rate_bmf[4]
	# 	currency_detail_EUR.lastupdated = timezone.now()
	# 	currency_detail_EUR.save()

	# 	GBP_rate_bmf = var4[2].split(" ")
	# 	currency_detail_GBP = Cur.objects.get(currency_name = 'GBP')
	# 	currency_detail_GBP.rate4 = GBP_rate_bmf[4]
	# 	currency_detail_GBP.lastupdated = timezone.now()
	# 	currency_detail_GBP.save()

	# 	AUD_rate_bmf = var4[4].split(" ")
	# 	currency_detail_AUD = Cur.objects.get(currency_name = 'AUD')
	# 	currency_detail_AUD.rate4 = AUD_rate_bmf[4]
	# 	currency_detail_AUD.lastupdated = timezone.now()
	# 	currency_detail_AUD.save()


def scrapedatabmf():
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
	url_text = "https://www.bookmyforex.com/"
	driver.get(url_text)
	driver.find_element_by_class_name("see_frc_btn").click()
	time.sleep(3)
	mytext = str(driver.find_element_by_class_name("fullratetable.table-responsive").text)
	mytext = mytext[203:]
	mylist = mytext.splitlines()
	del mylist[14:]
	mynewlist = []
	for ele in mylist:
		s1 = re.sub(r"(?!(?<=\d)\.(?=\d))[^0-9 ]", "", ele)
		s1.strip()
		mynewlist.append(s1)
	driver.close()
	return mynewlist

def scrapedatatmsck():
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
	url_text_2 = "https://www.thomascook.in/foreign-exchange/forex-rate-card"
	driver.get(url_text_2)
	time.sleep(30)
	mytext = str(driver.find_element_by_class_name("divTableBody").text)
	mytext = mytext[88:]
	mylist = mytext.splitlines()
	print(mylist)
	# mynewlist = []
	# for ele in mylist:
	# 	s1 = re.sub(r"(?!(?<=\d)\.(?=\d))[^0-9]", "", ele)
	# 	mynewlist.append(s1)
	# print(mynewlist)
	driver.close()
	return mylist

def scrapedatacrcykrt():
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
	url_text = "https://currencykart.com/forex/rate-card"
	driver.get(url_text)
	mytext = str(driver.find_element_by_class_name("currency-exchange-city.table-responsive").text)
	mylist = mytext.splitlines()
	mynewlist = []
	for ele in mylist:
		s1 = re.sub(r"(?!(?<=\d)\.(?=\d))[^0-9 ]", "", ele)
		mynewlist.append(s1)
	driver.close()
	return mynewlist
	print(mynewlist)

def scrapedatazenth():
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver")
	url_text = "https://www.zenithforexonline.com/MoneyChangeList"
	driver.get(url_text)
	time.sleep(5)
	driver.find_element_by_link_text("Pune").click()
	time.sleep(2)
	mytext = driver.find_element_by_class_name("table.table-bordered").text
	mylist = mytext.splitlines()
	mylist = mylist[2:]
	mynewlist = []
	for ele in mylist:
		s1 = re.sub(r"(?!(?<=\d)\.(?=\d))[^0-9 ]", "", ele)
		mynewlist.append(s1)
	print(mynewlist)
	driver.close()
	return mynewlist