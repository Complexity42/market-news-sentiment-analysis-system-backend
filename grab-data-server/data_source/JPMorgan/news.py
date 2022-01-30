import pprint
import json

# pp = pprint.PrettyPrinter(indent=2)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def getNewsData():
    chrome = webdriver.Chrome(service=Service("./chromedriver"))
    chrome.get("https://www.jpmorgan.com")

    soup = BeautifulSoup(chrome.page_source, "html.parser")
    items = soup.select("#jpmc-dynamic-grid-0 > div > .item")

    results = []

    for item in items:

        title = ""
        source_date = ""
        url = ""
        content = ""

        for field in item.contents:

            if field.name != "div":
                continue

            if field["class"][0] == "title":
                title = field.text.strip()
                url = field.a["href"].strip()

            if field["class"][0] == "date":
                source_date = field.text.strip()

        chrome.get("https://www.jpmorgan.com" + url)
        soup_content = BeautifulSoup(chrome.page_source, "html.parser")
        contents = soup_content.select(".article__body__text")
        content = contents[0].text.strip()

        # print("Title: " + title)
        # print("Date: " + source_date)
        # print("Url: " + url)
        # print("Content: " + content)

        result = {
            "title": title,
            "keywords": [],
            "source_name": "JPMorgan",
            "source_date": source_date,
            "source_url": "https://www.jpmorgan.com" + url,
            "content": content,
        }
        # pp.pprint(result)
        results.append(result)


    # jsonString = json.dumps(results, indent=4)
    # jsonFile = open("output.json", "w")
    # jsonFile.write(jsonString)
    # jsonFile.close()

    chrome.close()

    return results


if __name__ == "__main__":
    getNewsData()

    
