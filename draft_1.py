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
url = "https://f-avto.ru/engine"

r = requests.get(url=url, headers=headers)
# r = requests.post(url=url, headers=headers, params=params)
html_cod = r.text
soup = BeautifulSoup(html_cod, "lxml")
card_block = soup.find_all("div", class_="card-block")
# print(f"Работаю с {url}?page={pag}")
for card in card_block:
    try:
        price = card.find('span', class_='font-weight-bold').text
        link_item = f"https://f-avto.ru{card.find('a').get('href')}"
    except: pass




print(html_cod)