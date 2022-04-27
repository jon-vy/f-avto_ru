import requests
from user_agent import generate_user_agent
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import lxml
import re
import math



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
    print(f"найдено страниц {pagination}")
    return pagination
    # print(soup)


async def get_date(url, pag):
    print(f"Работаю с {url}?page={pag}")
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
    params = {
        "page": pag
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, params=params) as r:
            html_cod = await r.text()
            soup = BeautifulSoup(html_cod, "lxml")
            card_block = soup.find_all("div", class_="card-block")
            for card in card_block:
                link_item = f"https://f-avto.ru{card.find('a').get('href')}"
                title = card.find("a").find('span', class_='text-uppercase').text
                price = card.find('span', class_='font-weight-bold').text.strip()

                small = card.find("a").find_all('small')
                description = ""
                for descr in small:
                    description = f"{description}{' '.join(descr.text.split())}"

                params_item = []

                params_d_none = card.find('div', class_='d-none').find_all('div', class_='row')
                for param in params_d_none:
                    params_item.append(' '.join(param.text.split()))




                print(f"{title}\n{link_item}\n{description}\nЦена {price}\nПараметры\n{params_item}")
                print("1")






async def gather_get_urls():
    urls_category = [
        "https://f-avto.ru/engine",
        "https://f-avto.ru/transmissiya/kpp/avtomaticheskie",
        "https://f-avto.ru/transmissiya/kpp/mekhanicheskie"
    ]
    pagination = get_pagin(urls_category[0])
    tasks = []  # список задач
    for pag in range(1, 2):  # int(pagination)
        task = asyncio.create_task(get_date(urls_category[0], pag))  # создал задачу
        tasks.append(task)  # добавил её в список
    await asyncio.gather(*tasks)
#
#
#
# async def pars():
#     headers = {
#         "accept": "application/json, text/javascript, */*; q=0.01",
#         "User-Agent": generate_user_agent()
#         # "Cookie": "PHPSESSID=d9ir96fbsocha8p50f3obvcnb3; _ga_BBR7SD9FKY=GS1.1.1650973583.1.1.1650974555.0; _ga=GA1.1.810880577.1650973584"
#     }
#
#     r = requests.get(url=urls[1], headers=headers)
#     count_item = r.text
#     return count_item
#     # print(html_cod)



def main():
    asyncio.get_event_loop().run_until_complete(gather_get_urls())



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    urls_category = [
        "https://f-avto.ru/engine",
        "https://f-avto.ru/transmissiya/kpp"
    ]
    main()
    # get_pagin(urls_category[0])

