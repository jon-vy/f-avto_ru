import requests
from user_agent import generate_user_agent
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import lxml
import re
import math
import datetime
from xml.dom import minidom
from value import link_list
import time


def get_pagin(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
    r = requests.get(url=url, headers=headers)
    html_cod = r.text
    soup = BeautifulSoup(html_cod, "lxml")
    p = soup.find("button", id="btn-search-result").text
    find = p.strip().split()[1]
    pag = int(find)/20
    pagination = math.ceil(pag)
    print(f"{url} найдено ссылок {find}")
    return pagination
    # print(soup)

# Собираю ссылки с категорий
async def get_date(url, pag):

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
    params = {
        "page": pag
    }
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(3)
        async with session.get(url=url, headers=headers, params=params) as r:
            html_cod = await r.text()
            soup = BeautifulSoup(html_cod, "lxml")
            card_block = soup.find_all("div", class_="card-block")
            # print(f"Работаю с {url}?page={pag}")
            for card in card_block:
                link_item = f"https://f-avto.ru{card.find('a').get('href')}"
                # print(link_item)
                # pars(link_item)
                link_list.append(link_item)

async def gather_get_date():
    urls_category = [
        "https://f-avto.ru/engine",
        "https://f-avto.ru/transmissiya/kpp/avtomaticheskie",
        "https://f-avto.ru/transmissiya/kpp/mekhanicheskie",
        "https://f-avto.ru/transmissiya/kpp/razdatochnaye-korobki",
        "https://f-avto.ru/toplivnaya-sistema/tnvd",
        "https://f-avto.ru/zapchasti-dlya-dvigatelya/sistema-turbonadduva/turbiny",
        "https://f-avto.ru/transmissiya/mosty/zadnie/zadnie-mosty",
        "https://f-avto.ru/transmissiya/mosty/zadnie/reduktory-zadnego-mosta",
        "https://f-avto.ru/transmissiya/mosty/perednie/reduktory-perednego-mosta"
    ]
    for url in urls_category:  # [1:2]
        pagination = get_pagin(url)
        tasks = []  # список задач
        for pag in range(1, int(pagination)):  #
            task = asyncio.create_task(get_date(url, pag))  # создал задачу
            tasks.append(task)  # добавил её в список
        await asyncio.gather(*tasks)
# Собираю ссылки с категорий


async def gather_parser():
    queue = asyncio.Queue()
    tasks = []
    for link_item in link_list:
        task = asyncio.create_task(parser(link_item, queue))
        tasks.append(task)
    await queue.join()
    await asyncio.gather(*tasks, return_exceptions=True)



def pars(link_item):
    # print(f"начал парс {link_item}")
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
    r = requests.get(url=link_item, headers=headers)
    html_cod = r.text
    soup = BeautifulSoup(html_cod, "lxml")
    try:
        card_item = soup.find('div', id='goods_info')

        try:
            prise = card_item.find('span', class_='goods_price').text.strip()
        except:
            return

        title = card_item.find('h1').text.strip()

        try:
            description = card_item.find('td', colspan='2').text.strip()
        except:
            description = "None"

        goods_info = card_item.find('table', class_='goods_info').find_all('tr')

        specifications = {}
        for info in goods_info:
            try:
                key = info.find('th').text
                val = info.find('td').text
                specifications[key] = val
            except:
                pass

        img_source = soup.find('div', id='goods_img').find_all('a')
        img_1_dict = {}
        img_list_1 = []
        img_list_2 = []
        img_list_3 = []
        for img in img_source:
            url_i = img.get('style')
            url_img = re.search('(?<=\().*?(?=\))', url_i).group().replace('d.jpg', '.jpg')
            chek = url_img.split('/')[4]
            if chek == "detail":
                img_list_1.append(url_img)
            elif chek == "endoscope":
                img_list_2.append(url_img)
            elif chek == "lot":
                img_list_3.append(url_img)
        img_1_dict["Фото"] = img_list_1
        img_1_dict["Фото эндоскопом"] = img_list_2
        img_1_dict["Фото до разборки"] = img_list_3
        try:
            video = soup.find('div', id='goods_video').find('iframe').get('src')
        except:
            pass

        articul = soup.find('td', class_='goods_label').find('b').text
    except:
        print(f"ошибка здесь {link_item}")
        return
    print(f"Обработал {link_item} | {title}")



async def parser(link_item, queue: asyncio.Queue):
    # print(f"начал парс {link_item}")
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
    # async with aiohttp.ClientSession() as session:
    # async with aiohttp.ClientSession()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=200), trust_env=True) as session:

        await asyncio.sleep(3)
        async with session.get(url=link_item, headers=headers) as r:
            html_cod = await r.text()
            soup = BeautifulSoup(html_cod, "lxml")
            try:
                card_item = soup.find('div', id='goods_info')

                try:
                    prise = card_item.find('span', class_='goods_price').text.strip()
                except:
                    return

                title = card_item.find('h1').text.strip()

                try:
                    description = card_item.find('td', colspan='2').text.strip()
                except:
                    description = "None"

                goods_info = card_item.find('table', class_='goods_info').find_all('tr')

                specifications = {}
                for info in goods_info:
                    try:
                        key = info.find('th').text
                        val = info.find('td').text
                        specifications[key] = val
                    except:
                        pass

                img_source = soup.find('div', id='goods_img').find_all('a')
                img_1_dict = {}
                img_list_1 = []
                img_list_2 = []
                img_list_3 = []
                for img in img_source:
                    url_i = img.get('style')
                    url_img = re.search('(?<=\().*?(?=\))', url_i).group().replace('d.jpg', '.jpg')
                    chek = url_img.split('/')[4]
                    if chek == "detail":
                        img_list_1.append(url_img)
                    elif chek == "endoscope":
                        img_list_2.append(url_img)
                    elif chek == "lot":
                        img_list_3.append(url_img)
                img_1_dict["Фото"] = img_list_1
                img_1_dict["Фото эндоскопом"] = img_list_2
                img_1_dict["Фото до разборки"] = img_list_3
                try:
                    video = soup.find('div', id='goods_video').find('iframe').get('src')
                except:
                    pass

                articul = soup.find('td', class_='goods_label').find('b').text
            except:
                print(f"ошибка здесь {link_item}")
                return
    print(f"Обработал {link_item} | {title}")



def main():
    asyncio.get_event_loop().run_until_complete(gather_get_date())
    asyncio.get_event_loop().run_until_complete(gather_parser())

    # get_date_s(driver)




if __name__ == '__main__':
    start_time = time.time()
    print("Начат сбор ссылок на товары")
    main()
    # get_date_s(driver)
    print("Сбор ссылок закончен")
    print(f"собрано {len(link_list)} ссылок")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"затрачено на сбор ссылок {total_time}")

