import datetime
from xml.dom import minidom


root = minidom.Document()

today = datetime.datetime.today()
date = today.strftime("%Y-%m-%d %H:%M")

xml_root = root.createElement('yml_catalog')
root.appendChild(xml_root)
xml_root.setAttribute('date', date)

productChild = root.createElement('shop')

nameChild = root.createElement('name')
textName = root.createTextNode('SK Design')
nameChild.appendChild(textName)

companyChild = root.createElement('company')
textCompany = root.createTextNode('SK Design')
companyChild.appendChild(textCompany)

urlChild = root.createElement('url')
textUrl = root.createTextNode('https://skdesign.ru/')
urlChild.appendChild(textUrl)

platformChild = root.createElement('platform')
textPlatform = root.createTextNode('Yml for Yandex Market')
platformChild.appendChild(textPlatform)

versionChild = root.createElement('version')
textVersion = root.createTextNode('001')
versionChild.appendChild(textVersion)

currenciesChild = root.createElement('currencies')

currencyChild = root.createElement('currency')
currencyChild.setAttribute('id', 'RUB')
currencyChild.setAttribute('rate', '1')

categoriesChild = root.createElement('categories')

x = 0
while x < 10:
    categoryChild = root.createElement('category')
    categoryChild.setAttribute('id', f'44454 {x}')
    categoryChild.setAttribute('parentId', '2520')
    textCategory = root.createTextNode(f'Aldo {x}')
    categoryChild.appendChild(textCategory)
    categoriesChild.appendChild(categoryChild)
    x += 1

offersChild = root.createElement('offers')
y = 0
while y < 10:
    offerChild = root.createElement('offer')
    offerChild.setAttribute('group_id', f'162497{y}')
    offerChild.setAttribute('id', f'162499{y}')
    offerChild.setAttribute('available', 'true')
    offersChild.appendChild(offerChild)
    y += 1
    i = 0
    while i < 5:
        paramChild = root.createElement('param')
        paramChild.setAttribute('name', f'name-{i}')
        textParam = root.createTextNode(f'text - {i}')
        paramChild.appendChild(textParam)
        offerChild.appendChild(paramChild)
        i += 1
    nameOfferChild = root.createElement('name')
    textNameOffer = root.createTextNode(f'Table{y}')
    nameOfferChild.appendChild(textNameOffer)
    offerChild.appendChild(nameOfferChild)
    pictureOfferChild = root.createElement('picture')
    textPictureOffer = root.createTextNode(f'url{y}')
    pictureOfferChild.appendChild(textPictureOffer)
    offerChild.appendChild(pictureOfferChild)
    urlOfferChild = root.createElement('url')
    textUrlOffer = root.createTextNode(f'url-variation{y}')
    urlOfferChild.appendChild(textUrlOffer)
    offerChild.appendChild(urlOfferChild)

productChild.appendChild(nameChild)
productChild.appendChild(companyChild)
productChild.appendChild(urlChild)
productChild.appendChild(platformChild)
productChild.appendChild(versionChild)
productChild.appendChild(currenciesChild)
currenciesChild.appendChild(currencyChild)
productChild.appendChild(categoriesChild)
productChild.appendChild(offersChild)

xml_root.appendChild(productChild)

xml_str = root.toprettyxml(indent="\t")
save_path_file = "yandex.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)



# from xml.dom import minidom
# import datetime
# today = datetime.datetime.today()
# date = today.strptime("%Y-%m-%d-%H.%M")
# root = minidom.Document()
#
#
# xml_root = root.createElement('yml_catalog')
# root.appendChild(xml_root)
#
#
# xml_str = root.toprettyxml(indent="\t")
#
# save_path_file = "yandex.xml"
#
# with open(save_path_file, "w") as f:
#     f.write(xml_str)