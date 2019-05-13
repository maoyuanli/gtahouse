import scrapy
from scrapy.loader import ItemLoader
# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from realmaster.items import RealmasterItem


class RealMaster(scrapy.Spider):
    name = 'realmaster'

    def __init__(self, keywords='', *args, **kwargs):
        super(RealMaster, self).__init__(*args, **kwargs)
        self.start_urls = 'http://www.realmaster.com/prop/list/prov=ON.city={0}.ptype=Residential.saletp=sale.mlsonly=1.page={1}'

    def __str__(self):
        return 'realmaster.com spider'

    def start_requests(self):
        GTA = ['Toronto','Mississauga','Oakville','Vaughan',u'Richmond%20Hill','Markham','Burlington','Pickering']
        urls = [self.start_urls.format(city, 1) for city in GTA]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page_number)

    def parse_page_number(self,response):
        total_page_str = response.xpath("""//a[contains(text(),'Total Page')]/text()""").extract_first()
        total_page = int(total_page_str.split(':')[1].strip())
        base_url = response.url[0:-1]
        urls = [base_url + str(i) for i in range(1,total_page+1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        for house in response.xpath("""//div[@class='card_label2']/a"""):
            loader = ItemLoader(item=RealmasterItem(), selector=house, response=response)
            loader.add_xpath('location', """.//@href""")
            loader.add_xpath('price', """normalize-space(.//h4[@class = 'price']/text())""")
            yield loader.load_item()

