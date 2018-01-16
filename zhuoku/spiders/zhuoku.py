# coding:utf-8

import scrapy
from scrapy.selector import Selector
from ..items import ImageItem
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

class zhuoku(scrapy.Spider):
    name = "zhuoku"
    allowed_domain = ["zhuoku.com"]
    start_urls = ["http://www.zhuoku.com/zhuomianbizhi/show/index-1.htm"]

    def parse(self, response):
        sel = Selector(response)
        for first_urls in sel.xpath('//*[@id="liebiao"]/div[@class="bizhiin"]/a[2]/@href').extract():
            first_url = response.urljoin(first_urls)
            print "first url is: " + first_url
            self.logger.info("first url is: %s", first_url)
            yield Request(first_url, callback=self.second_parse)

        next_pages = sel.xpath('//*[@id="liebiao"]/div[@class="turn"]/select/option/@value').extract()
        for next_page in next_pages:
            if next_page is not None:
                page = response.urljoin(next_page)
                print "next page is: " + page
                self.logger.info("next page is: %s", page)
                yield Request(page, callback=self.parse)

    def second_parse(self, response):
        sel = Selector(response)
        for second_urls in sel.xpath('//*[@id="liebiao"]/div[@class="bizhiin"]/a/@href').extract():
            second_url = response.urljoin(second_urls)
            print "second url is: " + second_url
            self.logger.info("second url is: %s", second_url)
            yield Request(second_url, callback=self.third_parse)

    def third_parse(self, response):
        sel = HtmlXPathSelector(response)
        imgs = sel.select('//*[@id="imageview"]/@src').extract()
        item = ImageItem()
        item['image_urls'] = imgs
        return item
