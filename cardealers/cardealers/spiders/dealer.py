# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from cardealers.items import CardealersItem


class DealerSpider(scrapy.Spider):
    name = 'dealer'
    allowed_domains = ['cardekho.com']
    start_urls = ['https://www.cardekho.com/cardealers']

    def parse(self, response):
        companies_list = response.xpath(
            "//li[@class='gsc_col-xs-4 gsc_col-sm-3 gsc_col-md-3 gsc_col-lg-2']/a/@href").getall()
        # companies_list contains list of links to different company's dealers

# ------------Comment this section later-----------------
        # l = []
        # l.append(companies_list[0])
        # companies_list = l
# ----------------------------------------------------------

        if len(companies_list) is not 0:
            for company in companies_list:
                yield response.follow(company, callback=self.parse_cities)

    def parse_cities(self, response):
        cities_list = response.xpath(
            "//li[@class='gsc_col-xs-4 gsc_col-sm-3 gsc_col-md-2']/a/@href").getall()

# -------------- Comment this section later-----------------
        # l = []
        # l.append(cities_list[0])
        # cities_list = l
# -----------------------------------------------------------

        if len(cities_list) is not 0:
            for city in cities_list:
                yield response.follow(city, callback=self.parse_dealers)

    def parse_dealers(self, response):
        sections = response.xpath("//section[@class='marginBottom20 shadow24 dlradrWpr']")
        for section in sections:
            str = section.xpath('h2/text()').get().split()
            company = str[0]
            city = str[3]
            if 'Aston' in str or 'Rover' in str:
                company = ' '.join(str[:2])
                city = ' '.join(str[4:])
            if 'New' in str:
                city = 'New Delhi'
            for dealer_info in section.xpath("div/div/div/div/div"):
                l = ItemLoader(CardealersItem())
                name = dealer_info.xpath("h3/a/text()").get()
                address = dealer_info.xpath("div/div[@class='cd_address']/text()").get()
                email = dealer_info.xpath("div/div[@class='cd_mail']/text()").get()
                contact_number = dealer_info.xpath("div/div[@class='cd_call']/text()").get()
                l.add_value('city', city)
                l.add_value('company', company)
                l.add_value('name', name)
                l.add_value('address', address)
                l.add_value('email', email)
                l.add_value('contact_number', contact_number)
                yield l.load_item()
