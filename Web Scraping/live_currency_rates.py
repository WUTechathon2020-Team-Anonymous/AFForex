from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path="chromedriver.exe")

currency_from = 'usd'
currency_to = 'inr'
currency_holder_class = 'dDoNo.vk_bk.gsrt.gzfeS'

url = 'https://www.google.co.in/search?q={0}+to+{1}&ie=UTF-8&oe='.format(currency_from, currency_to)
driver.get(url)
time.sleep(2)
converted_value = driver.find_element_by_class_name(currency_holder_class).text
print(converted_value)
driver.close()