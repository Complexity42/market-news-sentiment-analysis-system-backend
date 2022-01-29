
def updateNewsByObjectList(db, data):
    news = db.collection('News')

    for item in data:
        news.document(item['source_name'] + " : " + item['title']).set(item)
