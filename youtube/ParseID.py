import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import re
def count_lines(filename, chunk_size=1 << 13):
    with open(filename) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))
# Parsing all id's by request string
def parse_id(request_string,path_to_txt, n):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get('https://www.youtube.com/')
    time.sleep(5)
    elem = driver.find_element_by_name("search_query")
    print(elem)
    elem.send_keys(request_string)
    elem.send_keys(Keys.RETURN)
    time.sleep(3)
    i = 0
    urls = []
    while i < n:
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        time.sleep(5)
        i = i+1
    links = driver.find_elements_by_xpath('//*[@id="video-title"]')
    with open(path_to_txt, 'w') as f:
        for link in links:
            url = str(link.get_attribute("href"))
            urls.append(url)
            id = str(link.get_attribute("href"))
            id = id[32:]
            print(url)
            if id != "None":
                print(id)
                f.writelines(f'{id}\n')
    print("Total downloaded ID's:", count_lines(path_to_txt))
    return urls

request_string = "rofl"
filepath_to_txt ='videos.txt'
if __name__ == "__main__":
    parse_id(request_string, filepath_to_txt,n)