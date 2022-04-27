import requests
from user_agent import generate_user_agent
from bs4 import BeautifulSoup

headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": generate_user_agent()
    }
params = {
    "flt_nomenclature": "амортизатор"
}
url = "https://f-avto.ru/catalog/search?filter_catalog=on"

r = requests.post(url=url, headers=headers, params=params)
html_cod = r.text
print(html_cod)

# url = "https://f-avto.ru/transmissiya/kpp"
# r = requests.get(url=url, headers=headers)
# # r = requests.post(url=url, headers=headers, params=params)
# html_cod = r.text
# soup = BeautifulSoup(html_cod, "lxml")
# links_list = []
# links = soup.find_all("a", class_="nomenclature1")
# for link in links:
#     links_list.append(link.get("href"))
#     print(link.get("href"))
# print(html_cod)