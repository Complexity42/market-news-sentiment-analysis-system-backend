from selenium import webdriver
import time
base_url = 'https://www.uclassify.com/browse/uclassify/iab-taxonomy-v2'
driver_path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

def classify_topic(text):
    driver.get(base_url)
    text_area = driver.find_element_by_css_selector('#text')
    text_area.send_keys(text)
    button = driver.find_element_by_css_selector('body > div.container.body-content > form > div:nth-child(4) > input')
    button.click()
    result = driver.find_element_by_css_selector('body > div.container.body-content > div.container > div:nth-child(1) > div > strong')
    return result.text.split('_')[0]

