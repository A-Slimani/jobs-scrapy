from scrapy.exceptions import CloseSpider
from ..items import JobItem 
import scrapy


class SeekspiderSpider(scrapy.Spider):
    name = "seekspider"
    allowed_domains = ["www.seek.com.au"]
    start_urls = ["https://www.seek.com.au/jobs-in-information-communication-technology/in-All-Sydney-NSW"]
    page_number = 1

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def parse(self, response):
        job_cards = response.xpath('//*[@data-card-type="JobCard"]')

        if job_cards == []:
            raise CloseSpider('No more pages to crawl')

        for card in job_cards:
            item = JobItem()
            item["title"] = card.xpath('.//*[starts-with(@id, "job-title-")]/text()').get()
            item["company"] = card.xpath('.//*[@data-automation="jobCompany"]/text()').get()
            item["salary"] = card.xpath('.//*[@class="y735df0 _153p76c1 _1iz8dgs4y _1iz8dgs0 _1iz8dgsr _153p76c3"]/text()').get()
            item["location"] = card.xpath('.//*[@data-automation="jobLocation"]/text()').get()
            item["link"] = f"https://seek.com.au{card.xpath('.//*[starts-with(@id, "job-title-")]/@href').get()}"

            yield item

        self.page_number += 1
        next_page = f"https://www.seek.com.au/jobs-in-information-communication-technology/in-All-Sydney-NSW?page={self.page_number}"
        yield response.follow(next_page, callback=self.parse)
    
    