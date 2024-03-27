from scrapy.exceptions import CloseSpider
from datetime import datetime as dt
from ..items import JobItem
import scrapy


class HatchSpider(scrapy.Spider):
    name = "hatchspider"
    allowed_domains = ["api.master.hatch.team"]
    start_urls = ["https://api.master.hatch.team/role-page/summary/search/open?hatchOnly=false&page=0&pageSize=20&roleFamilies=software%20engineering%2Cdata%20analytics"]
    page_no = 0

    def parse(self, response):
        json_data = response.json()

        def format_date(date_string):
            date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            date_obj = dt.strptime(date_string, date_format)
            return date_obj.strftime("%d/%m/%Y")

        if json_data['summaries'] == []:
            raise CloseSpider('No more pages to crawl')

        for job in json_data['summaries']:
            item = JobItem() 
            item['company_name'] = job['company']['companyName']
            item['job_title'] = job['roleTitle']
            item['location'] = job['location']
            item['link'] = f'https://hatch.team/role/{job["roleContextId"]}'
            item['close_date'] = job['applicationsCloseDateTime']
            # item['close_date_cleaned'] = format_date(job['applicationsCloseDateTime'])
            yield item

        self.page_no += 1
        next_page = f"https://api.master.hatch.team/role-page/summary/search/open?hatchOnly=false&page={self.page_no}&pageSize=20&roleFamilies=software%20engineering%2Cdata%20analytics"
        yield response.follow(next_page, callback=self.parse)
        
