import feedparser

def RssToNewsModelList(source_name, url):
    feed = feedparser.parse(url)

    results = []
    for entry in feed.entries:

        keywords = []
        if("tags" in entry):
            keywords = list(map(lambda x: x.term, entry.tags))
        
        summary = ""
        if("summary" in entry):
            summary = entry.summary

        result = {
            "title": entry.title,
            "keywords": keywords,
            "source_name": source_name,
            "source_date": entry.published,
            "source_url": entry.link,
            "content": summary
        }
        results.append(result)
    
    return results

def getRSSData():
    urls = [
        ["CNBC", "https://www.cnbc.com/id/19746125/device/rss/rss.xml"],
        ["Financial Times", "https://www.ft.com/rss/home/uk"],
        ["Fortune", "https://fortune.com/feed"],
        ["Morning Star", "https://feeds.feedburner.com/morningstar/glkd"],
        ["Investing.com", "https://www.investing.com/rss/news.rss"],
        ["The Financial Express", "https://www.financialexpress.com/feed/"],
        ["Seeking Alpha", "https://seekingalpha.com/market_currents.xml"],
        ["Yahoo Finance", "https://finance.yahoo.com/news/rssindex"],
        ["Financial Post", "https://financialpost.com/feed"],
        ["Money Web", "https://www.moneyweb.co.za/feed/"],
        ["Business Matters", "https://bmmagazine.co.uk/feed/"],
        ["Business Daily", "https://www.businessdailyafrica.com/latestrss.rss"],
        ["Insights Success", "https://insightssuccess.com/feed/"]
    ]

    results = []
    for source_name, url in urls:
        results += RssToNewsModelList(source_name, url)
    
    return results




