import pandas as pd
import matplotlib.pyplot as plt
import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config

from firebase_connection import FireBaseClass
from nltk_algo import getExtractiveSummarization

def setup():
    nltk.download('vader_lexicon')
    nltk.download('stopwords')
    nltk.download('punkt')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    global config
    global db
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10
    db = FireBaseClass()

def fetch():
    # company = input("Input company name:")
    # end_date = datetime.date.today()
    # start_date = end_date - datetime.timedelta(days = 1)
    # end_date = end_date.strftime('%m-%d-%Y')
    # start_date = start_date.strftime('%m-%d-%Y')
    # try:
    #     google_news = GoogleNews(start=start_date, end=end_date)
    #     google_news.search(company)
    #     result = pd.DataFrame(google_news.result())
    #     return result
    # except:
    #     print('Error in fetching!')
    return db.fetch_news()

def nlp_process(data):
    try:
        res = []
        for news in data:
            # print(news)
            try:
                # news = news.to_dict()
                dict = {}
                article = Article(news['source_url'], config=config)
                article.download()
                article.parse()
                article.nlp()
                # summary = getExtractiveSummarization(news['content'])
                analyzer = SentimentIntensityAnalyzer().polarity_scores(article.summary)
                positive = analyzer['pos']
                negative = analyzer['neg']
                score = positive - negative
                res.append((news, score))
            except:
                pass
        return res
    except:
        print('Error in NLP Process!')

def output(res):
    for news in res:
        db.save_result(news[0]['id'],news[1])

def main():
    setup()
    data = fetch()
    res = nlp_process(data)
    # print(res)
    output(res)

if __name__ == '__main__':
    main()
