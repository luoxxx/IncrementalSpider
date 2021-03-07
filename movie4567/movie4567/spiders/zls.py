# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis

class ZlsSpider(CrawlSpider):
    name = 'zls'
    # allowed_domains = ['www.xxx.com']
    conn = Redis(host='127.0.0.1', port=6379, db=0)
    start_urls = ['http://www.4567kan.com/frim/index1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/movie/index(\d+)\.html'), callback='parse_item', process_links='check_link', follow=False),
    )
    def check_link(self, links):
        for link in links:

            ex = self.conn.sadd('movie_urls',link.url)
            if ex == 1:
                print("有数据需要更新")
                yield link
            else:
                print("暂时没有数据需要更新")
    def parse_item(self, response):
        # print(response.text)
        response = response.xpath('//div[@class="stui-vodlist__box"]/a')
        with open('movie.txt', 'a+', encoding='utf-8') as f:
            for res in response:
                name = res.xpath('./@title').extract_first()
                movie_url = res.xpath('./@href').extract_first()
                s = '电影名字：'+name+", "+'电影链接：'+movie_url+'\n'
                f.write(s)

        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
