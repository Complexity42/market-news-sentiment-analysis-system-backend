
import news_model_adapter.adapter as adapter

def updateNewsByObjectList(db, data):
    news = db.collection('News')

    for item in data:
        item = adapter.toOutput(item)
        print(item)
        news.document(item['source_name'] + " : " + item['title'].replace('/', ' ')).set(item)
