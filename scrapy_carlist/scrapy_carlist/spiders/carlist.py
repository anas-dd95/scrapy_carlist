#!/usr/bin/python

import scrapy

# global variable
COUNT = 0
BODY_TYPE = [
    "Converible", "Coupe", "Hatchback", "Lorry", "MPV",
    "Pickup Truck", "SUV", "Sedan", "Van", "Wagon"
]
MANUFACTURER = ["Toyota", "Proton"]

class SpiderCarlist(scarpy.Spider):
    name = 'carlist' # spider name

    # list of site to crawl (top-level, first page)
    # respective to global list MANUFACTURER
    start_urls = []

    def parse(self, response):
        # total page to crawl = COUNT
        # maximum page per manufacturer = COUNT / len(MANUFACTURER)
        if (COUNT == 10):
            return

        top = response.css('article div.grid')

        for ls in top:
            title = ls.css('h2 a::text').extract()
            price = ls.css('p.listing__price::text').extract()
            spec = ls.css('div.listing__spec::text').extract()

            yield {
                'title': title,
                'price': price,
                'spec': spec
            }
