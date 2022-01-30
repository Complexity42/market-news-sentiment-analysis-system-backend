
def updateNewsByObjectList(db, data):
    news = db.collection('News')

    for item in data:
        # print(item)
        news.document(item['source_name'] + " : " + item['title'].replace('/', ' ')).set(item)
