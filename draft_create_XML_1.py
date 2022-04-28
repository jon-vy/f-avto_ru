import datetime
from xml.dom import minidom

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

offer = root.createElement('offer')
offers.appendChild(offer)
offer.setAttribute('id', 'id товара')
offer.setAttribute('available', 'true')
offer.setAttribute('group_id', 'id группы товара')

urlItem = root.createElement('url')
offer.appendChild(urlItem)
urlItem_text = root.createTextNode('ссылка на страницу товара')
urlItem.appendChild(urlItem_text)

priceItem = root.createElement('price')
offer.appendChild(priceItem)
priceItem_text = root.createTextNode('цена на товар')
priceItem.appendChild(priceItem_text)

currencyId = root.createElement('currencyId')
offer.appendChild(currencyId)
currencyId_text = root.createTextNode('RUB')
currencyId.appendChild(currencyId_text)

titleItem = root.createElement('title')
offer.appendChild(titleItem)
title_text = root.createTextNode('title название товара')
titleItem.appendChild(title_text)

categoryId = root.createElement('categoryId')
offer.appendChild(categoryId)
categoryId_text = root.createTextNode('id категории товара')
categoryId.appendChild(categoryId_text)

descriptionItem = root.createElement('categoryId')
offer.appendChild(descriptionItem)
descriptionItem_text = root.createTextNode('description описание товара')
descriptionItem.appendChild(descriptionItem_text)

specificationsItem = root.createElement('specifications')
offer.appendChild(specificationsItem)
specificationsItem_text = root.createTextNode('характеристики товара')
specificationsItem.appendChild(specificationsItem_text)

picture = root.createElement('picture')
offer.appendChild(picture)
picture_text = root.createTextNode('картинки товара')
picture.appendChild(picture_text)












xml_str = root.toprettyxml(indent="\t")
save_path_file = "yandex_1.xml.xml"
with open(save_path_file, "w", encoding="utf-8") as f:
    f.write(xml_str)













