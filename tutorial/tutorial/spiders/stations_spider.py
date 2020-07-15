import scrapy


class StationsSpider(scrapy.Spider):

    name = "station"
    start_urls = [
        'https://www.brandstof-zoeker.nl/',
    ]

    def parse(self, sel):
        for station in sel.css('li#station'):
            yield {
                'name': station.css('h2::text').get(),
                # 'details': station.css('//ul/li::text').get()
            }

        # for station in sel.xpath('//li[@class = "station"]'):
        #     dic = {
        #         'name': station.xpath('h2/text()').extract(),
        #         # 'details': station.css('//ul/li::text').get()
        #     }

