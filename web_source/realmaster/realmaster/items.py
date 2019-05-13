import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


# extract address info in the string
def pre_clean_address(raw: str):
    clean_address = raw.split('/')[3]
    return clean_address


class RealmasterItem(scrapy.Item):
    location = scrapy.Field(
        input_processor=MapCompose(str.strip, pre_clean_address),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
