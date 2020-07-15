# webscrape-scrapy-selenium

The project aims to scrape dynamically loaded websites using scrapy and selenium. 

The website used in this example is https://www.brandstof-zoeker.nl, a gas station listing website that uses Ajax to query 
data and Javascript to modify the source code. The interactive nature of the website also requires an interaction with DOM
inside the crawler to fully extract the data. 

Therefore, Selenium is incorporated with Scrapy to finish this task efficiently.

Documentation on both modules:
* Scrapy: https://docs.scrapy.org/en/latest/intro/overview.html
* Selenium: https://selenium-python.readthedocs.io/

In this project, `sel.py` uses solely Selenium whereas `crawler_spider.py` incorporates both Scrapy and selenium and 
has superior speed. Alternatively, driver_spider attempts to use scrapy-selenium, as suggested in this [document](https://docs.scrapy.org/en/latest/topics/dynamic-content.html)

More documentation and usage of items and pipelines coming soon!  
