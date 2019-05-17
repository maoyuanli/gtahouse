import re

import scrapy
# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from realmaster.items import RealmasterItem
from scrapy.loader import ItemLoader


class RealMaster(scrapy.Spider):
    name = 'realmaster'

    def __init__(self, keywords='', *args, **kwargs):
        super(RealMaster, self).__init__(*args, **kwargs)
        self.base_url = 'http://www.realmaster.com/prop/list/prov=ON.city={0}.ptype=Residential.ptype2={1}.saletp=sale.mlsonly=1.page='
        self.gta = ['Aurora', 'Burlington', 'Hamilton', 'Markham', 'Milton', 'Mississauga', 'Newmarket', 'Oakville',
                    'Oshawa', 'Pickering', 'Richmond%20Hill', 'Toronto', 'Vaughan']
        self.proptype = ['Detached', 'Semi-Detached', 'Townhouse', 'Apartment', 'Loft', 'Bungalow', 'Cottage']

    def url_generator(self):
        start_urls = []
        for city in self.gta:
            for cat in self.proptype:
                url = self.base_url.format(city,cat) + '{0}'
                start_urls.append(url)
        return start_urls

    def __str__(self):
        return 'realmaster.com spider'

    def start_requests(self):
        start_urls = self.url_generator()
        page1_urls = [ url.format(1) for url in start_urls]
        for p1_url in page1_urls:
            yield scrapy.Request(url=p1_url, callback=self.parse_page_number)

    def parse_page_number(self, response):
        total_page_str = response.xpath("""//a[contains(text(),'Total Page')]/text()""").extract_first()
        total_page = int(total_page_str.split(':')[1].strip())
        new_base_url = response.url[0:-1]
        urls = [new_base_url + str(i) for i in range(1, total_page + 1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        for house in response.xpath("""//div[@class='card_label2']/a"""):
            loader = ItemLoader(item=RealmasterItem(), selector=house, response=response)
            loader.add_xpath('location', """.//@href""")
            loader.add_xpath('price', """normalize-space(.//h4[@class = 'price']/text())""")
            loader.add_value('city', re.findall(r'city=(.*?)\.', response.url)[0])
            loader.add_value('proptype' ,re.findall(r'ptype2=(.*?)\.', response.url)[0])
            yield loader.load_item()
