from csv import DictWriter
from bs4 import BeautifulSoup
import requests
from pprint import pprint

url = 'https://www.jumia.sn/catalog/?q=couches+b%C3%A9b%C3%A9'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)
vente_flash = soup.find('div','-paxs row _no-g _4cl-3cm-shs')
# print(vente_flash.prettify())
items = vente_flash.find_all(class_='prd _fb col c-prd')
item_data=[]
for item in items:

    get_data={
        "item_image" : item.find("img",class_="img").get("data-src"),
        "desc" : item.find("h3",class_="name").getText(),
        "item_prix" : item.find("div",class_="prc").getText()
    }
    item_data.append(get_data)
    pprint(item_data)

with open('data_jumia.csv','w') as file:
    datas = DictWriter(file,fieldnames= list(item_data[0].keys()))
    datas.writeheader()
    datas.writerows(item_data)
    # print(datas)

