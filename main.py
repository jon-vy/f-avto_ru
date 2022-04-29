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
from asyncio import Semaphore
from transliterate import translit


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
    # print(f"{url} найдено ссылок {find}")
    return pagination
    # print(soup)

# Собираю ссылки с категорий
async def get_date(url, pag, semaphore):
    await semaphore.acquire()
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
                try:
                    price = card.find('span', class_='font-weight-bold').text
                    link_item = f"https://f-avto.ru{card.find('a').get('href')}"
                    print(f"{link_item}")
                    link_list.append(link_item)
                except:
                    pass
    semaphore.release()


async def gather_get_date():
    semaphore = Semaphore(20)
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
    for url in urls_category:  #[3:4]
        pagination = get_pagin(url)

        tasks = []  # список задач
        for pag in range(1, int(pagination)):  #
            task = asyncio.create_task(get_date(url, pag, semaphore))  # создал задачу
            tasks.append(task)  # добавил её в список
        await asyncio.gather(*tasks)
# Собираю ссылки с категорий


async def gather_parser(root, offers):
    # queue = asyncio.Queue()
    semaphore = Semaphore(20)

    tasks = []
    for link_item in link_list:
        # print(f"Создал задачу с ссылкой {link_item}")
        task = asyncio.create_task(parser(link_item, root, offers, semaphore))
        tasks.append(task)
    # await queue.join()
    await asyncio.gather(*tasks)



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
    print(f"{link_item} | {title}")
    # print(f"Обработал {link_item} | {title}")



async def parser(link_item, root, offers, semaphore):
    # print(f"начал парс {link_item}")
    await semaphore.acquire()
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
                elif cat.find("КПП 5ст") != -1:
                    category_id = "2"
                elif cat.find("КПП 6ст") != -1:
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



                img_source = soup.find('div', id='goods_img').find_all('a')
                url_pic = ""
                for img in img_source:
                    url = img.get('style')
                    url_img = re.search('(?<=\().*?(?=\))', url).group().replace('d.jpg', '.jpg')
                    url_pic = f"{url_pic}{url_img} | "

                try:
                    vid = soup.find('div', id='goods_video').find('iframe').get('src')
                except:
                    vid = "None"

                articul = soup.find('td', class_='goods_label').find('b').text
            except:
                print(f"ошибка здесь {link_item}")
                return

            # <editor-fold desc="Заполнение xml">
            offer = root.createElement('offer')
            offers.appendChild(offer)
            offer.setAttribute('id', f'{articul}')
            offer.setAttribute('available', 'true')
            # offer.setAttribute('group_id', 'id группы товара')

            urlItem = root.createElement('url')
            offer.appendChild(urlItem)
            urlItem_text = root.createTextNode(f'{link_item}')
            urlItem.appendChild(urlItem_text)

            priceItem = root.createElement('price')
            offer.appendChild(priceItem)
            priceItem_text = root.createTextNode(f'{prise}')
            priceItem.appendChild(priceItem_text)

            currencyId = root.createElement('currencyId')
            offer.appendChild(currencyId)
            currencyId_text = root.createTextNode('RUB')
            currencyId.appendChild(currencyId_text)

            titleItem = root.createElement('title')
            offer.appendChild(titleItem)
            title_text = root.createTextNode(f'{title}')
            titleItem.appendChild(title_text)

            categoryId = root.createElement('categoryId')
            offer.appendChild(categoryId)
            categoryId_text = root.createTextNode(f'{category_id}')
            categoryId.appendChild(categoryId_text)

            descriptionItem = root.createElement('description')
            offer.appendChild(descriptionItem)
            descriptionItem_text = root.createTextNode(f'{description}')
            descriptionItem.appendChild(descriptionItem_text)


            goods_info = card_item.find('table', class_='goods_info').find_all('tr')

            for info in goods_info:
                try:
                    key = info.find('th').text
                    # key_tr = translit(key, language_code='ru', reversed=True).replace(' ', '_')

                    if key == "Комплектность":
                        tr_compl = card_item.find('tr', id='tr_compl').find_all('div')
                        val = ""
                        for i in tr_compl:
                            val = f"{val}{i.text}. "
                    else:
                        val = info.find('td').text

                    specificationsItem = root.createElement(f'{key}')  # Создал тег
                    offer.appendChild(specificationsItem)  # Привязал тег
                    specificationsItem_text = root.createTextNode(f'{val}')  # Создал текст для тега
                    specificationsItem.appendChild(specificationsItem_text)  # Добавил текст в тег
                except:
                    pass



            picture = root.createElement('picture')
            offer.appendChild(picture)
            picture_text = root.createTextNode(f'{url_pic}')
            picture.appendChild(picture_text)

            video = root.createElement('video')
            offer.appendChild(video)
            video_text = root.createTextNode(f'{vid}')
            video.appendChild(video_text)
            # </editor-fold>

    print(f"{link_item} | {title}")
    semaphore.release()



def main():
    print("Начат сбор ссылок на товары")

    asyncio.get_event_loop().run_until_complete(gather_get_date())
    print("Сбор ссылок закончен")
    print(f"собрано {len(link_list)} ссылок")
    print("Начинаю сбор данных о товаре")
    # <editor-fold desc="xml начало">
    today = datetime.datetime.today()
    date = today.strftime("%Y-%m-%d %H:%M")

    root = minidom.Document()  # основной элемент

    xml_root = root.createElement('yml_catalog')  # создал элемент с именем yml_catalog
    root.appendChild(xml_root)  # добавил его в качестве дочернего к root
    xml_root.setAttribute('date', date)  # Записал данные в элемент xml_root

    shop = root.createElement('shop')
    xml_root.appendChild(shop)

    name = root.createElement('name')
    shop.appendChild(name)
    text_name = root.createTextNode('f-avto.ru')
    name.appendChild(text_name)

    company = root.createElement('company')
    shop.appendChild(company)
    text_name = root.createTextNode('f-avto.ru')
    company.appendChild(text_name)

    url_company = root.createElement('url')
    shop.appendChild(url_company)
    text_name = root.createTextNode('https://f-avto.ru')
    url_company.appendChild(text_name)

    currencies = root.createElement('currencies')
    shop.appendChild(currencies)

    currency = root.createElement('currency')
    currencies.appendChild(currency)
    currency.setAttribute('id', 'RUB')
    currency.setAttribute('rate', '1')

    categories = root.createElement('categories')
    shop.appendChild(categories)

    category_list = [
        "Двигатели",
        "КПП - автомат",
        "КПП - механика",
        "КПП - вариатор",
        "Раздаточные коробки",
        "Редуктор передний",
        "Редуктор задний",
        "Мост задний",
        "ТНВД",
        "Турбины"
    ]
    for i, cat in enumerate(category_list):
        # for cat in category_list:
        category = root.createElement('category')
        categories.appendChild(category)
        category.setAttribute('id', f'{i}')
        textCategory = root.createTextNode(cat)
        category.appendChild(textCategory)

    offers = root.createElement('offers')
    shop.appendChild(offers)

    # </editor-fold>
    asyncio.get_event_loop().run_until_complete(gather_parser(root, offers))
    # <editor-fold desc="Сохранение xml">
    xml_str = root.toprettyxml(indent="\t")
    save_path_file = "yandex.xml"
    with open(save_path_file, "w", encoding="utf-8") as f:
        f.write(xml_str)
    # </editor-fold>
    print("Работа закончена")
    # get_date_s(driver)




if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Затрачено времени {total_time}")

