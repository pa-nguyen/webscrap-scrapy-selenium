import scrapy
from selenium import webdriver
from scrapy.selector import Selector


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    start_urls = ['https://www.brandstof-zoeker.nl/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome("path/to/chromedriver", chrome_options=self.options)

    def options_scrape(self, tag_id):
        options = []
        select = self.driver.find_element_by_xpath("//select[@id = '" + tag_id + "']")
        select = select.find_elements_by_tag_name("option")
        for option in select:
            options.append(option.text)
        options.pop(0)
        return options

    def parse(self, response):
        self.driver.get(response.url)
        fuels, chains = self.options_scrape("brandstofselect"), self.options_scrape("ketenselect")
        for fuel in fuels:
            for chain in chains:
                search_fuel = self.driver.find_element_by_id('brandstofselect')
                search_fuel.send_keys(fuel)
                search_fuel.click()
                search_chain = self.driver.find_element_by_id('ketenselect')
                search_chain.send_keys(chain)
                search_chain.click()
                response = Selector(text=self.driver.page_source.encode('utf-8'))
                for sel in response.xpath('//li[@class="goedkoop station"]'):
                    details = sel.xpath('ul/li//text()').extract()
                    try:
                        yield {
                            'prices': details[1].split(':')[1].strip(),
                            'time': details[1].split(':')[0],
                            'station': sel.xpath('h2/text()').get().strip(),
                            'address': details[0],
                            'gratis': sel.xpath('ul/li/strong//text()').extract(),
                            'fuel': fuel,
                            'chain': chain,
                        }
                    except IndexError:
                        yield {
                            'prices': 'Unknown',
                            'time': 'Unknown',
                            'station': sel.xpath('h2/text()').get().strip(),
                            'address': details[0],
                            'gratis': sel.xpath('ul/li/strong//text()').extract(),
                            'fuel': fuel,
                            'chain': chain,
                        }
