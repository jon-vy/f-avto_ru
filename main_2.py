import math
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from user_agent import generate_user_agent
from value import link_list

user_agent = generate_user_agent()
options = webdriver.ChromeOptions()
options.add_argument((f'"{generate_user_agent()}"'))  # user_agent добавляется только так. Не напутать с кавычками
# options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")  или так
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ['enable-automation'])  # убирает это браузером chrome управляет автоматизированное тестовое по
options.add_argument("--headless")  # без отображения браузера

s = Service(executable_path="chromedriver")

driver = webdriver.Chrome(service=s, options=options)
driver.maximize_window()  # во весь экран
def get_date_s(driver):
    find_worlds = [
        "КПП-вариатор",
        "Редуктор переднего моста",
        "Редуктор задний",
    ]
    url = "https://f-avto.ru/catalog/search"
    driver.get(url)
    for word in find_worlds:

        # print("открыл")
        # time.sleep(3)
        filter_opption = driver.find_element(By.XPATH, "(.//div[@class='filter-option-inner-inner'])[4]")
        filter_opption.click()
        print(word)
        span_text = driver.find_element(By.XPATH, f"(.//ul[@role='presentation'])[4]/li/a/span[text()='{word}']")
        span_text.click()
        time.sleep(3)

        chek = driver.find_element(By.XPATH, "//button[@id='btn-search-result']").text
        if chek != "Нет предложений":
            pag = int(chek.split()[1])/20
            pagination = math.ceil(pag)

            button_search_result = driver.find_element(By.XPATH, "//button[@id='btn-search-result']")
            button_search_result.click()
            time.sleep(3)
            i = 1
            while True:
                try:
                    link_item = driver.find_element(By.XPATH, f"(.//a[@class='nomenclature1'])[{i}]").get_attribute("href")
                    i = i + 1
                    print(link_item)
                    link_list.append(link_item)
                except: break

            if pagination > 1:
                for i in range(2, pagination):
                    driver.get(f"https://f-avto.ru/catalog/search?page={i}")
                    i = 1
                    while True:
                        try:
                            link_item = driver.find_element(By.XPATH, f"(.//a[@class='nomenclature1'])[{i}]").get_attribute("href")
                            i = i + 1
                            print(link_item)
                        except:
                            break
            else: pass

        else: break

    # time.sleep(5)
    spare_part = "pass"
    pageSource = driver.page_source
    driver.close()
    driver.quit()
    print("закрыл")

get_date_s(driver)