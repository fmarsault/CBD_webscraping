# Felix Marsault CBD1
# TP Scrapping

import scrapy


class ScSpider(scrapy.Spider):
    name = "SoundCloud"
    start_urls = ["https://soundcloud.com/cigarettesaftersex/followers"]

    def parse(self, response):
        page = response.css('nomargin')
        print(page)

