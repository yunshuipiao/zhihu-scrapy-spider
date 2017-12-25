import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import ssl
import pickle
from scrapy import signals

class Zhihu(scrapy.Spider):
    name = "zhihu"
    cookeis = pickle.load(open("cookies.pkl", "rb"))
    urls = []
    questions_url = set()
    for i in range(1, 11):
        temp_url = "https://www.zhihu.com/collection/146079773?page=" + str(i)
        urls.append(temp_url)


    def start_requests(self):
        for url in self.urls:
            request = scrapy.Request(url=url, callback=self.parse, cookies=self.cookeis)
            yield request

    def parse(self, response):
        print(response.url)
        resSoup = BeautifulSoup(response.body, 'lxml')
        items = resSoup.select("div > h2 > a")
        print(len(items))
        for item in items:
            print(item['href'])
            self.questions_url.add(item['href'] + "\n")


    @classmethod
    # 信号的使用
    def from_crawler(cls, crawler, *args, **kwargs):
        print("from_crawler")
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        print("spider close, save urls")
        with open("urls.txt", "w") as f:
            for url in self.questions_url:
                f.write(url)



if __name__ == '__main__':
    cookies = pickle.load(open("cookies.pkl", "rb"))
    url = 'https://www.zhihu.com/collection/146079773'
    driver = webdriver.Chrome()
    driver.get("https://www.zhihu.com/signin")
    for cookie in cookies:
        print(cookie)
        driver.add_cookie(cookie)
    driver.get(url)
    driver.implicitly_wait(2)
    res = driver.page_source
    resSoup = BeautifulSoup(res, 'lxml')
    items = resSoup.select("div > h2 > a")
    print(len(items))
    for item in items:
        print(item)
        print(item.text)

    # ssl._create_default_https_context = ssl._create_unverified_context
    # # url = 'https://www.zhihu.com/collection/146079773'
    # url = "https://www.zhihu.com/signin"
    # # res = requests.get(url, verify=False)
    # driver = webdriver.Chrome()
    # driver.implicitly_wait(5)
    # driver.get(url)
    # time.sleep(40)
    # cookies = driver.get_cookies()
    # pickle.dump(cookies, open("cookies.pkl", "wb"))
    # print("save suc")


    # res = driver.page_source
    # resSoup = BeautifulSoup(res, 'lxml')
    # items = resSoup.select("div > h2 > a")
    # print(len(items))






def next_page_demo():
    #翻页操作
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    driver.get("https://www.zhihu.com/question/22856657")
    time.sleep(2)

    count = 1
    css_selector = "#root > div > main > div > div.Question-main > div.Question-mainColumn > div > div.Card > button"
    css_selector2 = "#root > div > main > div > div.Question-main > div.Question-mainColumn > div > div.CollapsedAnswers-bar"
    while len(driver.find_elements_by_css_selector(css_selector)) == 0 and \
            len(driver.find_elements_by_css_selector(css_selector2)) == 0:
        print("count:" + str(count))
        js = "var q=document.documentElement.scrollTop=" + str(count * 200000)
        count += 1
        driver.execute_script(js)
        time.sleep(0.5)

    resSoup = BeautifulSoup(driver.page_source, 'lxml')
    items = resSoup.select("figure > span > div")
    print(len(items))
    for item in items:
        print(item)
    driver.close()

