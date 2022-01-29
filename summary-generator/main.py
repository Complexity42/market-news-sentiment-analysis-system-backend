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

def add_summary():
    db.add_summary()

def main():
    setup()
    add_summary()

if __name__ == '__main__':
    main()
