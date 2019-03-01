from selenium import webdriver
import time
import os
import json
from pprint import pprint


class Taobao():

    def __init__(self):
        self.url = "https://market.m.taobao.com/app/tbsearchwireless-pages/categories/p/categories"
        self.headers = {
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36",
            'referer': 'https://h5.m.taobao.com/?sprefer=sypc00',
        }

    def get_cookie(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        cookies_source = driver.get_cookies()
        cookies = {i['name']:i['value'] for i in cookies_source}
        time.sleep(3)
        driver.quit()
        with open('./cookies/cookies.json', 'w+') as f:
            f.write(json.dumps(cookies))
        return cookies
