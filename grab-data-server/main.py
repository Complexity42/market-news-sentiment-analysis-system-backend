import threading
from time import sleep

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import data_source.Reuters.world
import data_source.Reuters.business
import data_source.Reuters.markets
import data_source.Reuters.breakingviews

import data_source.JPMorgan.news

import data_source.RSS.rss

from util.update_news import updateNewsByObjectList


### Init firebase ###
cred = credentials.Certificate('./serviceAccount.json')
firebase_admin.initialize_app(cred, options = { "httpTimeout": 660 })


### Get data source ###

def udpateReutersWorld():
    print("Get Reuters World data ...")
    reutersWorld =  data_source.Reuters.world.getWorldData()
    print("Get Reuters World data done")

    db = firestore.client()
    print("Update firebase - Reuters World ...")
    updateNewsByObjectList(db, reutersWorld)
    print("Update firebase - Reuters World done")
    db.close()


def udpateReutersBusiness():
    print("Get Reuters Business data ...")
    reutersBusiness =  data_source.Reuters.business.getBusinessData()
    print("Get Reuters Business data done")

    db = firestore.client()
    print("Update firebase - Reuters Business ...")
    updateNewsByObjectList(db, reutersBusiness)
    print("Update firebase - Reuters Business done")
    db.close()


def updateReuterMarkets():
    print("Get Reuters Markets data ...")
    reutersMarkets =  data_source.Reuters.markets.getMarketsData()
    print("Get Reuters Markets data done")

    db = firestore.client()
    print("Update firebase - Reuters Markets ...")
    updateNewsByObjectList(db, reutersMarkets)
    print("Update firebase - Reuters Markets done")
    db.close()


def updateReuterBreakingViews():
    print("Get Reuters BreakingViews data ...")
    reutersBreakingViews =  data_source.Reuters.breakingviews.getBreakingviewsData()
    print("Get Reuters BreakingViews data done")

    db = firestore.client()
    print("Update firebase - Reuters BreakingViews ...")
    updateNewsByObjectList(db, reutersBreakingViews)
    print("Update firebase - Reuters BreakingViews done")
    db.close()

def updateJPMorgan():
    print("Get JPMorgan News data ...")
    jpmorganNews =  data_source.JPMorgan.news.getNewsData()
    print("Get JPMorgan News data done")

    db = firestore.client()
    print("Update firebase - JPMorgan News ...")
    updateNewsByObjectList(db, jpmorganNews)
    print("Update firebase - JPMorgan News done")
    db.close()

def updateRSS():
    print("Get RSS data ...")
    rssData = data_source.RSS.rss.getRSSData()
    print("Get RSS data done")

    db = firestore.client()
    print("Update firebase - RSS data ...")
    updateNewsByObjectList(db, rssData)
    print("Update firebase - RSS data done")
    db.close()


while True:
    threads = [
        threading.Thread(target=udpateReutersWorld),
        threading.Thread(target=udpateReutersBusiness),
        threading.Thread(target=updateReuterMarkets),
        threading.Thread(target=updateReuterBreakingViews),
        threading.Thread(target=updateJPMorgan),
        threading.Thread(target=updateRSS),
    ]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
    
    print("Sleep for 10 minutes ...")
    sleep(600)


