# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pickle


class PhantomJSMiddleware(object):

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)

    def process_request(self, request, spider):
        print(request.url)
        driver = self.nextPage(request)
        return HtmlResponse(url=request.url, body=driver.page_source, encoding="utf-8")
        # 翻页操作

    def nextPage(self, request):
        self.driver.get(request.url)
        time.sleep(3)
        count = 1
        css_selector = "#root > div > main > div > div.Question-main > div.Question-mainColumn > div > div.Card > button"
        css_selector2 = "#root > div > main > div > div.Question-main > div.Question-mainColumn > div > div.CollapsedAnswers-bar"
        # css_selector = "div > a > img"
        # print(len(self.driver.find_elements_by_css_selector(css_selector)))
        while len(self.driver.find_elements_by_css_selector(css_selector)) == 0 and len(
                self.driver.find_elements_by_css_selector(css_selector2)) == 0:
            print("count:" + str(count))
            js = "var q=document.documentElement.scrollTop=" + str(count * 200000)
            count += 1
            self.driver.execute_script(js)
            time.sleep(0.5)
        print(count)
        time.sleep(2)
        return self.driver

    @classmethod
    # 信号的使用
    def from_crawler(cls, crawler):
        print("from_crawler")
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        print("spider close")
        self.driver.close()

# class PhantomJSMiddleware(object):
#
#     def __init__(self):
#         options = webdriver.ChromeOptions()
#         options.add_argument('headless')
#
#         self.driver = webdriver.Chrome()
#
#         self.driver.get("http://www.baidu.com")
#         time.sleep(2)
#         cookies = pickle.load(open("cookies.txt", "rb"))
#         for cookie_dicts in cookies:
#             print(cookie_dicts)
#             self.driver.add_cookie(cookie_dicts)
#
#         self.driver.implicitly_wait(1)
#
#
#     def process_request(self, request, spider):
#         print(request.url)
#         driver = self.nextPage(request)
#         return HtmlResponse(url=request.url, body=driver.page_source, encoding="utf-8")
#     # 翻页操作
#     def nextPage(self, request):
#         self.driver.get(request.url)
#         time.sleep(2)
#         count = 1
#         css_selector = "#root > div > main > div > div.Question-main > div.Question-mainColumn > div > div.Card > button"
#         css_selector2 = "#root > div > main > div > div.Question-main > div.Question-mainColumn > div > div.CollapsedAnswers-bar"
#         # css_selector = "div > a > img"
#         # print(len(self.driver.find_elements_by_css_selector(css_selector)))
#         while len(self.driver.find_elements_by_css_selector(css_selector)) == 0 and len(self.driver.find_elements_by_css_selector(css_selector2)) == 0:
#             print("count:" + str(count))
#             js = "var q=document.documentElement.scrollTop=" + str(count * 200000)
#             count += 1
#             self.driver.execute_script(js)
#             time.sleep(0.5)
#         print(count)
#         time.sleep(2)
#         return self.driver
#
#     def login(self):
#         # self.driver.get("https://www.zhihu.com/#signin")
#         time.sleep(5)
#         # do login
#         self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/form/div[1]/div[1]/input").send_keys("2963369109@qq.com")
#         self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/form/div[1]/div[2]/input").send_keys("xfxswpkkb1993")
#         time.sleep(10)
#         self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/form/div[2]/button").click()
#         return HtmlResponse(url="https://www.zhihu.com/#signin", body=self.driver.page_source, encoding="utf-8")
#
#     def get_question(self, request):
#         self.driver.find_elements_by_css_selector("#zh-fav-head-title")
#         return HtmlResponse(url=request.url, body=self.driver.page_source, encoding="utf-8")
#
#     @classmethod
#     # 信号的使用
#     def from_crawler(cls, crawler):
#         print("from_crawler")
#
#         print(crawler)
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_closed)
#         return s
#
#     def spider_opened(self, spider):
#         print("spider close")
#         self.driver.close()
