from ast import Bytes
from csv import DictReader
from curses import wrapper
from encodings import utf_8
from io import BytesIO
import json
from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from index import Alibaba, Auchan, Jumia, conn,cursor,app,DB_URL,db
from elasticsearch import Elasticsearch, helpers
import os, uuid
from elastic.es import fetch_auchan,fetch_jumia, match_phrase_prefix,multi_match,Elasticsearch,bulk_insert_all,DictReader,es
from flask_paginate import Pagination, get_page_parameter

###########################################################
################ SHOW ALL PRODUCTS IN TEMPLATES ###########
###########################################################

CORS(app)
# es = Elasticsearch('http://localhost:9200')
################# AFFICHER LES DONNÉES

@app.route("/")
def home():
    data = ""
    es_error = ""
    try:
        data = es.search(index="touslesproduits", body={"query": {"match_all": {}}})
    except Exception as e:
        es_error = "Configurer elastisearch et kibana afin de pouvoir y connecter"
        print(es_error)
    liste_data = []
    
    if data:
        for i in data['hits']['hits']:
            liste_data.append(i['_source'])
    return render_template("index.html", data=liste_data, es_error=es_error)

@app.route("/search", methods=['POST'])
def search_es():
    search =  False
    if request.method == 'POST':
        query = request.form['search']
    data = match_phrase_prefix(query,'touslesproduits')
    jumia = fetch_jumia(query,'jumia')
    auchan = fetch_auchan(query,'auchan')
    print(auchan)
    return render_template("index.html", listes_auchan=auchan,listes_jumia=jumia,query=query) 


############################# FIN ELASTIC #################


@app.route('/chart')
@app.route("/index",methods=['GET','POST'])
def index():
    
    results= Jumia.query.all()
    # print(results)
    if request.method == 'POST':
        form = request.form
        search_value = form['recherche']
        # print(search_value)
        search = "%{}%".format(search_value)
        l = Jumia.query.filter(Jumia.description.like(search)).order_by(Jumia.prix_fcfa).all()
        alibaba = Alibaba.query.filter(Alibaba.description.like(search)).order_by(Alibaba.prix_fcfa).all()
        a = Auchan.query.filter(Auchan.description.like(search)).order_by(Auchan.prix_fcfa).all()
        # print(len(a))
        # #########################################
        return render_template('afficheProduit.html',
            name = results, 
            elements = l,
            count = len(search),
            Countl = len(l),
            CountAuchan = len(a),
            CountAlibaba = len(alibaba),
            search = search,
            auchans = a,
            alibaba = alibaba
        )
        
    else:
        l = Jumia.query.all()
        a = Auchan.query.all()
        alibaba = Alibaba.query.all()
        
        return render_template('afficheProduit.html',elements = l,auchans=a,alibaba = alibaba,Countl=len(l),CountAuchan = len(a),CountAlibaba = len(alibaba))

#####################################################
################# GET EACH PRODUIT ##################
#####################################################
@app.route('/api/jumia/<id>', methods=['GET'])
def get_descrip(id):
    result = Jumia.query.filter_by(id=id).first()

    if result:
        return jsonify(status="True", 
                    result={
                                "id":result.id,
                                "image":result.image,
                                "description":result.description,
                                "prix_fcfa":result.prix_fcfa
                            }
                        )
    return jsonify(status="False")

@app.route('/api/auchan/<id>', methods=['GET'])
def get_prix(id):
    result = Jumia.query.filter_by(id=id).first()

    if result:
        return jsonify(status="True", 
                    result={
                                "id":result.id,
                                "image":result.image,
                                "description":result.description,
                                "prix_fcfa":result.prix_fcfa
                            }
                        )
    return jsonify(status="False")

####################################################
############ API ALL PRODUITS ######################
####################################################
@app.route('/api/jumia', methods=['GET'])
def get_all():
    result = Jumia.query.all()
    # print(result)
    liste =[]
    for i in result:
        d ={}
        d["id"] = i.id
        print(i.id)
        d["image"] = i.image
        d["description"]  = i.description
        d["prix_fcfa"] = i.prix_fcfa
        liste.append(d)
    return jsonify(liste)

@app.route('/api/auchan', methods=['GET'])
def get_all_produitAuchan():
    result = Auchan.query.all()
    # print(result)
    liste =[]
    for i in result:
        d ={}
        d["id"] = i.id
        d["image"] = i.image
        d["description"]  = i.description
        d["prix_fcfa"] = i.prix_fcfa
        liste.append(d)
    return jsonify(liste)

@app.route('/api/alibaba', methods=['GET'])
def get_produits_alibaba():
    result = Alibaba.query.all()
    # print(result)
    liste =[]
    for i in result:
        d ={}
        d["id"] = i.id
        # d["image"] = i.image
        d["description"]  = i.description
        d["prix_fcfa"] = i.prix_fcfa
        liste.append(d)
    return jsonify(liste)



##########################################################
################# LANCEMENT DU SERVEUR ###################

if __name__ == "__main__":
     app.run(host="0.0.0.0",debug=True)