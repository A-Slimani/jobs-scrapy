from scrapy.exceptions import CloseSpider
from ..items import JobItem
import scrapy


# Propsle spider sucks !!!! will not be using
class ProspleSpider(scrapy.Spider):
    name = "prosple"
    allowed_domains = ["au.prosple.com"]
    start_urls = ["https://au.prosple.com/search-jobs?study_fields=502&locations=9692&defaults_applied=1&sort=closing_date%7Casc"]

    def parse(self, response):
        job_cards = response.xpath('//*[@class="SearchResultsstyle__SearchResult-sc-c560t5-1 hlOmzw"]')

        if job_cards == []:
            raise CloseSpider('No more pages to crawl')
        
        for card in job_cards:
            item = JobItem() 
            item["title"] = card.xpath('.//h2/text()').get()
            item["company"] = card.xpath('').get() 
            item["salary"] = None 
            item["location"] = None 
            item["link"] = None 
            item["close_date"] = None 

            yield item