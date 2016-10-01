#!/usr/bin/python

import scrapy
from itertools import izip

# global variable
COUNT = 0

class SpiderCarlist(scrapy.Spider):
    name = 'carlist' # spider name

    # list of site to crawl (top-level, first page)
    start_urls = [
        'http://www.carlist.my/car/toyota/',
        'http://www.carlist.my/car/proton/',
        'http://www.carlist.my/car/mercedes-benz/',
        'http://www.carlist.my/car/perodua/',
        'http://www.carlist.my/car/nissan/',
        'http://www.carlist.my/car/honda/',
        'http://www.carlist.my/car/bmw/',
        'http://www.carlist.my/car/hyundai/',
        'http://www.carlist.my/car/audi/',
        'http://www.carlist.my/car/mitsubishi/'
    ] # total = 10

    def parse(self, response):
        # total page to crawl = COUNT
        # maximum page per manufacturer = COUNT / total start_urls)
        if (COUNT == 80): #  8 pages * 10 start_urls = 80 counts
            return

        # get top-level of list of car pages
        top = response.css('article div.grid')

        # follow link to car pages
        for href in top.css('h2 a::attr(href)').extract():
            yield scrapy.Request(url=response.urljoin(href), callback=self.parse_car)

        # follow pagination links
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            global COUNT # used global variable
            COUNT += 1 # add counter
            yield scrapy.Request(url=next_page, callback=self.parse)

    # get data for each page and extract
    def parse_car(self, response):
        # get label for car details
        label = response.css('div.listing__key-listing__list p span.list-item__title::text').extract()
        # get value for car details
        value = response.css('div.listing__key-listing__list p span.float--right::text').extract()
        # get price for car
        price = response.css('div.grid__item p.listing__price::text').extract_first()

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
            'Colour': data['Colour'],
            'Price': price
        }
