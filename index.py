from csv import DictWriter
import csv
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import re
import psycopg2
from pprint import pprint
from flask_cors import CORS


conn = psycopg2.connect(database="api_dbs",
                                user='postgres', password='passer', 
                                host='127.0.0.1', port='5432'
)
conn.autocommit = True
cursor = conn.cursor()

app = Flask(__name__)
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='passer',url='localhost',db='api_dbs')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


db = SQLAlchemy(app)
class Jumia(db.Model):
    tablename = 'jumia'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), unique=False, nullable=True)
    description = db.Column(db.String(200), unique=False, nullable=True)
    prix_fcfa = db.Column(db.String(200), unique=False, nullable=True)

    def init(self,image,description,prix_fcfa):
        self.image = image
        self.description = description
        self.prix_fcfa = prix_fcfa

class Alibaba(db.Model):
    tablename = 'alibaba'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), unique=False, nullable=True)
    prix_fcfa = db.Column(db.String(200), unique=False, nullable=True)

    def init(self,description,prix_fcfa):
        self.description = description
        self.prix_fcfa = prix_fcfa

class Auchan(db.Model):
    tablename = 'auchan'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), unique=False, nullable=True)
    description = db.Column(db.String(200), unique=False, nullable=True)
    prix_fcfa = db.Column(db.String(200), unique=False, nullable=True)

    def init(self,image,description,prix_fcfa):
        self.image = image
        self.description = description
        self.prix_fcfa = prix_fcfa

def Scraper():
    url = 'https://www.auchan.sn/198-couches-lingettes-de-bebe'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())
    vente_flash = soup.find(class_='products row product_content grid')
    # print(vente_flash.prettify())
    items = vente_flash.find_all(class_='item-product col-6 col-lg-4')
    # print(items)
    item_data=[]
    for item in items:
        # print(item.prettify())
        prix = item.find("span",class_="price").getText()
        Obtenirprix = prix.split('FCFA')
        # re.sub(r"^\s+|\s+$", "", Obtenirprix[0])
        g = re.sub(r"\s", "", Obtenirprix[0])


        get_data={
            "image" : item.find("img").get('src'),
            "description" : item.find("a",class_="js-add-meti-wishlist").get('data-name'),
            "price en FCFA" : g
        }
        item_data.append(get_data)
        pprint(item_data)

    with open('data_auchan.csv','w') as file:
        datas = DictWriter(file,fieldnames= list(item_data[0].keys()))
        datas.writeheader()
        datas.writerows(item_data)
    # print(datas)

def inserer():
    listes = ['data_alibaba1.csv','data_jumia.csv']
    # for liste in listes:
    with open('data_alibaba1.csv','r') as file:
        readers = csv.DictReader(file)
        data = []
        for reader in readers:
            # print(reader)
            image = reader.get('image')
            description = reader.get('description')
            price = reader.get('price')
            # print(price)
            price = re.sub(r'\s','',price)
            d = {
                'image':image,
                'description':description,
                'prix':price
            }
            data.append(d)
            
        # print(data)
        for d in data:

            try:
                
                sql = "INSERT INTO webscripingAlibaba(image,description,prix_fcfa) VALUES('%s','%s','%s')" % (d['image'],d['description'],d['prix'])
                cursor.execute(sql)
            except Exception as e:
                # pass
                print(e)
    conn.commit()
        
# inserer()

# db.create_all()
# db.drop_all()
