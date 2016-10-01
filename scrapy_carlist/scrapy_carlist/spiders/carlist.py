#!/usr/bin/python

import scrapy
from itertools import izip

# global variable
COUNT = 0

class SpiderCarlist(scrapy.Spider):
    name = 'carlist' # spider name

    # list of site to crawl (top-level, first page)
    # respective to global list MANUFACTURER
    start_urls = ['http://www.carlist.my/car/toyota']

    def parse(self, response):
        # total page to crawl = COUNT
        # maximum page per manufacturer = COUNT / len(MANUFACTURER)
        if (COUNT == 10):
            return

        # get top-level of list of car pages
        top = response.css('article div.grid')

        # follow link to car pages
        for href in top.css('h2 a::attr(href)').extract():
            yield scrapy.Request(url=response.urljoin(href), callback=self.parse_car)

    # get data for each page and extract
    def parse_car(self, response):
        # get label for car details
        label = response.css('div.listing__key-listing__list p span.list-item__title::text').extract()
        # get value for car details
        value = response.css('div.listing__key-listing__list p span.float--right::text').extract()

        # combine both label and value to dictionary object
        data = dict(izip(label, value));

        # extract relevant details of car
        yield {
            'Make': data['Make'],
            'Model': data['Model'],
            'Year': data['Year'],
            'Engine Capacity': data['Engine Capacity'],
            'Transmission': data['Transmission'],
            'Seat Capacity': data['Seat Capacity'],
            'Mileage': data['Mileage'],
            'Car type': data['Car type'],
            'Colour': data['Colour']
        }
