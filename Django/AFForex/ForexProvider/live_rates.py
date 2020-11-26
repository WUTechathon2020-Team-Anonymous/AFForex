from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

class LiveRates():
	def __init__(self):
		self.firefox_options = Options()
		self.firefox_options.add_argument("--headless")
		self.firefox_options.add_argument("--disable-notifications")
		self.firefox_options.add_argument("--disable-infobars")
		self.firefox_options.add_argument("--disable-extensions")
		# self.firefox_options.set_preference('dom.push.enabled', False)
		# self.firefox_options.set_preference('geo.enabled', False)
		self.firefox_options.set_preference("geo.prompt.testing", True)
		self.firefox_options.set_preference("geo.prompt.testing.allow", False)
		self.firefox_driver_path = "/usr/local/bin/geckodriver"#"./../../drivers/geckodriver"

		self.currency_holder_class = 'dDoNo.vk_bk.gsrt.gzfeS'

	def get_live_rates(self, currency_from, currency_to):
		try:
			driver = webdriver.Firefox(firefox_options=self.firefox_options, executable_path=self.firefox_driver_path)
			url = 'https://www.google.co.in/search?q={0}+to+{1}&ie=UTF-8&oe='.format(currency_from, currency_to)

			driver.get(url)
			time.sleep(2)
			value = driver.find_element_by_class_name(self.currency_holder_class).text

			return value.split(" ")[0]

		except Exception:
			return -1
