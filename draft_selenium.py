from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ['enable-automation'])  # убирает это браузером chrome управляет автоматизированное тестовое по
# options.add_argument("--headless")  # без отображения браузера

s = Service(executable_path="chromedriver")
url = "https://f-avto.ru/catalog/search"
driver = webdriver.Chrome(service=s, options=options)
driver.maximize_window()  # во весь экран
driver.get(url)
print("открыл")
time.sleep(3)
filter_opption = driver.find_element(By.XPATH, "(.//div[@class='filter-option-inner-inner'])[4]")
filter_opption.click()
span_text = driver.find_element(By.XPATH, "(.//ul[@role='presentation'])[4]/li/a/span[text()='Двигатель']")
span_text.click()
time.sleep(3)

button_search_result = driver.find_element(By.XPATH, "//button[@id='btn-search-result']")
button_search_result.click()

time.sleep(5)
spare_part = "pass"
pageSource = driver.page_source
driver.close()
driver.quit()
print("закрыл")