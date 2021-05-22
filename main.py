from typing import final
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re
import time
from nltk import flatten
import requests


options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
browser = webdriver.Firefox(executable_path=r"geckodriver.exe",firefox_options=options)

browser.get("https://www.reddit.com/r/F1Porn")

html = browser.find_element_by_tag_name('html')
i = 0
while True and i <= 50:
    html.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    i += 1;
    

html = browser.page_source

soup = bs(html, 'html.parser')

images = soup.find('div', class_ = 'rpBJOHq2PR60pnwJlUyP0')
h3raw = soup.find('div', class_ = 'rpBJOHq2PR60pnwJlUyP0')
h3 =[]
image = []

div_list = soup.find_all("div", class_ = "_1poyrkZ7g36PawDueRza-J")
images = []
h3 = []
for div in div_list:
    if div.find('span', class_ = "_2oEYZXchPfHwcf9mTMGMg8"):
        continue
    if div.find('a', class_ = "_13svhQIUZqD9PVzFcLwOKT"):
        h3imgur = div.findNext('h3', class_= "_eYtD2XCVieq6emjKBH3m")
        imgur = div.findNext('a', class_ = "_13svhQIUZqD9PVzFcLwOKT")
        h3.append(h3imgur.text)
        images.append(imgur['href'])
    else:
        h3raw = div.find('h3', class_= "_eYtD2XCVieq6emjKBH3m")
        imgraw = div.findNext('img', class_ = "_2_tDEnGMLxpM6uOa2kaDB3")
        h3.append(h3raw.text)
        images.append(imgraw['src'])    

for i, img in enumerate(images):
    if re.search(r"https://preview.redd.it//*[a-z0-9]{13}.jpg", img):
        temp = re.sub(r"preview", r"i", img)
        images[i] = re.findall(r"https://i.redd.it//*[a-z0-9]{13}.jpg", temp)
    else:
        continue
images = flatten(images)

#for downlaoding the images

for i, img in enumerate(images):
    response = requests.get(img)
    try:
        print("Downlaoding {}".format(h3[i]))
        file = open("output\{}.png".format(h3[i]), "wb")
    except OSError: 
        print("***********{} F A I L E D***********".format(h3[i]))
    else:
        print("Download Finished...Saving")
        file.write(response.content)
        print("Done")
        file.close()