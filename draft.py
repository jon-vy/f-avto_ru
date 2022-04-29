import requests
from user_agent import generate_user_agent
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import lxml
import re
import math


headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
url = "https://f-avto.ru/goods/d4754413"

r = requests.get(url=url, headers=headers)
# r = requests.post(url=url, headers=headers, params=params)
html_cod = r.text
soup = BeautifulSoup(html_cod, "lxml")
card_item = soup.find('div', id='goods_info')
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
        specifications[key] =val
    except: pass
try:
    prise = card_item.find('span', class_='goods_price').text.strip()
except: pass

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
except: pass

articul = soup.find('td', class_='goods_label').find('b').text


print(html_cod)