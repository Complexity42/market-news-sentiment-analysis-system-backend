
def getMarketsData():
    import pprint
    import json

    # pp = pprint.PrettyPrinter(indent=2)

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from bs4 import BeautifulSoup

    chrome = webdriver.Chrome(service=Service("./chromedriver"))


    chrome.get("https://www.reuters.com/markets")
    soup = BeautifulSoup(chrome.page_source, "html.parser")


    urls = []
    urls.append(
        "https://www.reuters.com"
        + soup.select(
            "#main-content > div:nth-child(2) > div > div:nth-child(1) > div > div > div.StaticMediaMaximizer__hero___3jy35n > div > div.MediaStoryCard__header___qimiYl > a"
        )[0]["href"]
    )

    for item in soup.select(
        "#main-content > div:nth-child(2) > div > div:nth-child(1) > div > ul > li"
    ):
        urls.append("https://www.reuters.com" + item.select("a")[0]["href"])

    
    for item in soup.select(
        "#main-content > div:nth-child(8) > div > div:nth-child(1) > div > ul > li"
    ):
        urls.append("https://www.reuters.com" + item.select("a")[0]["href"])

    for item in soup.select(
        "#main-content > div:nth-child(8) > div > div:nth-child(2) > div > ul > li"
    ):
        urls.append("https://www.reuters.com" + item.select("a")[0]["href"])

    for item in soup.select(
        "#main-content > div:nth-child(8) > div > div:nth-child(3) > div > ul > li"
    ):
        urls.append("https://www.reuters.com" + item.select("a")[0]["href"])


    # print(urls)


    def getModelByReutersPostUrl(url, source_name=""):
        chrome.get(url)
        soup_content = BeautifulSoup(chrome.page_source, "html.parser")

        title = soup_content.select(
            "#fusion-app > div > div.RegularArticleLayout__content-container___10ugl- > div > div.RegularArticleLayout__main___3Vspvp > article > div > header > div > div.ArticleHeader__heading___3ibi0Q > h1"
        )[0].text.strip()

        keywords = []
        for key in soup_content.select(
            "#fusion-app > div > div.RegularArticleLayout__content-container___10ugl- > div > div.RegularArticleLayout__main___3Vspvp > article > div > header > div > div.ArticleHeader__heading___3ibi0Q > span > span"
        ):
            keywords += key.text.strip().split(",")

        source_date = soup_content.select(
            "#fusion-app > div > div.RegularArticleLayout__content-container___10ugl- > div > div.RegularArticleLayout__main___3Vspvp > article > div > header > div > time > span:nth-child(1)"
        )[0].text

        content = soup_content.select(
            "#fusion-app > div > div.RegularArticleLayout__content-container___10ugl- > div > div.RegularArticleLayout__main___3Vspvp > article > div > div > div > div.ArticleBody__content___2gQno2.paywall-article"
        )[0].text.strip()

        result = {
            "title": title,
            "keywords": keywords,
            "source_name": source_name,
            "source_date": source_date,
            "source_url": url,
            "content": content,
        }

        return result


    results = []

    for url in urls:
        result = getModelByReutersPostUrl(url, source_name="Reuters - Markets")
        # pp.pprint(result)
        results.append(result)

    # print(results)

    # jsonString = json.dumps(results, indent=4)
    # jsonFile = open("output_markets.json", "w")
    # jsonFile.write(jsonString)
    # jsonFile.close()

    chrome.close()

    return results

if __name__ == 'main':
    getMarketsData()


