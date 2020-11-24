from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import re


currency_index = {'usd': 0, 'eur': 1, 'gbp': 2, 'aud': 3}
payment_method_format = {'buy_cash': 0, 'buy_card': 1, 'sell_cash': 2, 'sell_card': 3}


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
            usd = values_list[0].lstrip().rstrip().split(" ")
            usd = list(map(float, [usd[2], usd[0], usd[4], usd[5]]))
            eur = values_list[1].lstrip().rstrip().split(" ")
            eur = list(map(float, [eur[2], eur[0], eur[4], eur[5]]))
            gbp = values_list[2].lstrip().rstrip().split(" ")
            gbp = list(map(float, [gbp[2], gbp[0], gbp[4], gbp[5]]))
            aud = values_list[3].lstrip().rstrip().split(" ")
            aud = list(map(float, [aud[2], aud[0], aud[4], aud[5]]))
            values_list = [usd, eur, gbp, aud]
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
            usd = list(map(float, [values[2], values[1], values[3], "-1"]))
            eur = list(map(float, [values[7], values[6], values[8], "-1"]))
            gbp = list(map(float, [values[12], values[11], values[13], "-1"]))
            aud = list(map(float, [values[47], values[46], values[48], "-1"]))
            values_list = [usd, eur, gbp, aud]
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
            usd = values_list[3].lstrip().rstrip().split(" ")
            usd = list(map(float, [usd[0], usd[2], usd[1], usd[3]]))
            eur = values_list[4].lstrip().rstrip().split(" ")
            eur = list(map(float, [eur[0], eur[2], eur[1], eur[3]]))
            gbp = values_list[5].lstrip().rstrip().split(" ")
            gbp = list(map(float, [gbp[0], gbp[2], gbp[1], gbp[3]]))
            aud = values_list[7].lstrip().rstrip().split(" ")
            aud = list(map(float, [aud[0], aud[2], aud[1], aud[3]]))
            values_list = [usd, eur, gbp, aud]
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
            usd = values_list[0].lstrip().rstrip().split(" ")
            usd = list(map(float, [usd[1], usd[2], usd[0], "-1"]))
            eur = values_list[1].lstrip().rstrip().split(" ")
            eur = list(map(float, [eur[1], eur[2], eur[0], "-1"]))
            gbp = values_list[2].lstrip().rstrip().split(" ")
            gbp = list(map(float, [gbp[1], gbp[2], gbp[0], "-1"]))
            aud = values_list[4].lstrip().rstrip().split(" ")
            aud = list(map(float, [aud[1], aud[2], aud[0], "-1"]))
            values_list = [usd, eur, gbp, aud]        
        return values_list


