from django.shortcuts import render
from django.http import HttpResponse
from .models import Cur,CompareOutput
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

	updateData()

	cur = Cur.objects.values()
	cur.query = pickle.loads(pickle.dumps(cur.query))

	#updateData()
	# currency_detail1 = Cur.objects.get(currency_name = val1)
	currency_detail2 = Cur.objects.get(currency_name = val2)

	co1 = CompareOutput.objects.get(id = 1)
	co1.rate = currency_detail2.rate1
	co1.save()
	co2 = CompareOutput.objects.get(id = 2)
	co2.rate = currency_detail2.rate2
	co2.save()
	co3 = CompareOutput.objects.get(id = 3)
	co3.rate = currency_detail2.rate3
	co3.save()
	co4 = CompareOutput.objects.get(id = 4)
	co4.rate = currency_detail2.rate4
	co4.save()
	
	co = CompareOutput.objects.all().order_by("rate")
	print(co)
	rate = co[0].rate
	# rate = currency_detail2.rate1/currency_detail1.rate1
	return render(request,'convert.html',{'tcurr':val2 ,'cur':currency_detail2,'co':co , 'rate' : rate})

def updateData():
	bmf = scrapedatabmf()
	print("len in conv fun")
	print(len(bmf))

	zeneth = scrapedatazenth()
	print(len(zeneth))

	crcykrt = scrapedatacrcykrt()
	print(len(crcykrt))

	tmsck = scrapedatatmsck()
	print(tmsck)
	count = 0
	for v in tmsck:
		print(count)
		print(v)
		print("--------")
		count += 1
	# count = 0

	if len(bmf)>0:
		USD_rate_bmf = bmf[0].split(" ")
		currency_detail_USD = Cur.objects.get(currency_name = 'USD')
		currency_detail_USD.rate1 = USD_rate_bmf[4]
		currency_detail_USD.lastupdated = timezone.now()
		currency_detail_USD.save()

		EUR_rate_bmf = bmf[1].split(" ")
		currency_detail_EUR = Cur.objects.get(currency_name = 'EUR')
		currency_detail_EUR.rate1 = EUR_rate_bmf[4]
		currency_detail_EUR.lastupdated = timezone.now()
		currency_detail_EUR.save()

		GBP_rate_bmf = bmf[2].split(" ")
		currency_detail_GBP = Cur.objects.get(currency_name = 'GBP')
		currency_detail_GBP.rate1 = GBP_rate_bmf[4]
		currency_detail_GBP.lastupdated = timezone.now()
		currency_detail_GBP.save()

		AUD_rate_bmf = bmf[3].split(" ")
		currency_detail_AUD = Cur.objects.get(currency_name = 'AUD')
		currency_detail_AUD.rate1 = AUD_rate_bmf[4]
		currency_detail_AUD.lastupdated = timezone.now()
		currency_detail_AUD.save()

	if len(tmsck)>0:
		currency_detail_USD = Cur.objects.get(currency_name = 'USD')
		currency_detail_USD.rate2 = tmsck[2]
		currency_detail_USD.lastupdated = timezone.now()
		currency_detail_USD.save()

		currency_detail_EUR = Cur.objects.get(currency_name = 'EUR')
		currency_detail_EUR.rate2 = tmsck[7]
		currency_detail_EUR.lastupdated = timezone.now()
		currency_detail_EUR.save()

		currency_detail_GBP = Cur.objects.get(currency_name = 'GBP')
		currency_detail_GBP.rate2 = tmsck[12]
		currency_detail_GBP.lastupdated = timezone.now()
		currency_detail_GBP.save()

		currency_detail_AUD = Cur.objects.get(currency_name = 'AUD')
		currency_detail_AUD.rate2 = tmsck[47]
		currency_detail_AUD.lastupdated = timezone.now()
		currency_detail_AUD.save()

	if len(crcykrt)>0:
		USD_rate_bmf = crcykrt[3].split(" ")
		currency_detail_USD = Cur.objects.get(currency_name = 'USD')
		currency_detail_USD.rate3 = USD_rate_bmf[3]
		currency_detail_USD.lastupdated = timezone.now()
		currency_detail_USD.save()

		EUR_rate_bmf = crcykrt[4].split(" ")
		currency_detail_EUR = Cur.objects.get(currency_name = 'EUR')
		currency_detail_EUR.rate3 = EUR_rate_bmf[3]
		currency_detail_EUR.lastupdated = timezone.now()
		currency_detail_EUR.save()

		GBP_rate_bmf = crcykrt[5].split(" ")
		currency_detail_GBP = Cur.objects.get(currency_name = 'GBP')
		currency_detail_GBP.rate3 = GBP_rate_bmf[3]
		currency_detail_GBP.lastupdated = timezone.now()
		currency_detail_GBP.save()

		AUD_rate_bmf = crcykrt[7].split(" ")
		currency_detail_AUD = Cur.objects.get(currency_name = 'AUD')
		currency_detail_AUD.rate3 = AUD_rate_bmf[3]
		currency_detail_AUD.lastupdated = timezone.now()
		currency_detail_AUD.save()

	if len(zeneth)>0:
		USD_rate_bmf = zeneth[0].split(" ")
		currency_detail_USD = Cur.objects.get(currency_name = 'USD')
		currency_detail_USD.rate4 = USD_rate_bmf[4]
		currency_detail_USD.lastupdated = timezone.now()
		currency_detail_USD.save()

		EUR_rate_bmf = zeneth[1].split(" ")
		currency_detail_EUR = Cur.objects.get(currency_name = 'EUR')
		currency_detail_EUR.rate4 = EUR_rate_bmf[4]
		currency_detail_EUR.lastupdated = timezone.now()
		currency_detail_EUR.save()

		GBP_rate_bmf = zeneth[2].split(" ")
		currency_detail_GBP = Cur.objects.get(currency_name = 'GBP')
		currency_detail_GBP.rate4 = GBP_rate_bmf[4]
		currency_detail_GBP.lastupdated = timezone.now()
		currency_detail_GBP.save()

		AUD_rate_bmf = zeneth[4].split(" ")
		currency_detail_AUD = Cur.objects.get(currency_name = 'AUD')
		currency_detail_AUD.rate4 = AUD_rate_bmf[4]
		currency_detail_AUD.lastupdated = timezone.now()
		currency_detail_AUD.save()


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
