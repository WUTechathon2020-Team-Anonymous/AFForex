from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import re


class ForexProviderRates():
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

    def scrape_bookmyforex(self):
        driver = webdriver.Firefox(firefox_options=self.firefox_options, executable_path=self.firefox_driver_path)
        base_url = "https://www.bookmyforex.com/"

        driver.get(base_url)
        time.sleep(10)
        driver.find_element_by_class_name("see_frc_btn").click()
        time.sleep(5)
        values = str(driver.find_element_by_class_name("fullratetable.table-responsive").text)
        values = values[203:]
        lines = values.splitlines()
        del lines[14:]
        values_list = []
        for element in lines:
            s1 = re.sub(r"(?!(?<=\d)\.(?=\d))[^0-9 ]", "", element)
            values_list.append(s1)

        driver.close()
        if len(values_list) > 0:
            usd = values_list[0].split(" ")[4]
            eur = values_list[1].split(" ")[4]
            gbp = values_list[2].split(" ")[4]
            aud = values_list[3].split(" ")[4]
            values_list = [usd, eur, gbp, aud]
            values_list = list(map(float, values_list))
        return values_list

    def scrape_thomascook(self):
        driver = webdriver.Firefox(firefox_options=self.firefox_options, executable_path=self.firefox_driver_path)
        base_url = "https://www.thomascook.in/foreign-exchange/forex-rate-card"

        driver.get(base_url)
        time.sleep(25)
        values = str(driver.find_element_by_class_name("divTableBody").text)
        values = values[88:]
        values = values.splitlines()

        driver.close()
        values_list = []
        if len(values) > 0:
            usd = values[2]
            eur = values[7]
            gbp = values[12]
            aud = values[47]
            values_list = [usd, eur, gbp, aud]
            values_list = list(map(float, values_list))
        return values_list

    def scrape_currencykart(self):
        driver = webdriver.Firefox(firefox_options=self.firefox_options, executable_path=self.firefox_driver_path)
        base_url = "https://currencykart.com/forex/rate-card"

        driver.get(base_url)
        time.sleep(3)
        values = str(driver.find_element_by_class_name("currency-exchange-city.table-responsive").text)
        lines = values.splitlines()
        values_list = []
        for element in lines:
            value = re.sub(r"(?!(?<=\d)\.(?=\d))[^0-9 ]", "", element)
            values_list.append(value)

        driver.close()
        if len(values_list) > 0:
            usd = values_list[3].split(" ")[3]
            eur = values_list[4].split(" ")[3]
            gbp = values_list[5].split(" ")[3]
            aud = values_list[7].split(" ")[3]
            values_list = [usd, eur, gbp, aud]
            values_list = list(map(float, values_list))
        return values_list

    def scrape_zenithforex(self):
        driver = webdriver.Firefox(firefox_options=self.firefox_options, executable_path=self.firefox_driver_path)
        base_url = "https://www.zenithforexonline.com/MoneyChangeList"

        driver.get(base_url)
        time.sleep(5)
        driver.find_element_by_link_text("Pune").click()
        time.sleep(3)
        values = str(driver.find_element_by_class_name("table.table-bordered").text)
        lines = values.splitlines()
        lines = lines[2:]
        values_list = []
        for element in lines:
            value = re.sub(r"(?!(?<=\d)\.(?=\d))[^0-9 ]", "", element)
            values_list.append(value)

        driver.close()
        if len(values_list) > 0:
            usd = values_list[0].split(" ")[4]
            eur = values_list[1].split(" ")[4]
            gbp = values_list[2].split(" ")[4]
            aud = values_list[4].split(" ")[4]
            values_list = [usd, eur, gbp, aud]        
            values_list = list(map(float, values_list))
        return values_list


