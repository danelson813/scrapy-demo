import scrapy
from ..items import QuotescraperItem


class QuotescraperSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        base = "https://quotes.toscrape.com"
        quotes = response.xpath('//span[@class="text"]/text()').extract()
        authors = response.css('small.author::text').extract()

        items = QuotescraperItem()
        items['author'] = authors
        items['quote'] = quotes

        yield {
            "author": authors,
            'quote': quotes
        }

        next_page_url = base + response.xpath('//li[@class="next"]/a/@href')[0].extract()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback=self.parse)
