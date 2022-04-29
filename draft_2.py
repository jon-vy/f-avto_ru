import requests
from user_agent import generate_user_agent
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import lxml
import re
import math

async def parser(link_item):
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
                    print(f"Не нашёл цену {link_item}")
                    return


                title = card_item.find('h1').text.strip()


                cat = soup.find_all('span', itemprop='name')[-1].text
                if cat.find("вигатель") != -1:
                    category_id = "0"
                elif cat.find("втоматическая") != -1:
                    category_id = "1"
                elif cat.find("еханическ") != -1:
                    category_id = "2"
                elif cat.find("ариатор") != -1:
                    category_id = "3"
                elif cat.find("аздаточн") != -1:
                    category_id = "4"
                elif cat.find("Редуктор переднего моста") != -1:
                    category_id = "5"
                elif cat.find("Редуктор задний") != -1:
                    category_id = "6"
                elif cat.find("Мост задний") != -1:
                    category_id = "7"
                elif cat.find("ТНВД") != -1:
                    category_id = "8"
                elif cat.find("урбин") != -1:
                    category_id = "9"






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

    print(html_cod)
asyncio.run(parser("https://f-avto.ru/goods/d4754413"))