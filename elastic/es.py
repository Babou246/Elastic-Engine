from csv import DictReader
import os, uuid
import pprint
from elasticsearch import Elasticsearch, helpers
es = Elasticsearch('http://localhost:9200')



###########################################################
###################### ELASTICSEARCH ######################
###########################################################



def bulk_insert_all(index):
    ################ CHARGER LES DONNÉES
    liste = []
    with open('data_alibaba1.csv','r') as file:
        reader = DictReader(file)
        for read in reader:
            liste.append(read)

    # itérateur pour plusieurs documents
    actions = [
        {
            "_id" : uuid.uuid4(),
            "doc_type" : "couche",
            "doc": { 
                "image": liste[d]['image'],
                "description": liste[d]['description'],
                "price": liste[d]['price']
            }
        }
        for d in range(len(liste))
    ]

    try:
        # faire l'appel groupé en utilisant 'actions' et obtenir une réponse
        response = helpers.bulk(es, actions, index='alex', doc_type='couche')
        print ("actions RESPONSE:", response)
    except Exception as e:
        print("ERROR:\n", e)



##### REQUETE MULTI_MATCH
def multi_match(query,index):
    data = es.search(index=index, body={
            "query": {
            "multi_match" : {
                "query": query,
                "type":"bool_prefix",
                "fields": [ "doc.description^2", "doc.price*"]
                }
            }
    })
    return data



###### REQUETES MATCH_PHRASE_PREFIX
def match_phrase_prefix(query,index):
    data = es.search(index=index, body={
        "query": {
            "dis_max": {
                "queries": [
                {
                    "match_phrase_prefix": {
                    "doc.description": query
                    }
                },
                {
                    "match_phrase_prefix": {
                    "doc.price": query
                    }
                }
                ]
            }
        }
    })
    return data


###### RECUPERATIONS DES DONNÉES
def fetch_jumia(query,index):
    
    # Count element(s) trouvé(s)
    match_phrase_prefix(query,index)['hits']['total']['value']
    # On recupere l'image
    data = match_phrase_prefix(query,index)
    listes = []
    for i in range(len(data['hits']['hits'])):
        d = data['hits']['hits']
        image = d[i]['_source']['doc']['image']
        description = d[i]['_source']['doc']['description']
        price = d[i]['_source']['doc']['price']
        listes.append({'image':image,'description':description,'price':price})
    return listes


def fetch_auchan(query,index):
    
    # Count element(s) trouvé(s)
    match_phrase_prefix(query,index)['hits']['total']['value']
    # On recupere l'image
    data = match_phrase_prefix(query,index)
    listes = []
    for i in range(len(data['hits']['hits'])):
        d = data['hits']['hits']
        image = d[i]['_source']['doc']['image']
        description = d[i]['_source']['doc']['description']
        price = d[i]['_source']['doc']['price']
        listes.append({'image':image,'description':description,'price':price})
    return listes