import scrapy
from selenium import webdriver
from scrapy_selenium import SeleniumRequest


class DriverSpider(scrapy.Spider):
    name = 'driver'

    def start_requests(self):
        urls = ['https://www.brandstof-zoeker.nl/']
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        yield response.request.meta
        # fuel, chain = self.options_scrape("brandstofselect"), self.options_scrape("ketenselect")
        # for i in fuel:
        #     for j in chain:
        # yield SeleniumRequest(url=response.url, callback=self.process_webdriver)

    def process_webdriver(self, driver):
        results = driver.find_element_by_xpath("//div[@id = 'results']")
        yield {
            'text': results.text,
        }

