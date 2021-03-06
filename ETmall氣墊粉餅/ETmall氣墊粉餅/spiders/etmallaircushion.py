# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from ..items import EtmallItem
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


class EtmallaircushionSpider(scrapy.Spider):
    name = 'etmallaircushion'

    start_urls = ['http://www.etmall.com.tw/%E6%B0%A3%E5%A2%8A%E7%B2%89%E9%A4%85-%E6%B0%A3%E5%A2%8A%E9%9C%9C-%E5%BD%A9%E5%A6%9D%E9%A1%9E%E5%9E%8B/c3/75206?page=/']

    page = 1

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.action = webdriver.ActionChains(self.driver)

    def parse(self, response):
        self.driver.get(response.url)
        res = self.driver.execute_script("return document.documentElement.outerHTML")
        item = EtmallItem()
        soup = BeautifulSoup(res, 'html.parser')

        for items in soup.find('ul', {
            'class': 'n-hover--img n-m-bottom--sm n-card__list fun-searchResult-list'}).find_all_next('div', {
            'class': 'n-card__box'}):
            item['product_name'] = items.find('p', {'class': 'n-name'}).find('a').attrs['title']
            item['product_price'] = items.find('span', {'class': 'n-price--16'}).findAll('span')[1].text.replace(',','')
            item['product_url'] = 'www.etmall.com.tw' + items.find('p', {'class': 'n-name'}).find('a').attrs['href']
            item['product_images'] = 'https:'+ items.find('img').attrs['src']
            item['product_source'] = 'ETMall'
            item['product_category'] = 'Foundation'
            item['product_subcategory'] = 'pressedpowder'

            yield item

        next_page = 'https://www.etmall.com.tw/%E6%B0%A3%E5%A2%8A%E7%B2%89%E9%A4%85-%E6%B0%A3%E5%A2%8A%E9%9C%9C-%E5%BD%A9%E5%A6%9D%E9%A1%9E%E5%9E%8B/c3/75206?page=' + str(
            EtmallaircushionSpider.page)
        if EtmallaircushionSpider.page <= 10:
            # self.action.pause(1)
            # self.action.perform()
            EtmallaircushionSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)
